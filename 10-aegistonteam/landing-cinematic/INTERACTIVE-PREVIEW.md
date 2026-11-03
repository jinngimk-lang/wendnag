# AegistonTeam 交互落地页预览

## 在线预览

https://aegistonteam-light-motion-preview.vercel.app

这是独立 Vercel 预览项目，不使用 aegiston.com 正式域名，也没有修改任何现有生产站点。

## 页面交互

- 顶部导航吸顶；手机端可展开导航菜单。
- 页面区块进入视口时淡入；卡片 hover 轻微抬升。
- 页尾三位 AegistonTeam 卡通伙伴沿轨迹奔跑，进入视口后启动动效。
- 工作台与团队结构截图可点击放大查看。
- 尊重系统 prefers-reduced-motion 设置。
- 页面使用暖白 / 浅米色背景、自然中文无衬线字体、轻分隔线与克制橙色强调；没有深色整页背景、英文编号或装饰箭头。

## 真实性与边界

- 工作台与团队结构均为用户提供的真实产品截图，未重绘内部 UI。
- 角色视觉沿用 AegistonTeam 自有卡通角色，不使用外部 IP。
- 当前预览资源托管在 companion asset deployment：https://aegistonteam-light-landing-preview-tako8.vercel.app/assets。正式发布前需将图片资源归并进仓库或正式站点。
- “进入工作台”当前仅滚动至真实产品截图区域，不会登录或操作真实账户。

## 源码

页面源文件：10-aegistonteam/landing-cinematic/site/index.html

## QA

- HTML 结构解析通过。
- 内联 JavaScript 通过 node --check。
- Vercel 页面 HTTP 200。
- 工作台截图、团队结构截图、角色图片均 HTTP 200。
- 当前环境无法启动本地 Chromium；需要在真实浏览器继续验收桌面和移动端布局。
