from pathlib import Path
import json
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from threading import Thread
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
SHOTS = ROOT / "shots"
SHOTS.mkdir(exist_ok=True)
HTML = (ROOT / "index.html").read_text(encoding="utf-8")


def run():
    errors = []
    viewport_results = []
    server = ThreadingHTTPServer(("127.0.0.1", 0), partial(SimpleHTTPRequestHandler, directory=str(ROOT)))
    server_thread = Thread(target=server.serve_forever, daemon=True)
    server_thread.start()
    with sync_playwright() as p:
        launch = {"headless": True, "args": ["--no-sandbox"]}
        if Path("/usr/bin/chromium").exists():
            launch["executable_path"] = "/usr/bin/chromium"
        browser = p.chromium.launch(**launch)
        page = browser.new_page(viewport={"width": 1440, "height": 1000}, device_scale_factor=1)
        page.on("pageerror", lambda error: errors.append(f"pageerror: {error}"))
        page.on("console", lambda message: errors.append(f"console: {message.text}") if message.type == "error" else None)
        page.goto(f"http://127.0.0.1:{server.server_port}/index.html", wait_until="load")
        page.wait_for_selector("#arenaGrid .agent-card", state="attached")
        assert not errors, f"JavaScript errors during initial render: {errors}"
        page.wait_for_function("Array.from(document.querySelectorAll('#arenaGrid .agent-card img')).length === 6 && Array.from(document.querySelectorAll('#arenaGrid .agent-card img')).every(img => img.complete && img.naturalWidth > 0)")
        assert page.title().startswith("AI ARENA / FINANCE RESEARCH LAB")
        assert page.locator("#setupModal").is_visible()
        assert page.locator("#arenaGrid .agent-card").count() == 6
        assert page.locator("#arenaGrid .agent-scene").count() == 6
        assert page.locator("#arenaGrid .agent-card img").evaluate_all("imgs => imgs.every(img => img.complete && img.naturalWidth > 0)")
        page.screenshot(path=str(SHOTS / "setup-modal.png"), full_page=False)
        page.locator("#researchBtn").click()
        assert page.locator("#setupModal").is_hidden()
        assert page.locator("#arenaGrid .agent-card").count() == 6
        assert page.locator("#agentDetail").is_visible()
        assert page.locator("#agentDetail .detail-kpi").count() == 6
        assert page.locator("#agentDetail .detail-room").count() == 1
        assert page.locator("#agentDetail .role-chip").count() == 3
        assert page.locator("#tradeDecision").count() == 1
        page.wait_for_timeout(120)
        page.screenshot(path=str(SHOTS / "desktop-workstation.png"), full_page=False)

        viewports = [
            ("desktop", 1440, 1000),
            ("laptop", 1024, 900),
            ("tablet", 768, 1024),
            ("mobile", 390, 844),
            ("compact", 320, 780),
        ]
        for name, width, height in viewports:
            page.set_viewport_size({"width": width, "height": height})
            page.evaluate("window.scrollTo({top:0,behavior:'instant'})")
            page.wait_for_timeout(180)
            dimensions = page.evaluate("({client:document.documentElement.clientWidth,scroll:document.documentElement.scrollWidth,height:document.documentElement.scrollHeight})")
            overflow = dimensions["scroll"] > dimensions["client"]
            viewport_results.append({"name": name, "width": width, "height": height, **dimensions, "horizontalOverflow": overflow})
            page.screenshot(path=str(SHOTS / f"{name}.png"), full_page=False)

        page.set_viewport_size({"width": 1440, "height": 1000})
        page.locator('.agent-card[data-id="quant"]').click()
        assert page.locator("#detailName").inner_text() == "量化派"
        page.locator("#agentWorkspace").evaluate("(el) => window.scrollTo({top: el.getBoundingClientRect().top + window.scrollY - 120, behavior: 'instant'})")
        page.wait_for_timeout(160)
        page.screenshot(path=str(SHOTS / "selected-agent-workspace.png"), full_page=False)

        page.locator("#nextBtn").click()
        assert page.locator("#runDay").inner_text() == "DAY 001 / 090"
        page.wait_for_timeout(140)
        page.locator("#market").evaluate("(el) => window.scrollTo({top: el.getBoundingClientRect().top + window.scrollY - 80, behavior: 'instant'})")
        page.screenshot(path=str(SHOTS / "market-and-agent-cards.png"), full_page=False)

        page.set_viewport_size({"width": 390, "height": 844})
        page.locator("#agents").evaluate("(el) => window.scrollTo({top: el.getBoundingClientRect().top + window.scrollY - 60, behavior: 'instant'})")
        page.wait_for_timeout(160)
        page.screenshot(path=str(SHOTS / "agent-cards-mobile.png"), full_page=False)

        report = {
            "title": page.title(),
            "viewportChecks": viewport_results,
            "agents": 6,
            "independentPortfolios": 6,
            "avatarSlots": page.locator("#arenaGrid .agent-card img[data-image-src]").count(),
            "portraitAssetsLoaded": page.locator("#arenaGrid .agent-card img").evaluate_all("imgs => imgs.every(img => img.complete && img.naturalWidth > 0)"),
            "researchRoomScenes": page.locator("#arenaGrid .agent-scene").count(),
            "roleChips": page.locator("#agentDetail .role-chip").count(),
            "selectedAgent": page.locator("#detailName").inner_text(),
            "pageErrors": errors,
            "result": "PASS" if not errors and not any(v["horizontalOverflow"] for v in viewport_results) else "FAIL",
            "screenshots": sorted(p.name for p in SHOTS.glob("*.png")),
        }
        (SHOTS / "report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
        browser.close()
    server.shutdown()
    server.server_close()
    server_thread.join(timeout=2)

    if errors:
        raise AssertionError("Browser errors: " + " | ".join(errors))
    overflows = [v for v in viewport_results if v["horizontalOverflow"]]
    if overflows:
        raise AssertionError(f"Horizontal overflow: {overflows}")
    print("PASS: unified Agent workstation screenshots at 1440/1024/768/390/320px; no horizontal overflow or browser errors")


if __name__ == "__main__":
    run()
