from pathlib import Path
import os
from playwright.sync_api import sync_playwright

ROOT=Path(__file__).resolve().parents[1]
URL=(ROOT/'index.html').as_uri()

def run():
    errors=[]
    with sync_playwright() as p:
        browser=p.chromium.launch(executable_path='/usr/bin/chromium',headless=True,args=['--no-sandbox'])
        page=browser.new_page(viewport={'width':1440,'height':1000},device_scale_factor=1)
        page.on('pageerror',lambda e: errors.append(str(e)))
        page.on('console',lambda msg: errors.append(msg.text) if msg.type=='error' else None)
        page.set_content((ROOT/( 'packed-index.html' if os.getenv('PACKED') else 'index.html')).read_text(encoding='utf-8'),wait_until='load')
        page.wait_for_selector('.pod')
        assert page.title().startswith('AI ARENA / CAPITAL THEATER')
        assert page.locator('.pod').count()==4
        assert page.locator('#totalPnl').inner_text() == '+$0'
        page.locator('#ticker').fill('Acme Robotics / ACME')
        assert 'Acme Robotics' in page.locator('#matchSubject').inner_text()
        page.locator('#rules').click()
        assert page.locator('#dialog').is_visible()
        page.locator('#close').click()
        page.locator('#next').click()
        assert '01 / 06' in page.locator('#roundLabel').inner_text()
        assert page.locator('.bill').count()>0
        assert page.locator('.pod.loss').count()>0
        assert page.locator('.pod.gain').count()>0
        page.locator('#scrub').fill('0')
        assert page.locator('#totalPnl').inner_text()=='+$0'
        page.locator('#start').click()
        assert page.locator('#liveStatus').inner_text()=='LIVE'
        page.locator('#pause').click()
        assert page.locator('#liveStatus').inner_text()=='PAUSED'
        page.locator('#pause').click()
        assert page.locator('#liveStatus').inner_text()=='LIVE'
        page.locator('#finish').click()
        assert page.locator('#liveStatus').inner_text()=='SETTLED'
        assert 'CHAMPION' in page.locator('#winnerTag').inner_text()
        assert page.locator('.pod.winner').count()==1
        assert page.locator('#standing .standing-row').count()==4
        assert '+10.60%' in page.locator('#standing').inner_text()
        assert '+1059.57%' not in page.locator('#standing').inner_text()
        page.screenshot(path=str(ROOT/'desktop.png'),full_page=True)
        page.locator('#scrub').fill('3')
        assert '03 / 06' in page.locator('#roundLabel').inner_text()
        page.locator('#scrub').fill('6')
        assert page.locator('#liveStatus').inner_text()=='SETTLED'
        for width in [1024,768,390,320]:
            page.set_viewport_size({'width':width,'height':844})
            page.wait_for_timeout(60)
            overflow=page.evaluate('document.documentElement.scrollWidth > document.documentElement.clientWidth')
            assert not overflow,f'Horizontal overflow at {width}px: '+str(page.evaluate('document.documentElement.scrollWidth'))
        page.screenshot(path=str(ROOT/'mobile.png'),full_page=True)
        assert not errors,errors
        browser.close()
    print('PASS: interactive, P&L direction, pause/resume, scrub/replay, finish, 4 agents, rules, responsive and no browser errors')

if __name__=='__main__':run()