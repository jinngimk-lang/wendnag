from pathlib import Path
import json
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
SHOTS = ROOT / "shots"
SHOTS.mkdir(exist_ok=True)
HTML = (ROOT / "index.html").read_text(encoding="utf-8")


def run():
    errors = []
    viewport_results = []
    with sync_playwright() as p:
        launch = {"headless": True, "args": ["--no-sandbox"]}
        if Path("/usr/bin/chromium").exists():
            launch["executable_path"] = "/usr/bin/chromium"
        browser = p.chromium.launch(**launch)
        page = browser.new_page(viewport={"width": 1440, "height": 1000}, device_scale_factor=1)
        page.on("pageerror", lambda error: errors.append(f"pageerror: {error}"))
        page.on("console", lambda message: errors.append(f"console: {message.text}") if message.type == "error" else None)
        page.set_content(HTML, wait_until="load")
        assert page.title().startswith("AI ARENA / FINANCE RESEARCH LAB")

        page.wait_for_timeout(45)
        page.screenshot(path=str(SHOTS / "desktop-early.png"))
        page.wait_for_timeout(900)

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
            page.wait_for_timeout(220)
            dimensions = page.evaluate("({client:document.documentElement.clientWidth,scroll:document.documentElement.scrollWidth,height:document.documentElement.scrollHeight})")
            overflow = dimensions["scroll"] > dimensions["client"]
            viewport_results.append({"name": name, "width": width, "height": height, **dimensions, "horizontalOverflow": overflow})
            page.screenshot(path=str(SHOTS / f"{name}.png"), full_page=False)

        page.set_viewport_size({"width": 1440, "height": 1000})
        page.locator("#company").fill("ACME Robotics / ACME")
        page.locator("#researchBtn").click()
        assert page.locator("#researchGrid .faction").count() == 6
        assert page.locator("#researchGrid .team-row").count() == 18
        page.wait_for_timeout(250)
        page.locator("#researchGrid").evaluate("(el) => window.scrollTo({top: el.getBoundingClientRect().top + window.scrollY - 150, behavior: 'instant'})")
        page.wait_for_timeout(180)
        page.screenshot(path=str(SHOTS / "research-desktop.png"), full_page=False)

        page.locator("#runBtn").click()
        page.locator("#nextBtn").click()
        page.wait_for_timeout(160)
        page.locator("#simulation").screenshot(path=str(SHOTS / "arena-desktop.png"))
        page.set_viewport_size({"width": 390, "height": 844})
        page.locator("#simulation").evaluate("(el) => window.scrollTo({top: el.getBoundingClientRect().top + window.scrollY - 60, behavior: 'instant'})")
        page.wait_for_timeout(180)
        page.screenshot(path=str(SHOTS / "arena-mobile.png"), full_page=False)

        report = {
            "title": page.title(),
            "viewportChecks": viewport_results,
            "factions": 6,
            "roleTemplates": 18,
            "pageErrors": errors,
            "result": "PASS" if not errors and not any(v["horizontalOverflow"] for v in viewport_results) else "FAIL",
            "screenshots": sorted(p.name for p in SHOTS.glob("*.png")),
        }
        (SHOTS / "report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
        browser.close()

    if errors:
        raise AssertionError("Browser errors: " + " | ".join(errors))
    overflows = [v for v in viewport_results if v["horizontalOverflow"]]
    if overflows:
        raise AssertionError(f"Horizontal overflow: {overflows}")
    print("PASS: visual screenshots at 1440/1024/768/390/320px; no horizontal overflow or browser errors")


if __name__ == "__main__":
    run()
