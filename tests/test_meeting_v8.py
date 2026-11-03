"""AragonTeam v8: meeting-flow UI smoke tests, frontend-only."""
from pathlib import Path
from playwright.sync_api import sync_playwright
import json,sys

HTML=(Path(__file__).resolve().parents[1]/"index.html").read_text(encoding="utf-8")
results=[]
with sync_playwright() as pw:
  browser=pw.chromium.launch(headless=True,executable_path="/usr/bin/chromium",
      args=["--no-sandbox","--disable-dev-shm-usage"])
  for width in (320,390,768,1024,1440,1664):
    pg=browser.new_page(viewport={"width":width,"height":900})
    errors=[]
    pg.on("pageerror",lambda exc: errors.append(str(exc)))
    pg.set_default_timeout(7000)
    step="load"
    try:
      pg.set_content(HTML,wait_until="domcontentloaded",timeout=30000)
      step="group navigation"
      pg.locator('[data-area="智能体"]').click()
      btn=pg.locator('#subnav [data-sub="群聊"]')
      if not btn.is_visible():
        btn=pg.locator('[data-ux5="nav"]').filter(has_text="群聊")
      btn.first.click()
      step="meeting preparation and cancellation"
      pg.locator('[data-v7="open-meeting"]').first.click()
      assert pg.locator("#v8SetupForm").count()==1
      assert pg.locator(".v8-meeting").count()==0
      pg.locator('[data-v8="cancel-prejoin"]').first.click()
      assert pg.locator("#v8SetupForm").count()==0
      step="start"
      pg.locator('[data-v7="open-meeting"]').first.click()
      pg.locator("#v8MeetingTitle").fill("版本迭代评审")
      pg.locator('#v8SetupForm button[type="submit"]').click()
      assert pg.locator(".v8-meeting").is_visible()
      assert pg.locator(".v8-person-card.is-joined").count()==1
      assert pg.locator(".v8-waiting").count()==1
      step="participants and extra invitation"
      pg.locator('.v8-waiting [data-v8="switch-people"]').click()
      pg.locator('[data-v8="join-person"]').first.click()
      assert pg.locator(".v8-person-card.is-joined").count()==2
      pg.locator('[data-v8="invite-open"]').first.click()
      assert pg.locator("#v8InviteForm").count()==1
      assert pg.locator("#ux6MembersForm").count()==0
      choices=pg.locator('#v8InviteForm input[name="person"]')
      if choices.count():
        choices.first.check()
        pg.locator('#v8InviteForm button[type="submit"]').click()
      else:
        pg.locator('[data-v8="cancel-invite"]').click()
      step="minimize and restore"
      pg.locator('[data-v8="minimize"]').click()
      assert pg.locator(".v8-room-live").count()==1
      pg.locator('[data-v7="open-meeting"]').first.click()
      assert pg.locator(".v8-meeting").is_visible()
      step="meeting notes and exit"
      pg.locator('[data-v7="meeting-tab"][data-value="minutes"]').click()
      pg.locator('[data-v7="meeting-action"]').first.check()
      assert pg.locator('[data-v7="meeting-action"]').first.is_checked()
      pg.locator('[data-v8="ask-end"]').click()
      pg.locator('[data-v8="cancel-end"]').click()
      assert pg.locator('[data-v8="confirm-end"]').count()==0
      pg.locator('[data-v8="ask-end"]').click()
      pg.locator('[data-v8="confirm-end"]').click()
      assert pg.locator(".v8-meeting").count()==0
      assert pg.locator(".v8-room-live").count()==0
      step="project regression"
      pg.locator('[data-area="项目"]').click()
      assert pg.locator(".project-card").count()>=2
      over=pg.evaluate("document.documentElement.scrollWidth-document.documentElement.clientWidth")
      assert over<4, f"horizontal overflow: {over}"
      assert not errors,errors
      results.append({"width":width,"result":"PASS","overflow":over})
    except Exception as e:
      results.append({"width":width,"result":"FAIL","step":step,
                      "error":str(e)[:400],"javascript_errors":errors})
    finally:
      pg.close()
  browser.close()
print(json.dumps(results,ensure_ascii=False,indent=2))
if any(r["result"]!="PASS" for r in results):
  sys.exit(1)
