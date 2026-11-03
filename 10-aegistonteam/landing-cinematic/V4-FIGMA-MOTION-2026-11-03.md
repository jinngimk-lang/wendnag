# AegistonTeam V4 · 暖白漫画互动落地页（2026-11-03）

> **当前最新设计锚点，优先于本目录 V1 / V2 / V3。** 本轮用户连续两次明确要求继续优化「aegistonteam协作落地页.png」认可的漫画风格，并**结合 Figma Motion / Smart Animate**设计真实动效和更灵动的排版；保存可持续恢复的 GitHub 上下文。此项目为**可交互概念页面，不是已部署正式网站**。
> 关联：Draft PR #27，分支 `design/aegistonteam-cinematic-landing-20261103`。

## 1. 不得丢失的唯一视觉事实源

- 用户亲自确认并要求持续优化的原图：本对话附件 `aegistonteam协作落地页.png`，**910×1729**；SHA-256 **`94e78b7b06678fc0ad29a6581e376500a3987f6a2327a611a1c489818e97e441`**。
- 图中核心：`#FCF8F3` 左右的暖纸白背景、深石墨蓝中文标题、橙色强调、黑色手绘线条、三位原创卡通伙伴（橙色主角带白色斜条、奶白伙伴、深灰伙伴）、真实 AegistonTeam 工作台和团队组织截图。
- 页面务必保持漫画/手绘语气而非泛用 SaaS 卡片模板；角色运动表现遵循用户提供的 [Zenith Footer](https://motionsites.ai/?prompt=zenith-footer) 交互**结构**，不是复制任何外部人物、作品或 IP。
- **禁用**：整页深蓝、星空橙色传送门、英文大编号、空洞英文胶囊标签、满屏装饰箭头 `→↑↗`、AI 重画中文产品 UI、未经核实的商业功能/数据宣称。
- 真实产品 UI 来自用户附件 `image(20261103-053734).png` / `image(20261103-053851).png`。只缩放/裁切截图，不改变内部像素。

## 2. V4 核心实现（本轮新增）

V4 是真实可操作的**离线 HTML/CSS/JavaScript 原型**，不只是效果图。

**页面结构（阅读顺序）**
1. 大面积暖白首屏：标题「让好点子，开始一起工作。」；右侧保持用户确认的原漫画三人奔跑视觉；两条无箭头 CTA「看看工作台」「了解怎么协作」。
2. 三条极短用户价值句，分隔而不是无限重复方框卡片。
3. 大型真实产品浏览器视窗：可点击切换「工作台 / 团队结构」，用同一容器 crossfade / slide 过渡。
4. 三张错位暖色漫画卡片：「把灵感留下 / 把事情往前推 / 把伙伴聚在一起」，对原画进行抠图，不用陌生角色。
5. 「从一个人想到，到一群人做到。」：交互式三项单选手风琴，右侧显示原始团队组织截图。
6. 「下一次好点子，我们一起完成。」：暖杏色页脚、手绘跑道，三人漫画小队随滚动推进，按钮可重播。

**行为说明**
- 鼠标轻微视差：0–16px，以触控为例时不触发；退出后归位。
- 滚动进入的区块：opacity 0→1 + Y 26→0px，700–800ms。
- 标签：两张真实截图使用480–600ms过渡，aria-selected / aria-hidden 随状态同步。
- 卡片：Y -11px + 少量缩放，用克制 easing/spring。
- 手风琴：只有一项打开，使用 aria-expanded 标注。
- 页脚：三人组随 scroll progress 0→1 沿跑道横移并微弹跳；手动触发重播 3.4s。
- 进度条跟随页面长度；移动端支持展开/收起菜单；系统 `prefers-reduced-motion: reduce` 时关闭非必要运动。
- 所有 CTA 链接当前只导向页面内可用 section，**不要虚构登录或上线地址**。

**Figma 对应**
- 采用 Figma Smart Animate 的“同层匹配、容器稳定、内容改变”与 Figma Motion 的 easing/keyframe 设计思路。
- 本轮另创建了 **[Figma Motion Study](https://www.figma.com/design/TqvJueUd5dKgqtRFWcmQ3W)**，包含可编辑中文文案、导航/按钮和原生关键帧：首屏文字入场、三人主视觉的**简化几何运动代理**入场、结尾小队的**简化几何运动代理**水平位移和Y轴节奏；关键帧 API 已回读确认（TRANSLATION_X/Y、OPACITY）。
- **诚实边界**：Figma 内不是原始插画导入的正式全页复刻；原版漫画角色和可操作的完整页面仍以本轮 HTML 原型为准。Figma Starter 接口当轮达到调用上限，未能获取画布截图做最后的视觉复验，后续需复检，不可宣称 Figma 已像素级验收。

## 3. 本轮交付物（由 ChatGPT 工作容器生成，在会话中下载；不在 GitHub 仓库中冒称已有二进制）

工作目录 `/mnt/data/aegistonteam_v4/`，所需全部素材已随 ZIP 打包：

| 交付物 | SHA-256 | 验证 |
| --- | --- | --- |
| `AegistonTeam_V4_暖白漫画动态落地页_HTML源码.zip` | `ee945d3d0a8e1041168adf3de908d6f71067d8a52da141cefe60f13f5380c169` | 包括 index.html、README.md、MOTION_SPEC.md、7张真实/原画衍生素材 |
| `preview_desktop_first.png` | `eb629fea2f9c28318477c239fac3effc942b940ef1c2b455f5ef6c4ab893dbe1` | 1440×900 首屏 |
| `preview_desktop_full.png` | `1f68c3dbff546e445ce5a919c44815186968e08558dc1cd359ad311726cf8c17` | 1440宽全页 |
| `preview_mobile_full.png` | `965613bff7006d633918c877447431363f24cbe07ed201ad378b8c238764fb92` | 390宽移动长页 |
| `AegistonTeam_V4_交互动效演示.mp4` | `4ea8941dfe115183f0df3b66ec32bd97be15d46d565efb770079660cddc1dbbb` | 6s / 12fps，浏览器实际画面采集 |

完整代码文件内 SVG / JS / CSS 都可再编辑，不使用外部 JS 运行时或账户；由 `index.html` 加 7 个素材离线运行。素材包括： `hero-doodle.png`、`footer-doodle.png`、`card-idea.png`、`card-focus.png`、`card-team.png`、`workspace.webp`、`orgchart.webp`。
原始素材仍属于**当前对话附件**，本轮已提交到 GitHub 的是上下文/工程规范，而不是全部二进制。

## 4. V4 已验证

- Playwright Chromium，1440×900 与 390×844 视口；所有 8 张 img 成功加载（其中一张真实 UI 复用两处）。
- `document.documentElement.scrollWidth == window.innerWidth`，桌面/手机均没有横向溢出。
- 点击「团队结构」后 tab aria-selected=true、对应真实图 aria-hidden=false；截图可切回工作台。
- 点击手风琴第二项，`aria-expanded=true`；手机端打开导航时类名变化且 aria-expanded=true。
- 6 秒演示 MP4 已由真实浏览器逐帧截取并经 ffprobe 核验。
- 本验证在隔离浏览器中使用 data URI 对图片进行加载，原因是沙箱会禁止 file:// 导航；这不是用户机器本地 HTML 打开会被禁止的证据。
- 尚未验证全部机型浏览器和线上实际产品路由；**未部署线上**。

## 5. 下一阶段建议与不可超越边界

1. 若用户认可 V4，可继续增强首屏角色的手绘细节并增加更像真实跑步的同一角色逐帧步态（目前是2.5D横移和上下跳）。
2. 如要将原型嵌入正式站点，先定位前端仓库、现有视觉 token、可用路由和构建流程；**没有真实登录 URL 不可把概念入口硬编码为正式登录**。
3. Figma 若继续编辑，需要先实际截图核验代理画板，再导入本人 PNG 原始角色，完成可编辑的 Frame/Component/Timeline，不能把现有几何代理当作角色正稿。
4. 视觉/动效的一切新迭代优先核对 SHA 锚点，持续保持上一轮已批准的暖白漫画方向。

参考文档： [Figma Motion 官方发布](https://www.figma.com/blog/introducing-figma-motion/) 、[Smart Animate](https://help.figma.com/hc/en-us/articles/360039818874-Smart-animate-layers-between-frames)、[Figma easing/spring](https://help.figma.com/hc/en-us/articles/360051748654-Prototype-easing-and-spring-animations)。
