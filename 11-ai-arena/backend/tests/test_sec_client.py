import json
import unittest

from backend.adapters.sec_client import SECClient, SECFetchError, SECResponse


class FakeClock:
    def __init__(self):
        self.now = 0.0
        self.sleeps = []

    def monotonic(self):
        return self.now

    def sleep(self, seconds):
        self.sleeps.append(seconds)
        self.now += seconds


class FakeTransport:
    def __init__(self, responses):
        self.responses = list(responses)
        self.calls = []

    def get(self, url, *, headers, timeout, max_bytes):
        self.calls.append({"url": url, "headers": dict(headers), "timeout": timeout, "max_bytes": max_bytes})
        if not self.responses:
            raise AssertionError("unexpected extra HTTP request")
        response = self.responses.pop(0)
        if isinstance(response, Exception):
            raise response
        return response


def response(payload, status=200, headers=None):
    body = payload if isinstance(payload, bytes) else json.dumps(payload).encode("utf-8")
    return SECResponse(status=status, headers=headers or {}, body=body)


def client(transport, clock=None, **kwargs):
    clock = clock or FakeClock()
    instance = SECClient(
        "AI Arena research contact research@example.com", transport=transport,
        monotonic=clock.monotonic, sleep=clock.sleep, **kwargs,
    )
    return instance, clock


class SECClientTests(unittest.TestCase):
    def test_user_agent_requires_contact_email_and_from_env_requires_configuration(self):
        with self.assertRaises(SECFetchError):
            SECClient("AI Arena research bot")
        with self.assertRaises(SECFetchError):
            SECClient("AI Arena research contact research@example.com\\nInjected: header")
        with self.assertRaises(SECFetchError):
            SECClient.from_env()

    def test_only_https_sec_hosts_are_allowed(self):
        transport = FakeTransport([response({"ok": True})])
        sec, _ = client(transport)
        for url in ("http://data.sec.gov/a", "https://example.com/a", "https://data.sec.gov.evil.test/a",
                    "https://user@data.sec.gov/a", "https://data.sec.gov:444/a"):
            with self.subTest(url=url), self.assertRaises(SECFetchError):
                sec.get_json(url)
        self.assertEqual(transport.calls, [])

    def test_cik_helpers_call_correct_sec_endpoints_and_set_headers(self):
        transport = FakeTransport([response({"cik": 123}), response({"facts": {}}), response({"0": {"ticker": "EXM"}})])
        sec, _ = client(transport)
        self.assertEqual(sec.get_submissions(123)["cik"], 123)
        self.assertEqual(sec.get_companyfacts("0000000123"), {"facts": {}})
        self.assertIn("0", sec.get_company_tickers())
        self.assertTrue(transport.calls[0]["url"].endswith("/submissions/CIK0000000123.json"))
        self.assertTrue(transport.calls[1]["url"].endswith("/companyfacts/CIK0000000123.json"))
        self.assertTrue(transport.calls[2]["url"].endswith("/files/company_tickers.json"))
        self.assertEqual(transport.calls[0]["headers"]["User-Agent"], "AI Arena research contact research@example.com")
        self.assertEqual(transport.calls[0]["headers"]["Accept"], "application/json")

    def test_429_retry_after_is_respected_and_success_is_cached(self):
        transport = FakeTransport([
            response({"error": "rate limit"}, status=429, headers={"Retry-After": "1"}),
            response({"cik": 123}),
        ])
        sec, clock = client(transport, min_interval=.25)
        first = sec.get_submissions(123)
        first["cik"] = "mutated by caller"
        second = sec.get_submissions(123)
        self.assertEqual(second["cik"], 123)
        self.assertEqual(len(transport.calls), 2)
        self.assertIn(1.0, clock.sleeps)
        self.assertEqual(transport.calls[0]["headers"], transport.calls[1]["headers"])

    def test_requests_are_spaced_by_minimum_interval(self):
        transport = FakeTransport([response({"a": 1}), response({"b": 2})])
        sec, clock = client(transport, min_interval=.5)
        sec.get_json("https://data.sec.gov/a")
        sec.get_json("https://data.sec.gov/b")
        self.assertTrue(any(abs(x - .5) < 1e-9 for x in clock.sleeps))

    def test_transient_5xx_uses_exponential_backoff(self):
        transport = FakeTransport([
            response({"error": "temporary"}, status=503),
            response({"ok": True}),
        ])
        sec, clock = client(transport, base_backoff=.5)
        self.assertEqual(sec.get_json("https://data.sec.gov/a"), {"ok": True})
        self.assertIn(.5, clock.sleeps)
        self.assertEqual(len(transport.calls), 2)

    def test_non_retryable_status_invalid_json_and_oversized_response_fail(self):
        sec, _ = client(FakeTransport([response({"denied": True}, status=403)]))
        with self.assertRaises(SECFetchError):
            sec.get_json("https://data.sec.gov/a")
        sec, _ = client(FakeTransport([response(b"not-json")]))
        with self.assertRaises(SECFetchError):
            sec.get_json("https://data.sec.gov/a")
        sec, _ = client(FakeTransport([response(b"1234567890")]), max_response_bytes=5)
        with self.assertRaises(SECFetchError):
            sec.get_json("https://data.sec.gov/a")

    def test_retry_limit_is_bounded(self):
        transport = FakeTransport([response({}, status=503), response({}, status=503), response({}, status=503)])
        sec, _ = client(transport, max_retries=2)
        with self.assertRaises(SECFetchError):
            sec.get_json("https://data.sec.gov/a")
        self.assertEqual(len(transport.calls), 3)

    def test_cik_normalization_rejects_empty_input(self):
        self.assertEqual(SECClient.normalize_cik("123"), "0000000123")
        for invalid in ("ABC", "ABC123", "12345678901", 0, True, 1.5):
            with self.subTest(invalid=invalid), self.assertRaises(SECFetchError):
                SECClient.normalize_cik(invalid)


if __name__ == "__main__":
    unittest.main(verbosity=2)
