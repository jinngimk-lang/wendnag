"""Chromium smoke regression for the offline AragonTeam team prototype.
Install: pip install playwright && playwright install chromium
Run: python tests/team_smoke.py
Uses set_content to work inside browser environments that block localhost navigation.
"""
from pathlib import Path
from shutil import which
from playwright.sync_api import sync_playwright

HTML = Path(__file__).resolve().parents[1].joinpath('index.html').read_text(encoding='utf-8')
with sync_playwright() as api:
    browser_bin = which('chromium') or which('google-chrome')
    options = {'headless': True}
    if browser_bin:
        options['executable_path'] = browser_bin
    browser = api.chromium.launch(**options)
    for width in [320, 390, 768, 1024, 1440, 1664]:
        page = browser.new_page(viewport={'width': width, 'height': 900})
        errors = []
        page.on('pageerror', lambda e: errors.append(str(e)))
        page.set_content(HTML)
        assert page.locator('.project-card').count() == 2
        page.locator('[data-area="团队"]').click()
        assert page.locator('.team-stat-value').all_inner_texts() == ['8','42','18','6']
        assert page.evaluate('document.documentElement.scrollWidth <= innerWidth + 1'), f'Overflow at {width}px'
        page.locator('#teamQuery').fill('Research')
        assert page.locator('.team-card').count() == 1
        page.locator('[data-team-action="clear-search"]').click()
        page.locator('[data-team-view="list"]').click()
        assert page.locator('.team-plain-table tbody tr').count() == 8
        page.locator('[data-team-view="cards"]').click()
        page.locator('#createBtn').click()
        page.locator('#newTeamName').fill('用户体验测试团队')
        page.locator('#teamCreateForm button[type="submit"]').click()
        assert page.locator('.team-stat-value').first.inner_text() == '9'
        page.locator('#subnav [data-sub="成员管理"]').click() if width > 700 else page.locator('[data-team-nav="成员管理"]').first.click()
        assert page.locator('.team-plain-table tbody tr').count() == 42
        assert not errors, errors
        page.close()
    browser.close()
print('PASS: six widths; team search, view switch, creation, members; original project regression')
