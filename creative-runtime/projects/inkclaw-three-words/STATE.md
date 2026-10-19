# InkClawAgent：《老板说，就改三个字》视觉制作回溯文档

更新：2026-10-19

## 用户最终需求
- 在 ChatGPT 对话里交付两个故事人物的完整三视图（正/侧/背）和多张分镜图。
- 真实使用 TinyFish 已登录云端浏览器浏览 https://inkclawagent.com/ 的 Doc Agent 功能并截取真实界面；真实 UI 不得使用 AI 重新绘制、杜撰 AI 生成结果。
- 必要时从本文件恢复，不打扰用户；保存到 `jinngimk-lang/wendnag`，本创意与原有 BP/LegalLens 任务严格隔离。
- 影像质感为高水平真实企业广告摄影 / Nikon Z9 风格，低 AI 感，原创人物设定，电影摄影连续性。
- 对此前广告剧本《老板说，就改三个字》产生具体可用分镜。
- 不需要将本任务图片发布到外网，用户要在当前对话获得图像。

## 剧情锚点
40 秒办公室反转轻喜剧。
00–05：晚上九点办公楼，员工 B 一人加班，女老板 A 说「这个方案很好，就改三个字」。
05–15：B 放松，A 一字一顿「重、新、做」；B 笑容凝固，办公桌文件混乱，悲喜反差。
15–30：B 在电脑打开真实 InkClawAgent Doc Agent 编辑器，输入针对文件的具体修改要求；展示流程操作，不展示未验证的成功结果。
30–40：A 再问「怎么样了？」B 捧着养生茶说「在检查最后的结果」；末尾标题「工作可以很复杂，办法可以更聪明」。
若应用仍429，不得拍虚构的已完成 AI 生成。

## 角色不能混
- 人物 A：约45岁中国女性、面部成熟严厉、深色头发紧盘发/发髻、橄榄棕西装、印花上衣、低跟黑鞋；不混用 B 的蓝衬衫。
- 人物 B：约23岁中国女性、黑色高马尾、浅蓝衬衫、深蓝牛仔裤、工牌、白运动鞋；不混用 A 的盘发/西装。
- 品牌数字伙伴栀夏：深色长直发、白色针织衫，本剧首批分镜**不出场**，避免角色混淆；作为未来独立系列。

## 场景与镜头连贯
- 单一现代办公室；同一张木色桌、左前方银灰笔记本电脑、右侧报告堆、暖白办公台灯/顶灯、夜晚窗外高楼玻璃反光，桌面有茶杯。
- A 从过道右侧进入，B 端坐桌前面朝笔记本；保持镜头轴线与眼神方位。
- 时间夜晚九点，冷暖混合真实光源；压力段画面密集/手持轻微晃，产品段干净静止，尾声留白。
- 所有 AI 场景图均属于**剧情演绎**，产品 UI 为另行获取的**真实屏幕证据**，后期合成可用不可修改原像素内容。

## 真实产品证据（截至 2026-10-19）
TinyFish 通过登录用户工作区，测试记录：
- Doc Agent: https://agent.tinyfish.ai/runs/d0bbf5f9-7a18-4fb0-a0d3-ee9c59ed9898
- Review Agent: https://agent.tinyfish.ai/runs/dd3270bc-e93a-4657-b6fd-3d7431f33da4
- Brainstorm: https://agent.tinyfish.ai/runs/5889a7d5-31f8-428d-b59c-b0a2319b9904
- 2026-10-19 当前真实 UI 截图任务 run: https://agent.tinyfish.ai/runs/72485f97-70ea-4dcd-9d8a-4a551125ea3a
观察：Doc Agent Business Report Writer 可打开，输入区可用，Validate/Outline/Pages/Upload/Export/Reduce AI/AI Polish 控件可见，模型 glm-5.3，Agent mode/Team mode 等；生成时 HTTP429，文档0 words。Review Agent 可输入/保存测试文档但未完成 AI 分析输出。Brainstorm Input→Discovery→SPEC→TODO→Output 界面可打开，但 Discovery 阶段 429。
**未证实** Doc Agent 完整生成/改稿成功，任何广告产品效果镜头必须保留限制，不得模拟虚构的成功返回。

## 制作工具与进度
- 已读仓库根 AGENTS.md 两项创意 skill、creative-runtime/STATE.md / LEARNINGS.md；原有 STATE 仍属于 LegalLens 任务，不要修改。
- 当前独立分支 creative/inkclaw-three-words-20261019。
- Higgsfield gpt_image_2_5 双图提交尝试失败：用户计划不含 Basic；不升级。
- 改用已连接 Canva image generation 两个 16:9 三视图任务，UI 已提交；需要核对图片实际质量。
- 真实产品 screenshot 通过 TinyFish 浏览器进行专门截图任务；目前是否能从工具拿到独立截图文件仍待确认，不得把 run 链接谎称为 PNG。
- 下一步：取 TinyFish 截图任务结果；继续生成 6–8 张故事分镜图；核对三视图与镜头视觉连续性；把真实产品 UI 的单独截图（若可拿到）插入特写而非 AI 伪造；在 ChatGPT 对话直接呈现。
