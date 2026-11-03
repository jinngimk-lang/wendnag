# AragonTeam UI v5 — Frontend-only review anchor

Date: 2026-10-22. Target `jinngimk-lang/wendnag` branch `jinngimk-lang-AT`; review entrypoint `index.html`. This deliverable is **interactive UI only**: no backend work, no authentication integration, no real AI execution, no real Git/PR/CI/token billing, no outbound invitations, and no claims of a production deployment.

## User intent and constraints

- Preserve the project's **seven existing secondary menu items**: 项目管理 / 需求看板 / BUG看板 / 文档 / 代码仓 / 建议 / 版本. Do not add more project menu items.
- Keep original first screenshot design language: narrow icon rail, secondary side nav, white surfaces, navy text, orange primary controls, clean spacing. Start simple; expose complexity only when requested.
- User supplied screenshots of project document folders, code repositories + Agent sidebar, Agent chat/work start, project modal, personal dashboard, Agent management/requirements board. The source PDF `AegisTeam_超级团队_竞品调研_V0.2_格式修正版.pdf` discusses monday AI, GenTeam and hilos; interpret as research references, not a feature checklist. Distilled ideas: preserve one workspace for work + Agent, show clear task status and human approval boundaries, and avoid multiple competing chat panels.

## v5 changes

1. **Personal / 个人主页**: responsive dashboard with stat cards derived from local example tasks, priority/project/type filters, actionable task rows opening the common task detail drawer, recent activity, calculated completion overview. Existing 我的任务 and 消息通知 pages remain; notifications now have read/unread states.
2. **Agent navigation**: 对话 / 智能体设置 / 智能体模板 / 智能体任务. Existing chat/work, MCP/Skill setup and Agent task workflows remain. Template gallery supports filters, preview, and creating an **unpublished local draft** that opens Agent settings.
3. **Project modal**: original project cards remain and open modal with direct paths to Kanban, docs, and repos. The modal now includes the requested 7-day Token usage visual. Its 128,560 and percentages are explicitly **mock values based on a reference screenshot**, not measured usage.
4. **Mobile**: secondary page tabs for Agent and Personal now remain reachable at 320/390px. Project mobile tabs and team mobile tabs retained.
5. **Docs/repo**: folder and file view, doc form, repo details tabs, mock Agent discussion. No actual Git/CI data or AI results.
6. **Safety / clarity**: local-only labels, no fabricated successful remote operations. User text is escaped before HTML interpolation. Last administrator protection from earlier team implementation remains.

## Visual/interaction review by roles

- New user: primary tasks obvious, templates provide helpful starting points, no new project menu.
- Experienced developer: direct repository/task links, inline status and project filters; no fake real PR merge action.
- Project administrator: project summary and team/Agent access converge; token numbers overtly mock rather than false billing information.
- Minimalist: no permanent side panels in project modal; optional controls appear within the relevant feature.
- Blue-team reviewer: content escaping, local-only boundaries, admin retention and UI state protections. Red-team challenge cases: malicious text should not execute, cancelled popovers must not write remote data, narrow viewport must retain a route to all menu items.

## Verification and limitations

- Chromium via Playwright `page.set_content()` passed at 320, 390, 768, 1024, 1440 and 1664px. Flow includes original project cards, modal/token details, creating and reopening a document with `<script>` text, code repo PR tab, Agent chat, template preview/create draft, personal task details, notifications read/unread, team regression, and no top-level horizontal overflow / no JS runtime errors.
- Automated test: `test_v5.py` (Chromium/Playwright). Source project may have earlier tests `tests/team_smoke.py` and `tests/test_rd_quick.py`; the new smoke suite does not replace other regression suites.
- This environment blocks Chromium navigation to `file://` and localhost, so **reload persistence and native file downloads could not be automatically verified**. UI state relies on browser localStorage and should be manually checked by opening the HTML in Chrome/Edge.
- UI is **not production ready as a complete SaaS** and must not be presented as backend connected. User has explicitly scoped this phase to **UI and interaction only**, not backend.

## Continuity protocol

1. Re-read this document, the predecessor `docs/RD_SIMPLIFICATION_SPEC.md` and `docs/TEAM_UX_SPEC.md`, and the current `index.html` at the exact target branch before a new change.
2. Verify latest branch and file blob SHA before writing; preserve earlier verified behaviors; deliver a complete single-file HTML for owner review.
3. Track screenshot-grounded facts separately from interaction assumptions; evaluate usability with new-user, developer, manager, and security roles and run explicit browser tests after edits.
