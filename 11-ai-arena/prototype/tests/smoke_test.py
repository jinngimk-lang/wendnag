from pathlib import Path
import json
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]

def main():
    errors = []
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, args=["--no-sandbox"])
        page = browser.new_page(viewport={"width": 1440, "height": 1100})
        page.on("pageerror", lambda error: errors.append(str(error)))
        page.on("console", lambda message: errors.append(message.text) if message.type == "error" else None)

        html = (ROOT / "index.html").read_text(encoding="utf-8")
        html = html.replace("<head>", "<head><base href='http://127.0.0.1:4173/'>")
        assets = {
            name: (ROOT / name).read_text(encoding="ascii")
            for name in ("shell.html.gz.b64", "styles.css.gz.b64", "app.js.gz.b64")
        }
        for name, body in assets.items():
            page.route(f"**/{name}", lambda route, body=body: route.fulfill(
                status=200, body=body, headers={"Access-Control-Allow-Origin": "*"}
            ))

        page.set_content(html, wait_until="load")
        page.wait_for_function("document.querySelectorAll('#leaderboardRows .rank-row').length === 6")
        assert page.title() == "AI Arena — Think. Compete. Simulate."
        assert not page.locator("#resultBanner").is_visible()
        assert page.locator("#agentGrid .agent-card").count() == 6
        page.screenshot(path=str(ROOT / "screenshots/finance-desktop.png"), full_page=True)

        page.locator("#subjectInput").fill("Acme Robotics / ACME")
        assert "Acme Robotics" in page.locator("#matchName").inner_text()
        page.locator("#subjectInput").fill("NVIDIA / NVDA")
        page.locator("#rulesButton").click()
        assert page.locator("#rulesDialog").is_visible()
        page.locator("#rulesDialog .modal-close").click()

        page.locator("#startButton").click()
        page.wait_for_timeout(200)
        assert page.locator("#matchState").inner_text() == "LIVE"
        page.locator("#pauseButton").click()
        assert "继续" in page.locator("#pauseButton").inner_text()
        page.locator("#pauseButton").click()
        page.locator("#fastForwardButton").click()
        assert page.locator("#resultBanner").is_visible()
        assert page.locator("#eventCount").inner_text() == "07 EVENTS"
        page.locator("#reportButton").click()
        assert page.locator("#reportDialog").is_visible()
        page.locator("#reportDialog .modal-close").click()
        page.locator("#agentGrid .agent-card").first.click()
        assert page.locator("#detailDialog").is_visible()
        page.locator("#detailDialog .modal-close").click()

        page.locator('.mode-tab[data-mode="marketing"]').click()
        assert page.locator(".network-field").is_visible()
        assert page.locator(".platform-card").count() == 4
        page.locator("#startButton").click()
        page.wait_for_timeout(100)
        page.locator("#fastForwardButton").click()
        assert "创作者派" in page.locator("#resultHeadline").inner_text()
        page.screenshot(path=str(ROOT / "screenshots/marketing-desktop.png"), full_page=True)

        page.locator('.mode-tab[data-mode="life"]').click()
        assert page.locator(".life-path").count() == 3
        page.locator("#startButton").click()
        page.wait_for_timeout(100)
        page.locator("#fastForwardButton").click()
        assert "不代表唯一" in page.locator("#resultSubline").inner_text()
        page.screenshot(path=str(ROOT / "screenshots/life-desktop.png"), full_page=True)

        page.locator('.mode-tab[data-mode="finance"]').click()
        for width in (1024, 768, 390):
            page.set_viewport_size({"width": width, "height": 844})
            page.wait_for_timeout(80)
            overflow = page.evaluate("document.documentElement.scrollWidth > document.documentElement.clientWidth")
            assert not overflow, f"Layout has horizontal overflow at {width}px"
        page.locator("#toast").evaluate("el => { el.classList.remove('visible'); el.style.display = 'none'; }")
        page.screenshot(path=str(ROOT / "screenshots/finance-mobile.png"), full_page=True)
        assert not errors, "Browser errors: " + " | ".join(errors)
        browser.close()

    print("PASS: initial render, subject input, rules, three arenas, six Agents, live controls, results, report, Agent detail, responsive widths, no browser errors")

if __name__ == "__main__":
    main()
