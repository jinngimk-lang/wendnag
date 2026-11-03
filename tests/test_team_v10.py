"""AragonTeam v10 member and Agent team creation regression."""
from pathlib import Path
from playwright.sync_api import sync_playwright
import json,sys
html=(Path(__file__).resolve().parents[1]/"index.html").read_text(encoding="utf-8")
results=[]
with sync_playwright() as p:
 b=p.chromium.launch(headless=True,executable_path="/usr/bin/chromium",args=["--no-sandbox","--disable-dev-shm-usage"])
 for width in (320,390,768,1024,1440,1664):
  pg=b.new_page(viewport={"width":width,"height":950})
  pg.set_default_timeout(7000)
  errs=[]
  pg.on("pageerror",lambda e:errs.append(str(e)))
  step="load"
  try:
   pg.set_content(html,wait_until="domcontentloaded")
   pg.locator('[data-area="团队"]').click()
   step="create picker"
   pg.locator("#createBtn").click()
   f=pg.locator("#teamCreateForm")
   assert f.is_visible() and f.locator(".team-picker").count()==2
   assert f.locator('[name="initialMembers"]').count()>30
   assert f.locator('[name="initialAgents"]').count()>=7
   step="search and select humans"
   f.locator("#teamPickerSearch-member").fill("李明")
   assert f.locator('[data-roster-choice="member"]:visible').count()==1
   f.locator('input[name="initialMembers"][value="2"]').check()
   assert f.locator('[data-picker-count="member"]').inner_text()=="已选 1"
   f.locator("#teamPickerSearch-member").fill("")
   step="search and select agents"
   f.locator("#teamPickerSearch-agent").fill("文档")
   assert f.locator('[data-roster-choice="agent"]:visible').count()>=1
   f.locator('input[name="initialAgents"][value="5"]').check()
   assert f.locator('input[name="initialAgents"][value="7"]').is_disabled()
   step="create mixed team"
   f.locator("#newTeamName").fill("回归测试团队"+str(width))
   f.locator('button[type="submit"]').click()
   assert pg.evaluate("teamData.teams[0].memberIds")==[1,2]
   assert pg.evaluate("teamData.teams[0].agentIds")==[5]
   card=pg.locator(".team-card").filter(has_text="回归测试团队"+str(width))
   assert "1 Agent" in card.inner_text()
   step="Agent detail and updates"
   card.locator('[data-team-action="details"]').first.click()
   pg.locator('[data-team-action="detail-tab"][data-tab="agents"]').click()
   assert "文档助手" in pg.locator("#teamDetailPane").inner_text()
   pg.locator('[data-team-action="manage-agents"]').click()
   pg.locator('#teamManageAgentsForm input[name="initialAgents"][value="2"]').check()
   pg.locator('#teamManageAgentsForm button[type="submit"]').click()
   assert sorted(pg.evaluate("teamData.teams[0].agentIds"))==[2,5]
   step="original project regression"
   pg.locator('#modalContainer .close').first.click()
   pg.locator('[data-area="项目"]').click()
   assert pg.locator(".project-card").count()>=2
   over=pg.evaluate("document.documentElement.scrollWidth-document.documentElement.clientWidth")
   assert over<5 and not errs,(over,errs)
   results.append({"width":width,"status":"PASS","overflow":over})
  except Exception as e:
   results.append({"width":width,"status":"FAIL","step":step,"error":str(e)[:480],"jsErrors":errs})
  pg.close()
 b.close()
print(json.dumps(results,ensure_ascii=False,indent=2))
if any(r["status"]!="PASS" for r in results):sys.exit(1)
