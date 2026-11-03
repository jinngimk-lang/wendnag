"""AragonTeam v8: test safety of invitations and displayed text."""
from pathlib import Path
from playwright.sync_api import sync_playwright
import json
HTML=(Path(__file__).resolve().parents[1]/"index.html").read_text(encoding="utf-8")
out=[]
with sync_playwright() as pw:
  browser=pw.chromium.launch(headless=True,executable_path="/usr/bin/chromium",
      args=["--no-sandbox","--disable-dev-shm-usage"])
  for width in (390,1440):
    pg=browser.new_page(viewport={"width":width,"height":900})
    pg.set_default_timeout(7000)
    errs=[]
    pg.on("pageerror",lambda exc:errs.append(str(exc)))
    pg.set_content(HTML,wait_until="domcontentloaded")
    pg.locator('[data-area="智能体"]').click()
    btn=pg.locator('#subnav [data-sub="群聊"]')
    if not btn.is_visible():
      btn=pg.locator('[data-ux5="nav"]').filter(has_text="群聊")
    btn.first.click()
    people_before=pg.evaluate("ux6Channel().people.length+ux6Channel().agents.length")
    pg.locator('[data-v7="open-meeting"]').first.click()
    pg.locator("#v8MeetingTitle").fill("<img src=x onerror=alert(7)>")
    pg.locator('#v8SetupForm input[name="notify"]').uncheck()
    ag=pg.locator('#v8SetupForm input[name="agent"]')
    if ag.count():ag.first.check()
    pg.locator('#v8SetupForm button[type="submit"]').click()
    assert pg.locator(".v8-meeting-headerline img").count()==0
    assert "<img" in pg.locator(".v8-meeting-headerline").inner_text()
    assert pg.locator(".v8-person-card.is-joined").count()==1
    assert pg.locator(".v8-person-row").count()==0
    pg.locator('[data-v8="invite-open"]').first.click()
    pg.locator('#v8InviteForm input[name="person"]').first.check()
    pg.locator('#v8InviteForm button[type="submit"]').click()
    assert pg.evaluate("ux6Channel().people.length+ux6Channel().agents.length")==people_before
    assert pg.locator(".v8-person-card.is-joined").count()==1
    pg.locator('[data-v8="minimize"]').click()
    assert pg.locator(".v8-room-live").count()==1
    pg.locator('[data-v7="open-meeting"]').first.click()
    assert pg.locator(".v8-person-card.is-joined").count()==1
    pg.locator('[data-v8="ask-end"]').click()
    pg.locator('[data-v8="confirm-end"]').click()
    assert pg.evaluate("v8Session===null")
    assert not errs,errs
    out.append({"width":width,"pass":True,"memberCountUnchanged":people_before,
                "javascriptErrors":len(errs)})
    pg.close()
  browser.close()
print(json.dumps(out,ensure_ascii=False,indent=2))
