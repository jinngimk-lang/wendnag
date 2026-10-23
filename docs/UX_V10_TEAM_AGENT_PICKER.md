# AragonTeam v10：新建团队同时选择人员与 Agent

日期：2026-10-23。分支：`jinngimk-lang-AT`。原型入口：仓库根目录 `index.html`。

## 本轮内容与界面逻辑

- 「团队管理 → 新建团队」保留名称、类型、简介；新增 **团队成员** 和 **智能体 Agent** 双选择区域，分别支持搜索、多选、选中数量、无匹配提示。桌面双栏，窄屏单栏。
- 人员使用已有 `teamData.members` 全量名单（不只显示前九名）。Ada 默认作为管理员进入新团队；不额外选择人也可以创建。
- Agent 使用已有原型 `rd.agents`，已发布 Agent 可选，草稿可见但禁用。Agent 不自动拥有人的管理员角色，也不会触发真实 Agent 执行或权限。
- 新建团队保存 `agentIds:number[]`，与原有 `memberIds` 分开。老团队缺失 agentIds 字段时按空数组处理，兼容原有 localStorage 数据。
- 卡片仅在分配了 Agent 时显示数量；团队详情新增 Agent 标签与「管理 Agent」入口，创建后可增减。归档团队不能调整。
- 团队搜索支持 Agent 名称，展示文字继续 HTML 转义。四个一级导航和项目七项二级导航保持原样。

## 本地验收

2026-10-23 Chromium + Playwright 页面注入模式：
- `tests/test_team_v10.py`：320/390/768/1024/1440/1664px 六宽度 PASS，成员/Agent 搜索、多选保留、创建结果、团队详情、后续 Agent 管理、原团队兼容和项目回归均通过；无整页横向溢出、无捕获 JS 异常。
- `tests/test_team_v10_adversarial.py`：390/1440px PASS，无选择时 Ada 仍是管理员；没有默认 Agent；草稿禁用；搜索空态；恶意 HTML 文本不会执行；Agent 更新不改变人类成员身份。
- 九段内嵌 JS `node --check` 语法检查通过。

**注意**：这是纯前端 UI 原型，不接真实后端，不发邀请或授权。文件跨刷新本地持久化尚未在此沙盒执行真实 file:// 浏览器测试，需用户本机审核。

## 恢复上下文与后续迭代

先读取本文件、`docs/UX_V9_MEETING_INVITATION.md`、`docs/UX_V8_MEETING_FLOW.md` 和最新 `index.html`，确认分支 SHA，再做可逆修改；保持智能体/项目/团队/个人四大入口、项目七项菜单不变。