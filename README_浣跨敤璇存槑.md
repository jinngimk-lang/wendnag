# AragonTeam 项目管理 — Figma 可编辑设计与交互原型

## 当前交付状态

- `index.html`：已经在 Chromium 中测试过的独立网页交互原型；不需要安装依赖，使用 Chrome/Edge 双击打开即可。
- `preview.png`：项目主界面静态预览（1664 × 913）。
- `figma-plugin/code.js`：Figma 本地开发插件脚本；目标是在**已打开的 Figma 设计文件**中创建原生可编辑图层与 Figma Prototype 跳转，而不是贴入扁平截图。
- `figma-plugin/manifest.json`：本地开发插件配置。Figma 可能要求您先创建一个开发插件取得官方分配的 `id`，然后将该 `id` 添加到 manifest。

**重要限制：** 此次 Figma 连接器报告 Starter 套餐 MCP 调用限额已用尽，因此没有直接改动你的云端 Figma 文件；本地插件也尚未能在你的 Figma 会话中真机验证。使用前请保留原始设计作为对照。

## 在网页中体验

直接用 Chrome、Edge 或 Safari 打开 `index.html`：

1. 搜索栏：输入项目名称可过滤项目。
2. 新建项目：填写表单后在当前网页会话中新建一张项目卡片。
3. 项目卡片：打开详情、查看成员、重命名及归档（演示数据，不接后端）。
4. 二级导航：可切换到需求看板、BUG 看板、文档等演示页面。
5. 一级导航：可切换智能体、项目、团队、个人和设置的二级导航。
6. 顶栏：主题切换、通知、账号菜单；Ctrl/Cmd + K 聚焦搜索；Esc 关闭弹窗。

## 将原生设计生成到原 Figma 文件

目标文件：
https://www.figma.com/design/5F8wZ9w0kRQInYOAj7kBji/AragonTeam-%E9%A1%B9%E7%9B%AE%E7%AE%A1%E7%90%86%E4%BB%AA%E8%A1%A8%E7%9B%98%EF%BD%9C%E5%8F%AF%E7%BC%96%E8%BE%91%E5%A4%8D%E5%88%BB?node-id=0-1

1. 使用可编辑权限登录 Figma Desktop，打开上面的**原文件**（不是新建空白文件）。
2. 如 Figma Desktop 支持无 ID 的本地开发 manifest，可直接选择 Plugins → Development → Import plugin from manifest，选择 `figma-plugin/manifest.json`。
3. 若 Figma 报告缺少 `id`，先在 Figma 里使用 **Plugins → Development → New plugin…** 创建一个本地开发插件，取得 Figma 自动分配的 `id`。将这个 `id` 写入本套件 `figma-plugin/manifest.json` 的顶层属性中（如 `"id": "Figma分配给你的ID"`）；不要随意猜测别的插件 ID。随后再执行第 2 步。
4. 通过 Plugins → Development → AragonTeam Project UI Builder 运行脚本。
5. 插件会在当前画布右侧追加 **5 个画板**：主项目页、项目详情、需求看板、新建项目弹窗、项目成员弹窗。所有界面元素都是 Figma 原生文本、Frame、Ellipse 或 SVG 矢量节点。
6. 进入右上角 **Prototype / Present** 模式，可尝试「新建项目」、「打开项目」、「成员」、「需求看板」等跳转；如果当前 Figma 版本不接受某些 API 连接，可在 Prototype 面板手工连线。
7. 修改名称、颜色、层级、字号、按钮尺寸均在 Figma 编辑器中进行，主界面并非背景图片。

本地插件**不会删除或覆盖原有图层**，每次运行只会在右侧增加新画板。如果重复运行，需自行清理多余的演示画板。

## 交互范围与注意事项

- Figma 原型负责画板跳转和弹窗展示；输入框在 Figma 中是可编辑的设计图层，并不是实际可输入的运行时表单。
- 真正的输入、搜索过滤、创建项目、重命名、主题切换等功能，请以网页 `index.html` 为交互演示。
- 因未经你的 Figma 环境实测，不能声称 Figma 中的原型交互全部运行成功。
- 头像在 Figma 里使用可编辑的图形占位；项目名称、描述、数字与颜色参考你给出的最初截图，没有把截图作为整页图像贴入。

## 设计规格

- 画板：1664 × 913，桌面端
- 三级信息结构：70px 一级图标轨 / 246px 二级导航 / 内容工作区
- 主色：深海军蓝 `#111D63`、功能蓝 `#536FAA`、强调橙 `#FF4A1B`
- 原始项目：AragonTeam Platform / Legallens
- 主要操作：新建项目、打开项目、成员、更多操作、项目搜索和二级模块导航
