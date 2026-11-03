# AegistonTeam V3 — 已确认漫画基准的交互式落地页

> 2026-11-03｜**当前有效设计锚点（优先于 V1 / V2）**｜[Draft PR #27](https://github.com/jinngimk-lang/wendnag/pull/27)
> 结果状态：本地 HTML + 原始素材衍生 PNG/WebP + 桌面/移动预览 + 实际 CSS 动效 GIF 已生成且通过浏览器验证。**尚未部署 V3 至正式网站，也没有创建原生 Figma 文件。**
> 当前对话工作目录 `/mnt/data/aegistonteam_v3/` 是临时工作区，不是 GitHub 远程目录。完整源码以用户可下载 ZIP 交付。**远端 GitHub 当前已有早期 V2 网页源码 `site/index.html`，但它不是 V3！V3 的完整 HTML 与原图衍生素材目前仅在聊天 ZIP 中交付，尚未上传远端。不要误把旧 `site/index.html` 当成 V3。**

## 唯一视觉基准与用户已确认反馈
用户明确表示**找回的图片就是想延续的方向**：`/mnt/data/aegistonteam协作落地页.png`，910×1729，暖纸白背景、橙色主角/乳白与灰色伙伴、粗黑手绘轮廓、轻量橙色动态线、自然中文排版、真实工作台截图。此图是原始视觉锚，不再以 V1 深色游戏门户，也不以 V2 的另一套白底排版作为主基准。

用户要求：
- 延续这一张的全页漫画插画风格，仍然是**产品官网**，不是 AI 梗图或插画海报。
- 以 Figma Smart Animate / Motion 的原则去做动效；最终网页需要真实交互，不能只发静图。
- 排版有节奏、轻盈、有趣，禁止粗糙模板堆叠、编号大英文、泛用标签和大量箭头 `→↑↗`。
- 准确保留三位原创角色的脸、比例、斜饰带与黑色描边；不替换示例 IP。
- 真实 AegistonTeam UI 不能由 AI 重新绘制错字，保持原始截图像素内容。
- 更新 GitHub 为后续上下文恢复锚点。当前状态若回读，**先读本文件**。

## V3 项目内容与路径（只在本次会话容器中）
- `site/index.html`：纯 HTML/CSS/JS、没有依赖 CDN 或账户登录，压缩前 31,707 bytes，SHA256 `68b89e71d3d9a068b8cff28de660a9382081751f29800c99e2ba671db965d2ad`。
- `site/assets/hero-doodle.png`：从**用户确认的漫画视觉基准**抠出的三人奔跑主角，102?（实际 1014×620），SHA `ae6814934aa3d0a302fc8ec7401925ff5a78a4c8f3534e59e9991d1013010a5a`。
- `site/assets/footer-doodle.png`：同一漫画基准提取的结尾奔跑小队，1120×418，SHA `4d343bcc5caf205b17c210406544aa6ad9cef3617292acd3f44997ef586267b7`。
- `site/assets/card-idea.png`、`card-focus.png`、`card-team.png`：从同一用户确认原图提取的三张插画，原轮廓/身份未由生成模型改写。
- `site/assets/workspace.webp`、`orgchart.webp`：由用户真实截图缩放制作；截图内部中文内容不变，不绘制虚构菜单。
- `AegistonTeam_V3_首屏.png`：1600×900，SHA `06412b69ee3ef0d622ad008aae42452efa319db7c8fcf68663e021fb07d0b0bb`。
- `AegistonTeam_V3_完整落地页.png`：1600×5183，SHA `dd7a086bc034da802bf8e1fb0b0f02016b02867e6025f388d3edcd4e9d61eee9`。
- `AegistonTeam_V3_手机端首屏.png`：390×844，SHA `7e4983b9ef063a952df0eff4283c1a4285ee7626ed2c76b2bdd291951324b7e1`。
- `AegistonTeam_V3_手机端完整页.png`：390×4882，SHA `37c440ff8e3ddcaa6afe94fbc415bd94b4a123c0e634b90280f70bf17eb01688`。
- `AegistonTeam_V3_真实网页奔跑动效.gif`：来自真正的 Chromium CSS animation 帧采集，不是独立编造的展示动画，SHA `b5e428a8cf7de17f65553d76a2152e933a6fb953c2088ea9b631fb0da94bd4c2`。
- `AegistonTeam_V3_交互式落地页_完整源码.zip`：离线可打开的 `site/index.html` 和对应 assets，SHA `ada8a2eb0c94daafac04c7d333e96895320ce0e4af42ac07c8e19f36471d23c0`。解压后打开 `site/index.html`。

## V3 信息架构（准确文字）
1. **Hero**：「让好点子，开始一起工作。」+「项目、任务、智能体，在一个工作空间里彼此连接。让每一次灵感，都有人一起往前推进。」右侧用户确认的三人奔跑插画。两个主 CTA「看看工作台」「我们怎么协作」**只锚点滚动到页面内；不假称真实登录**。
2. **协作叙事**：「一个人有灵感，一群人有办法。」交互式三态“灵感探索 / 专注推进 / 默契协作”，左边同一展示画框切换角色图片，右侧标题、说明协同更新。
3. **产品截图**：「好看的背后，是真正能做事的工作空间。」原始截图切换“工作空间 / 团队组织”，放大弹窗，按 ESC 关闭。产品真实 UI 只放大/缩放/切换，不重新绘制。
4. **伙伴卡**：「认真做事，也可以很有趣。」三张品牌漫画角色卡，有轻微 hover 提升，但不擅自将这些角色卡写成已交付的智能体功能。
5. **团队证明**：「大家都在同一队，事情就更好推进。」原始组织图截图加少量编辑说明。
6. **页尾**：「下一次好点子，我们一起完成。」暖杏色背景+三人奔跑横向位移+微弹跳；进入视口时才开始，有「再跑一圈」真实可用按钮。

## Motion 状态机 / Figma Smart Animate 映射
| 交互 | 起止状态 | 运动参数 | 目的 |
| --- | --- | --- | --- |
| 首屏角色 | Idle → PointerShift | ±18px X / ±14px Y, 500ms, `cubic-bezier(.22,1,.36,1)` | 低幅度视差，不干扰文案 |
| 叙事插画 | Idea / Focus / Together | 210ms 淡出，图片/标题一起替换，280–480ms 淡入 | 对应 Figma matching-layer Smart Animate 的状态连续性 |
| 产品截图 | Workspace / Team Organization | 支持时使用 `document.startViewTransition()`，否则 CSS transform+fade | 强调“同一展示画框不同状态” |
| 卡片 Hover | Default / Hover | Y -10px, ~450ms 同一 easing | 按摩擦最少原则提示可互动 |
| 滚动揭示 | Hidden → Visible | 24px Y + opacity, 750ms | 内容层级逐步进入 |
| 页脚跑动 | Offstage → Across → Rest | ~5.6s 横向移动，0.62s 微弹跳循环，可重复触发 | 将自有小队变成页面结尾的记忆点 |
| Navigation | Desktop / Mobile | 折叠菜单 / 关闭菜单，滚动进度线，锚点高亮 | 清晰方向与响应式 |
| Reduced Motion | Any → Static | `prefers-reduced-motion: reduce`：停止奔跑和非必要过渡 | 兼顾易用与无障碍 |

**重要区别**：上表是对 Figma Smart Animate 原理的 Web 实现，不代表当前已创建 Figma 原生可编辑画板/原生交互原型。网页无 Motion.js 第三方运行依赖，采用浏览器原生 CSS / View Transition / IntersectionObserver 保持离线可复现。

## 本轮浏览器 QA（2026-11-03）
- Chromium headless，桌面 1600×900；手机 390×844。
- 页面运行 JS exception 0；所有 img 完整加载，桌面与手机 page scrollWidth 分别与 clientWidth 相同：无横向溢出。
- 点击第三个场景，标题正确变为「一起做，更有默契。」。
- 切换真实截图到组织图后，img.alt 和图片源发生对应切换；放大弹窗显示，ESC 可关闭并恢复焦点。
- 移动端菜单展开后 `aria-expanded=true`；页面链接是内部锚点。
- 真正的 CSS runner 在 20 个连续时间采样中有位置变化，已输出 GIF；页面支持手动重播。
- 图片使用浏览器内联数据 URI 进行测试，因为这个隔离环境对 file:// / localhost 浏览器导航存在管理员策略限制。**这是 QA 环境限制，不是网页源文件本身无法本地打开的证据。**
- 没有执行线上正式域名部署。移动端实际用户设备上的细节依然建议做最终目测。

## 视觉基准优先级与反向禁令
1. **最高**：用户确认的 `aegistonteam协作落地页.png`；
2. 最新用户明确要求；
3. 本 V3 文件；
4. 用户 V2 决策历史文档；
5. V1 仅用于撤回原因追溯，不得作为样式恢复候选。

禁止将整页改回深海蓝、添加巨型传送门、用陌生角色替代、增添大量英文编号/箭头或重绘真实 UI 错字。未经验证不得添加产品性能、客户、功能承诺。

## 下轮最小可逆迭代
优先考虑提高真实截图可读尺寸、完善角色跑步帧（目前是原画位置移动+轻弹跳，不是真实的腿部逐帧步态），以及与真实工作台 URL 对接（必须验证地址和登录策略）。若进入 Figma 原生协作，需独立创建**可编辑图层**并按此 V3 Motion 状态机建立匹配层连接，不能简单将整页扁平截图当成可编辑原型。

## 外部参考（原则，不复制资产）
- [Figma Smart Animate 官方说明](https://help.figma.com/hc/en-us/articles/360039818874-Smart-animate-layers-between-frames)
- [Figma 原型 easing / spring 官方说明](https://help.figma.com/hc/en-us/articles/360051748654-Prototype-easing-and-spring-animations)
- [Figma interactive components 官方说明](https://help.figma.com/hc/en-us/articles/39747190144023-Components-collection-Interactive-components-fundamentals)
- [Motion scroll animation 文档](https://motion.dev/docs/scroll)
- [MotionSites Zenith Footer 参考](https://motionsites.ai/?prompt=zenith-footer)
