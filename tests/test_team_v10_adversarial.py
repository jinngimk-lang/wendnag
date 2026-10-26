"""AragonTeam v10: guard default admin, unpublished Agents and unsafe HTML."""
from pathlib import Path
from playwright.sync_api import sync_playwright
import json,sys
html=(Path(__file__).resolve().parents[1]/"index.html").read_text(encoding="utf-8")
results=[]
with sync_playwright() as p:
 b=p.chromium.launch(headless=True,executable_path="/usr/bin/chromium",args=["--no-sandbox","--disable-dev-shm-usage"])
 for width in (390,1440):
  pg=b.new_page(viewport={"width":width,"height":850})
  pg.set_default_timeout(7000)
  errs=[]
  pg.on("pageerror",lambda e:errs.append(str(e)))
  try:
   pg.set_content(html,wait_until="domcontentloaded")
   pg.locator('[data-area="团队"]').click()
   pg.locator("#createBtn").click()
   f=pg.locator("#teamCreateForm")
   f.locator("#newTeamName").fill('测试<img src=x onerror="window.pwned=1">')
   assert f.locator('input[name="initialAgents"]:checked').count()==0
   f.locator("#teamPickerSearch-agent").fill("不存在的 Agent")
   assert f.locator('[data-picker-empty="agent"]').is_visible()
   f.locator("#teamPickerSearch-agent").fill("自定义")
   assert f.locator('input[name="initialAgents"][value="7"]').is_disabled()
   f.locator("button[type=submit]").click()
   assert pg.evaluate("teamData.teams[0].memberIds")==[1]
   assert pg.evaluate("teamData.teams[0].agentIds")==[]
   assert pg.evaluate("window.pwned===undefined")
   card=pg.locator(".team-card").filter(has_text="测试<img").first
   assert card.count()==1 and card.locator("img").count()==0
   card.locator('[data-team-action="details"]').first.click()
   pg.locator('[data-team-action="manage-agents"]').click()
   pg.locator('#teamManageAgentsForm input[value="1"]').check()
   pg.locator('#teamManageAgentsForm button[type="submit"]').click()
   assert pg.evaluate("teamData.teams[0].agentIds")==[1]
   over=pg.evaluate("document.documentElement.scrollWidth-document.documentElement.clientWidth")
   assert over<4 and not errs,(over,errs)
   results.append({"width":width,"status":"PASS"})
  except Exception as e:results.append({"width":width,"status":"FAIL","error":str(e)[:500],"jsErrors":errs})
  pg.close()
 b.close()
print(json.dumps(results,ensure_ascii=False,indent=2))
if any(r["status"]!="PASS" for r in results):sys.exit(1)
