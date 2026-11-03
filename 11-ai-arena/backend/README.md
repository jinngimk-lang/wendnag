# AI Arena backend — evidence gateway core (V0.1)

This is the first executable backend contract behind \`experience-v3/REAL_DATA_BLUEPRINT.md\`. It is intentionally provider-agnostic and uses only the Python standard library.

## Implemented

- Exact issuer resolution with explicit \`resolved\` / \`ambiguous\` / \`not_found\` outcomes. Ambiguous tickers are never silently selected.
- Immutable, source-attributed evidence records with UTC publication, availability and retrieval timestamps, provider/license metadata, JSON payloads and SHA-256 content hashes.
- Point-in-time evidence-pack freezing. Records unavailable at the requested \`as_of\` cutoff are excluded; foreign issuers, invalid chronology, unapproved licenses and conflicting duplicate IDs fail closed.
- Typed faction-research contract with confidence, evidence/counter-evidence references, entry triggers, invalidation conditions and a hard target-weight cap.
- Append-only in-memory event ledger with payload hashes and a verifiable previous-event hash chain.
- SEC EDGAR submissions/companyfacts parser anchors each fact to the filing `acceptanceDateTime` and accession, never the reporting period end or date-only `filingDate`. Missing acceptance times and unmatched accessions are excluded. License status defaults to `review_required`.

## Run tests in the project virtual environment

\`\`\`bash
.venv/bin/python -m unittest discover -s backend/tests -v
PYTHONPATH=/opt/pyvenv/lib/python3.13/site-packages .venv/bin/python tests/test_ui.py
\`\`\`

## Explicit non-goals

No SEC, Alpaca, news, macro or sentiment provider is connected yet. No network requests, API keys, live LLM workers, database persistence, broker integration or order execution are included. Fixture records in tests are synthetic. A production adapter must preserve provider accession/version data and source-specific \`available_at\`, pass license review, and create a new immutable snapshot rather than rewriting old evidence.
