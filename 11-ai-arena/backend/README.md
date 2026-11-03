# AI Arena backend — evidence gateway core (V0.1)

This is the first executable backend contract behind `experience-v3/REAL_DATA_BLUEPRINT.md`. It is intentionally provider-agnostic and uses only the Python standard library.

## Implemented

- Exact issuer resolution with explicit `resolved` / `ambiguous` / `not_found` outcomes. Ambiguous tickers are never silently selected.
- Immutable, source-attributed evidence records with UTC publication, availability and retrieval timestamps, provider/license metadata, JSON payloads and SHA-256 content hashes.
- Point-in-time evidence-pack freezing. Records unavailable at the requested `as_of` cutoff are excluded; foreign issuers, invalid chronology, unapproved licenses and conflicting duplicate IDs fail closed.
- Typed faction-research contract with confidence, evidence/counter-evidence references, entry triggers, invalidation conditions and a hard target-weight cap.
- Append-only in-memory event ledger with payload hashes and a verifiable previous-event hash chain.
- SEC EDGAR submissions/companyfacts parser anchors each fact to the filing `acceptanceDateTime` and accession, never the reporting period end or date-only `filingDate`. Missing acceptance times, unmatched accessions and form mismatches are excluded. License status defaults to `review_required`.
- Read-only SEC JSON client requires an explicit contact-email User-Agent, allows only HTTPS SEC hosts, paces requests at no more than 4/sec by default, honors Retry-After, retries bounded transient failures, caps response size and caches successful JSON briefly in memory.

## Run tests in the project virtual environment

```bash
.venv/bin/python -m unittest discover -s backend/tests -v
PYTHONPATH=/opt/pyvenv/lib/python3.13/site-packages .venv/bin/python tests/test_ui.py
```

The current backend suite contains **30 standard-library tests**, including SEC accession timestamp, duplicate-accession collision, fiscal-frame identity, User-Agent validation, host allowlisting, rate limiting, bounded retries, response-size limits and cache behavior. The repository workflow runs this suite alongside the Finance Lab Playwright browser regression.

## Explicit non-goals

The SEC parser accepts already-fetched JSON; the separate SEC client can make read-only requests only when explicitly constructed with a configured `SEC_USER_AGENT`. No live SEC request was performed in this milestone. Alpaca, news, macro and sentiment adapters are not connected. No API keys, live LLM workers, database persistence, broker integration or order execution are included. Fixture records in tests are synthetic. The SEC adapter defaults to `review_required`; a caller must complete terms review before promoting any record to `approved`. A production adapter must preserve provider accession/version data and source-specific `available_at`, and create a new immutable snapshot rather than rewriting old evidence.
