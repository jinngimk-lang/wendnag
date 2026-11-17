#!/usr/bin/env python3
"""Deterministic public-report arithmetic; amounts are RMB millions.
Run from any cwd: python scripts/check_metrics.py
No dependencies; source pages: S01, S02 in SOURCES.md.
"""
from math import isclose
d = dict(
    revenue_2026h1=2917.692, revenue_2025h1=3112.662,
    gross_2026h1=2318.408, gross_2025h1=2542.345,
    sell_2026h1=1266.821, sell_2025h1=1058.575,
    rnd_2026h1=45.517, rnd_2025h1=41.176,
    cashflow_2026h1=789.709, cashflow_2025h1=715.689,
    net_2026h1=939.528, net_2025h1=1182.444,
)
r = lambda a,b: 100*a/b
gross26=r(d["gross_2026h1"],d["revenue_2026h1"])
gross25=r(d["gross_2025h1"],d["revenue_2025h1"])
sell26=r(d["sell_2026h1"],d["revenue_2026h1"])
sell25=r(d["sell_2025h1"],d["revenue_2025h1"])
print(f"Gross margin H1 2026: {gross26:.2f}%; H1 2025: {gross25:.2f}%")
print(f"Selling expense / revenue H1 2026: {sell26:.2f}%; H1 2025: {sell25:.2f}%; change: {sell26-sell25:.2f}pp")
print(f"R&D / revenue H1 2026: {r(d['rnd_2026h1'],d['revenue_2026h1']):.2f}%")
print(f"Operating cash / net profit H1 2026: {r(d['cashflow_2026h1'],d['net_2026h1']):.2f}%")
assert isclose(sell26-sell25,9.41,abs_tol=0.01)
assert isclose(gross26,79.46,abs_tol=0.01)
assert isclose(r(d["cashflow_2026h1"],d["net_2026h1"]),84.05,abs_tol=0.01)
print("PASS: financial ratio checks")
