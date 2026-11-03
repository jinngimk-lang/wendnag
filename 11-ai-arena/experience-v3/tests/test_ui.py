from pathlib import Path
import json
import os
import tempfile
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]

def run():
    errors = []
    with sync_playwright() as p:
        launch = {"headless": True, "args": ["--no-sandbox"]}
        if Path("/usr/bin/chromium").exists():
            launch["executable_path"] = "/usr/bin/chromium"
        browser = p.chromium.launch(**launch)
        page = browser.new_page(viewport={"width": 1440, "height": 1000})
        page.on("pageerror", lambda e: errors.append(str(e)))
        page.on("console", lambda m: errors.append(m.text) if m.type == "error" else None)
        page.set_content((ROOT / "index.html").read_text(encoding="utf-8"), wait_until="load")

        assert page.title().startswith("AI ARENA / FINANCE RESEARCH LAB")
        assert page.locator("#research").is_hidden()
        assert page.locator("#simulation").is_hidden()
        page.locator("#rulesOpen").click()
        assert page.locator("#rulesModal").is_visible()
        page.locator("#closeRules").click()
        page.locator("#company").fill("ACME Robotics / ACME")
        page.locator("#days").evaluate("(el) => { el.value = '60'; el.dispatchEvent(new Event('input', {bubbles:true})); }")
        assert page.locator("#daysOut").inner_text() == "60 天"
        page.locator("#capital").select_option("250000")
        page.locator("#riskMode").select_option("conservative")
        page.locator("#researchBtn").click()

        assert page.locator("#research").is_visible()
        assert page.locator("#researchGrid .faction").count() == 6
        assert page.locator("#researchGrid details").count() == 6
        assert page.locator("#researchGrid .team-row").count() == 18
        assert "ACME Robotics" in page.locator("#configSubject").inner_text()
        assert page.locator("#configDays").inner_text() == "60 DAYS"
        assert "合成" in page.locator("#researchGrid").inner_text()
        page.locator("#researchGrid details").evaluate_all("els => els.forEach(el => el.open = true)")
        research_text = page.locator("#researchGrid").inner_text()
        assert "入场触发条件" in research_text and "观点失效条件" in research_text
        assert "合成情景指标" in research_text
        assert page.locator("#debate .debate-col").count() == 3

        page.locator("#runBtn").click()
        assert page.locator("#simulation").is_visible()
        assert page.locator("#runDay").inner_text() == "DAY 000 / 060"
        assert page.locator(".pod").count() == 6
        assert page.locator("#ledger").is_visible()
        assert page.locator("#ledgerBody tr").count() == 1
        assert page.locator("#eventTotal").inner_text() == "0 EVENTS SEEN"
        assert "等待" not in page.locator("#ledgerSummary").inner_text()

        page.locator("#nextBtn").click()
        assert page.locator("#runDay").inner_text() == "DAY 001 / 060"
        assert page.locator("#decisionCount").inner_text() == "6"
        assert page.locator("#ledgerBody tr").count() == 6
        assert "市场" in page.locator("#ledgerBody").inner_text() and "情绪" in page.locator("#ledgerBody").inner_text()
        assert int(page.locator("#eventTotal").inner_text().split()[0]) == page.locator("#eventsList .event").count()
        page.locator("#next5Btn").click()
        assert page.locator("#runDay").inner_text() == "DAY 006 / 060"
        page.locator("#finishBtn").click()
        assert page.locator("#runState").inner_text() == "SETTLED"
        assert page.locator("#runDay").inner_text() == "DAY 060 / 060"
        assert page.locator("#ledgerSummary").inner_text().startswith("已记录 360 条")
        assert page.locator("#standings").inner_text().count("· 日波动") == 6
        assert page.locator("#eventsList .event").count() > 0
        assert page.locator("#factorGrid .factor").count() == 4
        assert page.locator("#equityChart path").count() >= 7
        assert page.locator("#priceNow").inner_text().startswith("$")
        assert page.locator("#scrubLabel").inner_text() == "60 / 60"

        # Replay must update the market state, standings and ledger window.
        page.locator("#scrub").evaluate("(el) => { el.value = '20'; el.dispatchEvent(new Event('input', {bubbles:true})); }")
        assert page.locator("#runDay").inner_text() == "DAY 020 / 060"
        assert page.locator("#ledgerSummary").inner_text().startswith("已记录 120 条")
        chart_path = page.locator("#equityChart path").first.get_attribute("d")
        assert chart_path.count("L") == 20, "Chart must not reveal future simulation points during replay"
        page.locator("#agentFilter").select_option("value")
        assert page.locator("#ledgerBody tr").count() == 20
        page.locator("#actionFilter").select_option("BUY")
        assert "买入" in page.locator("#ledgerBody").inner_text() or "当前筛选" in page.locator("#ledgerBody").inner_text()
        page.locator("#agentFilter").select_option("all")
        page.locator("#actionFilter").select_option("all")
        page.locator("#dayFilter").select_option("late")
        assert page.locator("#ledgerSummary").inner_text().startswith("已记录 ")
        page.locator("#dayFilter").select_option("all")

        # Pause/resume and replay controls.
        page.locator("#scrub").evaluate("(el) => { el.value = '0'; el.dispatchEvent(new Event('input', {bubbles:true})); }")
        page.locator("#playBtn").click()
        assert page.locator("#runState").inner_text() == "LIVE"
        page.wait_for_timeout(600)
        page.locator("#pauseBtn").click()
        assert page.locator("#runState").inner_text() == "PAUSED"
        page.locator("#resetBtn").click()
        assert page.locator("#runDay").inner_text() == "DAY 000 / 060"

        # JSON export contains inputs, six reports, daily market path and 6*days ledger records.
        page.locator("#finishBtn").click()
        with page.expect_download() as dl_info:
            page.locator("#exportBtn").click()
        download = dl_info.value
        target = Path(tempfile.gettempdir()) / download.suggested_filename
        download.save_as(str(target))
        payload = json.loads(target.read_text(encoding="utf-8"))
        assert payload["dataMode"] == "SYNTHETIC_DEMO_ONLY"
        assert payload["schema"] == "ai-arena-run-v0.3.1"
        assert payload["evidencePack"]["sourceCount"] == 0 and payload["evidencePack"]["companyLabelOnly"]
        assert payload["benchmark"]["shares"] > 0 and payload["benchmark"]["initialFee"] > 0
        assert abs(payload["benchmark"]["finalValue"] - payload["benchmark"]["path"][-1]) < 1e-8
        assert payload["inputs"]["days"] == 60
        assert len(payload["research"]) == 6
        assert len(payload["market"]) == 61
        assert len(payload["operations"]) == 360
        assert int(page.locator("#eventTotal").inner_text().split()[0]) == len(payload["events"])
        page.locator("#scrub").evaluate("(el) => { el.value = '20'; el.dispatchEvent(new Event('input', {bubbles:true})); }")
        assert int(page.locator("#eventTotal").inner_text().split()[0]) == sum(1 for e in payload["events"] if e["day"] <= 20)
        page.locator("#scrub").evaluate("(el) => { el.value = '0'; el.dispatchEvent(new Event('input', {bubbles:true})); }")
        for result in payload["results"]:
            expected_score = result["totalReturn"] - .48 * result["maxDrawdown"] - .20 * result["dailyVolatilityPct"]
            assert abs(result["score"] - expected_score) < 1e-8
        assert {x["action"] for x in payload["operations"]}.issubset({"BUY", "SELL", "HOLD"})
        assert all("fillPrice" in x and "slippageCost" in x and "cashBalance" in x and "sharesHeld" in x for x in payload["operations"])
        assert all("marketReturnPct" in x and "macro" in x and "sentimentRaw" in x and "sector" in x and "volatility" in x and "eventKind" in x and "eventDescription" in x for x in payload["operations"])
        assert all(x["volatility"] >= 0 and 0 <= x["sentiment"] <= 100 for x in payload["operations"])
        cap = {"conservative": .35, "balanced": .60, "aggressive": .85}[payload["inputs"]["risk"]]
        assert all(x["weight"] <= cap + 1e-9 for x in payload["operations"])
        assert all(x["cashBalance"] >= -0.01 for x in payload["operations"])
        sentiment_path = [x["sentiment"] for x in payload["market"]]
        assert len(set(sentiment_path)) > 8
        assert len({round(x["macro"], 3) for x in payload["operations"]}) > 8
        assert len({round(x["sector"], 3) for x in payload["operations"]}) > 8
        sentiment_weights = {round(x["weight"], 3) for x in payload["operations"] if x["agentId"] == "sentiment"}
        assert len(sentiment_weights) > 3
        target.unlink(missing_ok=True)

        # New duration and deterministic rerun.
        page.locator("#days").evaluate("(el) => { el.value = '30'; el.dispatchEvent(new Event('input', {bubbles:true})); }")
        page.locator("#researchBtn").click()
        page.locator("#runBtn").click()
        page.locator("#finishBtn").click()
        first_total = page.locator("#totalPnl").inner_text()
        page.locator("#researchBtn").click()
        page.locator("#runBtn").click()
        page.locator("#finishBtn").click()
        assert page.locator("#totalPnl").inner_text() == first_total
        assert page.locator("#ledgerSummary").inner_text().startswith("已记录 180 条")

        for width in [1024, 768, 390, 320]:
            page.set_viewport_size({"width": width, "height": 844})
            page.wait_for_timeout(80)
            overflow = page.evaluate("document.documentElement.scrollWidth > document.documentElement.clientWidth")
            assert not overflow, f"Horizontal overflow at {width}px"
        page.set_viewport_size({"width": 1440, "height": 1000})
        page.evaluate("document.documentElement.style.scrollBehavior='auto';document.body.style.scrollBehavior='auto';document.scrollingElement.scrollTop=0;window.scrollTo({top:0,behavior:'instant'})")
        page.wait_for_timeout(100)
        assert page.evaluate("window.scrollY") == 0
        page.screenshot(path=str(ROOT / "desktop.png"))
        page.locator("#simulation").evaluate("(el) => el.scrollIntoView({behavior:'instant',block:'start'})")
        page.wait_for_timeout(100)
        page.screenshot(path=str(ROOT / "arena.png"))
        page.set_viewport_size({"width": 390, "height": 844})
        page.evaluate("document.documentElement.style.scrollBehavior='auto';document.body.style.scrollBehavior='auto';document.scrollingElement.scrollTop=0;window.scrollTo({top:0,behavior:'instant'})")
        page.wait_for_timeout(100)
        assert page.evaluate("window.scrollY") == 0
        page.screenshot(path=str(ROOT / "mobile.png"))
        page.set_viewport_size({"width": 1440, "height": 1000})
        page.locator("#days").evaluate("(el) => { el.value = '252'; el.dispatchEvent(new Event('input', {bubbles:true})); }")
        page.locator("#researchBtn").click()
        page.locator("#runBtn").click()
        page.locator("#finishBtn").click()
        assert page.locator("#runDay").inner_text() == "DAY 252 / 252"
        assert page.locator("#ledgerSummary").inner_text().startswith("已记录 1,512 条")
        assert not errors, errors
        browser.close()
    print("PASS: 6-faction research, triggers/invalidation, 18 role templates, configurable duration, shared market path, per-decision factor snapshots, visible event replay, benchmark fee accounting, 6x daily ledger, filters, export, deterministic rerun, responsive and no browser errors")

if __name__ == "__main__":
    run()