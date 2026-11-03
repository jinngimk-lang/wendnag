"""Conservative, read-only SEC JSON client with identity and rate-limit guards.

No request is made at import time. Construct SECClient with an explicit
identifying User-Agent (including a monitored contact email), or use
SECClient.from_env() with SEC_USER_AGENT configured. Tests inject a fake
transport; production calls remain opt-in.
"""
from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
import json
import os
import re
import time
from typing import Mapping, Protocol
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen
from urllib.parse import urlparse


class SECFetchError(RuntimeError):
    pass


@dataclass(frozen=True, slots=True)
class SECResponse:
    status: int
    headers: Mapping[str, str]
    body: bytes


class SECTransport(Protocol):
    def get(self, url: str, *, headers: Mapping[str, str], timeout: float, max_bytes: int) -> SECResponse:
        ...


class UrllibSECTransport:
    """Small urllib transport; response bodies are bounded before parsing."""

    def get(self, url: str, *, headers: Mapping[str, str], timeout: float, max_bytes: int) -> SECResponse:
        request = Request(url, headers=dict(headers), method="GET")
        try:
            with urlopen(request, timeout=timeout) as response:
                return SECResponse(
                    status=int(response.status), headers=dict(response.headers.items()),
                    body=response.read(max_bytes + 1),
                )
        except HTTPError as exc:
            return SECResponse(
                status=int(exc.code), headers=dict(exc.headers.items()) if exc.headers else {},
                body=exc.read(max_bytes + 1),
            )
        except URLError as exc:
            raise SECFetchError(f"SEC transport error: {exc.reason}") from exc


class SECClient:
    ALLOWED_HOSTS = frozenset({"data.sec.gov", "www.sec.gov"})
    RETRYABLE_STATUSES = frozenset({429, 500, 502, 503, 504})

    def __init__(
        self,
        user_agent: str,
        *,
        transport: SECTransport | None = None,
        timeout: float = 15.0,
        min_interval: float = 0.25,
        max_retries: int = 3,
        base_backoff: float = 0.5,
        max_backoff: float = 8.0,
        cache_ttl_seconds: float = 30.0,
        max_response_bytes: int = 25_000_000,
        monotonic=time.monotonic,
        sleep=time.sleep,
    ) -> None:
        if not isinstance(user_agent, str) or not user_agent.strip():
            raise SECFetchError("SEC_USER_AGENT is required")
        if not re.search(r"[^\s@]+@[^\s@]+\.[^\s@]+", user_agent):
            raise SECFetchError("SEC User-Agent must identify a contact email")
        if timeout <= 0 or min_interval < 0.1 or max_retries < 0 or max_retries > 5:
            raise SECFetchError("invalid SEC client timeout, rate limit or retry configuration")
        if base_backoff < 0 or max_backoff < base_backoff or cache_ttl_seconds < 0 or max_response_bytes <= 0:
            raise SECFetchError("invalid SEC client backoff, cache or response-size configuration")
        self.user_agent = user_agent.strip()
        self.transport = transport or UrllibSECTransport()
        self.timeout = timeout
        self.min_interval = min_interval
        self.max_retries = max_retries
        self.base_backoff = base_backoff
        self.max_backoff = max_backoff
        self.cache_ttl_seconds = cache_ttl_seconds
        self.max_response_bytes = max_response_bytes
        self._monotonic = monotonic
        self._sleep = sleep
        self._next_request_at = 0.0
        self._cache: dict[str, tuple[float, dict]] = {}

    @classmethod
    def from_env(cls, **kwargs) -> "SECClient":
        return cls(os.environ.get("SEC_USER_AGENT", ""), **kwargs)

    def _validate_url(self, url: str) -> None:
        parsed = urlparse(url)
        if (parsed.scheme != "https" or parsed.hostname not in self.ALLOWED_HOSTS
                or parsed.username or parsed.password or parsed.port not in (None, 443)):
            raise SECFetchError("SEC client only permits HTTPS requests to approved SEC hosts")

    def _pace(self) -> None:
        wait = self._next_request_at - self._monotonic()
        if wait > 0:
            self._sleep(wait)
        self._next_request_at = self._monotonic() + self.min_interval

    def _retry_delay(self, headers: Mapping[str, str], attempt: int) -> float:
        normalized = {str(k).lower(): str(v) for k, v in headers.items()}
        raw = normalized.get("retry-after")
        if raw:
            try:
                return min(self.max_backoff, max(0.0, float(raw)))
            except ValueError:
                try:
                    retry_at = parsedate_to_datetime(raw)
                    if retry_at.tzinfo is None:
                        retry_at = retry_at.replace(tzinfo=timezone.utc)
                    return min(self.max_backoff, max(0.0, (retry_at - datetime.now(timezone.utc)).total_seconds()))
                except (TypeError, ValueError, OverflowError):
                    pass
        return min(self.max_backoff, self.base_backoff * (2 ** attempt))

    def get_json(self, url: str) -> dict:
        self._validate_url(url)
        now = self._monotonic()
        cached = self._cache.get(url)
        if cached and now - cached[0] <= self.cache_ttl_seconds:
            return deepcopy(cached[1])

        headers = {
            "User-Agent": self.user_agent,
            "Accept": "application/json",
            "Accept-Encoding": "identity",
        }
        for attempt in range(self.max_retries + 1):
            self._pace()
            try:
                response = self.transport.get(
                    url, headers=headers, timeout=self.timeout, max_bytes=self.max_response_bytes,
                )
            except SECFetchError:
                if attempt >= self.max_retries:
                    raise
                self._sleep(min(self.max_backoff, self.base_backoff * (2 ** attempt)))
                continue
            if len(response.body) > self.max_response_bytes:
                raise SECFetchError("SEC response exceeds configured size limit")
            if response.status in self.RETRYABLE_STATUSES:
                if attempt >= self.max_retries:
                    raise SECFetchError(f"SEC returned retryable HTTP status {response.status} after retries")
                self._sleep(self._retry_delay(response.headers, attempt))
                continue
            if response.status != 200:
                raise SECFetchError(f"SEC returned HTTP status {response.status}")
            try:
                payload = json.loads(response.body.decode("utf-8"))
            except (UnicodeDecodeError, json.JSONDecodeError) as exc:
                raise SECFetchError("SEC response was not valid UTF-8 JSON") from exc
            if not isinstance(payload, dict):
                raise SECFetchError("SEC JSON response must be an object")
            self._cache[url] = (self._monotonic(), deepcopy(payload))
            return payload
        raise SECFetchError("SEC request exhausted retries")

    @staticmethod
    def normalize_cik(cik: str | int) -> str:
        digits = "".join(ch for ch in str(cik) if ch.isdigit())
        if not digits:
            raise SECFetchError("CIK must contain digits")
        return digits.zfill(10)

    def get_submissions(self, cik: str | int) -> dict:
        normalized = self.normalize_cik(cik)
        return self.get_json(f"https://data.sec.gov/submissions/CIK{normalized}.json")

    def get_companyfacts(self, cik: str | int) -> dict:
        normalized = self.normalize_cik(cik)
        return self.get_json(f"https://data.sec.gov/api/xbrl/companyfacts/CIK{normalized}.json")

    def get_company_tickers(self) -> dict:
        return self.get_json("https://www.sec.gov/files/company_tickers.json")
