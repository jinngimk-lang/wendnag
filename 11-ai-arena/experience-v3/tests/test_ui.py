from pathlib import Path
import json
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
        assert page.locator("#setupModal").is_visible()
        assert page.locator("#simulation").is_visible()
        assert page.locator("#arenaGrid .agent-card").count() == 6
        assert page.locator("#arenaGrid .agent-card").evaluate_all("els => new Set(els.map(e => e.dataset.id)).size") == 6
        assert page.locator("#arenaGrid .agent-card img[data-image-src]").count() == 6
        assert page.locator("#arenaGrid .agent-card img").evaluate_all("imgs => imgs.every(img => img.getAttribute('src') ? (img.complete && img.naturalWidth > 0) : getComputedStyle(img).display === 'none')")
        assert page.locator(".vault").count() == 0
        assert page.locator("#cashflowLayer").count() == 0

        page.locator("#closeSetup").click()
        assert page.locator("#setupModal").is_hidden()
        page.locator("#rulesOpen").click()
        assert page.locator("#rulesModal").is_visible()
        assert "不存在" in page.locator("#rulesModal").text_content()
        page.locator("#closeRules").click()
        page.locator("#newRunBtn").click()
        assert page.locator("#setupModal").is_visible()

        page.locator("#company").fill("ACME Robotics / ACME")
        page.locator("#days").evaluate("(el) => { el.value = '60'; el.dispatchEvent(new Event('input', {bubbles:true})); }")
        assert page.locator("#daysOut").inner_text() == "60 天"
        page.locator("#capital").select_option("250000")
        page.locator("#riskMode").select_option("conservative")
        page.locator("#researchBtn").click()

        assert page.locator("#setupModal").is_hidden()
        assert "RESEARCH COMPLETE" in page.locator("#researchStatus").inner_text()
        assert page.locator("#arenaGrid .agent-card").count() == 6
        card_rects = page.locator("#arenaGrid .agent-card").evaluate_all("els => els.map(e => { const r=e.getBoundingClientRect(); return {x:r.x,y:r.y,w:r.width,h:r.height}; })")
        for i, a in enumerate(card_rects):
            for b in card_rects[i + 1:]:
                overlaps = a["x"] < b["x"] + b["w"] and a["x"] + a["w"] > b["x"] and a["y"] < b["y"] + b["h"] and a["y"] + a["h"] > b["y"]
                assert not overlaps, f"Agent cards overlap: {a} / {b}"
        assert page.locator("#agentDetail .detail-kpi").count() == 6
        assert page.locator("#detailName").inner_text() == "价值派"
        assert page.locator("#detailEquity").inner_text() == "$250,000"
        assert page.locator("#runSubject").inner_text() == "ACME Robotics / ACME"
        assert page.locator("#runDay").inner_text() == "DAY 000 / 060"
        assert page.locator("#ledgerBody tr").count() == 1
        assert page.locator("#eventTotal").inner_text() == "0 EVENTS SEEN"

        # Selecting an Agent changes the detailed workspace without changing any other account.
        page.locator('.agent-card[data-id="quant"]').click()
        assert page.locator("#detailName").inner_text() == "量化派"
        assert "QUANT" in page.locator("#agentDetail").inner_text()
        page.locator('.agent-card[data-id="value"]').click()
        assert page.locator("#detailName").inner_text() == "价值派"

        # One shared market day produces six separate decisions and six independent account cards.
        page.locator("#nextBtn").click()
        assert page.locator("#runDay").inner_text() == "DAY 001 / 060"
        assert page.locator("#decisionCount").inner_text() == "6"
        assert page.locator("#ledgerBody tr").count() == 6
        assert page.locator("#totalPnl").evaluate("el => ['rgb(112, 223, 173)', 'rgb(255, 136, 126)'].includes(getComputedStyle(el).color)")
        assert page.locator("#macroNow").inner_text() != "0.00" or page.locator("#sectorNow").inner_text() != "0.00"
        assert page.locator("#detailCash").inner_text().startswith("$")
        assert page.locator("#detailShares").inner_text() != "—"
        assert page.locator("#detailLastAction").inner_text()
        assert "共享资金池" in page.locator("#totalReturn").inner_text() or "独立账户" in page.locator("#totalReturn").inner_text()
        assert page.locator("#arenaGrid .agent-card").count() == 6
        assert page.locator(".vault").count() == 0
        assert page.locator("#cashflowLayer").count() == 0
        assert "Agent 之间的资金转账" in page.locator("#rulesModal").inner_text()

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

        # Replay hides future points and keeps every account's ledger isolated.
        page.locator("#scrub").evaluate("(el) => { el.value = '20'; el.dispatchEvent(new Event('input', {bubbles:true})); }")
        assert page.locator("#runDay").inner_text() == "DAY 020 / 060"
        assert page.locator("#ledgerSummary").inner_text().startswith("已记录 120 条")
        chart_path = page.locator("#equityChart path").first.get_attribute("d")
        assert chart_path.count("L") == 20
        page.locator("#agentFilter").select_option("value")
        assert page.locator("#ledgerBody tr").count() == 20
        page.locator("#actionFilter").select_option("BUY")
        assert "买入" in page.locator("#ledgerBody").inner_text() or "当前筛选" in page.locator("#ledgerBody").inner_text()
        page.locator("#agentFilter").select_option("all")
        page.locator("#actionFilter").select_option("all")
        page.locator("#dayFilter").select_option("late")
        assert page.locator("#ledgerSummary").inner_text().startswith("已记录 ")
        page.locator("#dayFilter").select_option("all")

        # Pause, resume, reset and export the complete experiment.
        page.locator("#scrub").evaluate("(el) => { el.value = '0'; el.dispatchEvent(new Event('input', {bubbles:true})); }")
        page.locator("#playBtn").click()
        assert page.locator("#runState").inner_text() == "LIVE"
        page.wait_for_timeout(600)
        page.locator("#pauseBtn").click()
        assert page.locator("#runState").inner_text() == "PAUSED"
        page.locator("#resetBtn").click()
        assert page.locator("#runDay").inner_text() == "DAY 000 / 060"
        page.locator("#finishBtn").click()
        with page.expect_download() as dl_info:
            page.locator("#exportBtn").click()
        download = dl_info.value
        target = Path(tempfile.gettempdir()) / download.suggested_filename
        download.save_as(str(target))
        payload = json.loads(target.read_text(encoding="utf-8"))
        assert payload["dataMode"] == "SYNTHETIC_DEMO_ONLY"
        assert payload["schema"] == "ai-arena-run-v0.4.0"
        assert payload["versions"]["simulator"] == "paper-sim-v0.4.0"
        assert payload["evidencePack"]["sourceCount"] == 0 and payload["evidencePack"]["companyLabelOnly"]
        assert payload["benchmark"]["shares"] > 0 and payload["benchmark"]["initialFee"] > 0
        assert abs(payload["benchmark"]["finalValue"] - payload["benchmark"]["path"][-1]) < 1e-8
        assert payload["inputs"]["days"] == 60
        assert len(payload["research"]) == 6
        assert len(payload["market"]) == 61
        assert len(payload["operations"]) == 360
        assert {x["agentId"] for x in payload["operations"]} == {"value", "growth", "trend", "quant", "sentiment", "macro"}
        assert len(payload["results"]) == 6
        for result in payload["results"]:
            assert len(result["equityPath"]) == 61
            assert len(result["cashPath"]) == 61
            assert len(result["sharesPath"]) == 61
            assert len(result["weightPath"]) == 61
            assert len(result["targetWeightPath"]) == 61
            for day_index, actual_weight in enumerate(result["weightPath"]):
                equity = result["equityPath"][day_index]
                expected_weight = result["sharesPath"][day_index] * payload["market"][day_index]["price"] / equity if equity else 0
                assert abs(actual_weight - expected_weight) < 1e-8
            assert max(result["targetWeightPath"]) <= cap + 1e-9
            expected_score = result["totalReturn"] - .48 * result["maxDrawdown"] - .20 * result["dailyVolatilityPct"]
            assert abs(result["score"] - expected_score) < 1e-8
        assert all("fillPrice" in x and "slippageCost" in x and "cashBalance" in x and "sharesHeld" in x for x in payload["operations"])
        assert all("marketReturnPct" in x and "macro" in x and "sentimentRaw" in x and "sector" in x and "volatility" in x and "eventKind" in x and "eventDescription" in x for x in payload["operations"])
        assert all(x["volatility"] >= 0 and 0 <= x["sentiment"] <= 100 for x in payload["operations"])
        cap = {"conservative": .35, "balanced": .60, "aggressive": .85}[payload["inputs"]["risk"]]
        assert all(x["weight"] <= cap + 1e-9 for x in payload["operations"])
        assert all(x["cashBalance"] >= -0.01 for x in payload["operations"])
        assert len(set(x["sentiment"] for x in payload["market"])) > 8
        target.unlink(missing_ok=True)

        # A new experiment is deterministic and can use a different duration.
        page.locator("#newRunBtn").click()
        page.locator("#days").evaluate("(el) => { el.value = '30'; el.dispatchEvent(new Event('input', {bubbles:true})); }")
        page.locator("#researchBtn").click()
        page.locator("#finishBtn").click()
        first_total = page.locator("#totalPnl").inner_text()
        page.locator("#newRunBtn").click()
        page.locator("#researchBtn").click()
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
        page.locator("#agentWorkspace").evaluate("(el) => el.scrollIntoView({behavior:'instant',block:'start'})")
        page.wait_for_timeout(100)
        page.screenshot(path=str(ROOT / "agent-workspace.png"))
        page.set_viewport_size({"width": 390, "height": 844})
        page.evaluate("document.documentElement.style.scrollBehavior='auto';document.body.style.scrollBehavior='auto';document.scrollingElement.scrollTop=0;window.scrollTo({top:0,behavior:'instant'})")
        page.wait_for_timeout(100)
        assert page.evaluate("window.scrollY") == 0
        page.screenshot(path=str(ROOT / "mobile.png"))
        page.set_viewport_size({"width": 1440, "height": 1000})
        page.locator("#newRunBtn").click()
        page.locator("#days").evaluate("(el) => { el.value = '252'; el.dispatchEvent(new Event('input', {bubbles:true})); }")
        page.locator("#researchBtn").click()
        page.locator("#finishBtn").click()
        assert page.locator("#runDay").inner_text() == "DAY 252 / 252"
        assert page.locator("#ledgerSummary").inner_text().startswith("已记录 1,512 条")
        assert not errors, errors
        browser.close()
    print("PASS: six independent Agent portfolios, shared market path, distinct research/persona cards, per-agent cash/share/equity paths, selected Agent workspace, isolated ledger, replay, export, deterministic rerun, 252-day stress, responsive and no browser errors")


if __name__ == "__main__":
    run()
