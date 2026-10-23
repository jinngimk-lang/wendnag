"""Front-end-only Chromium smoke test: pip install playwright; install Chromium."""
from pathlib import Path
import shutil
from playwright.sync_api import sync_playwright

html = (Path(__file__).resolve().parents[1] / 'index.html').read_text()

def navigate(page, name):
    desktop = page.locator('#subnav').get_by_role('button', name=name)
    if desktop.count() and desktop.is_visible():
        desktop.click()
    else:
        page.locator('[data-ux5="nav"]').filter(has_text=name).first.click()

with sync_playwright() as playwright:
    browser = playwright.chromium.launch(headless=True, **({"executable_path": shutil.which("chromium")} if shutil.which("chromium") else {}))
    for width in (320, 390, 768, 1024, 1440, 1664):
        page = browser.new_page(viewport={'width': width, 'height': 900})
        errors = []
        page.on('pageerror', lambda error: errors.append(str(error)))
        page.set_content(html)
        page.locator('[data-area="智能体"]').click()
        navigate(page, '群聊')
        page.locator('#ux6Message').fill('<b>研发测试</b>')
        page.locator('#ux6ChatForm [type="submit"]').click()
        assert page.locator('.ux6-chat-bubble').last.inner_text() == '<b>研发测试</b>'
        assert page.locator('.ux6-chat-bubble b').count() == 0
        page.locator('.ux6-chat-actions [data-ux6="make-task"]').last.click()
        page.locator('#ux6TaskForm [type="submit"]').click()
        assert page.locator('#pageTitle').inner_text() == '需求看板'
        page.locator('[data-area="智能体"]').click()
        navigate(page, '模板中心')
        page.locator('[data-ux6="catalog-tab"][data-value="skill"]').click()
        page.locator('#search').fill('代码审查')
        assert page.locator('.ux6-catalog-card').count() == 1
        assert page.locator('#ux6CatalogSearch').input_value() == '代码审查'
        page.locator('[data-area="项目"]').click()
        assert page.locator('#subnav button').count() == 7
        assert not page.evaluate('document.documentElement.scrollWidth > innerWidth + 2')
        assert not errors, errors
        page.close()
        print(f'{width}px: PASS')
    browser.close()
