# AI 宣传视频导演系统研究 — Checkpoint 05

日期：2026-09-24  
分支：`research/ai-video-director-system-20260924`

## 1. 用户目标

在既有《自媒体平台流量机制地图-2026.md》基础上，把“什么内容容易获得流量”进一步编译成一套可直接用于 AI 视频生成的导演系统。

用户希望未来只需要提供：
- 产品/主题；
- 平台；
- 目标时长（例如 6s / 15s / 30s / 60s）；
- 目标（曝光、搜索、收藏、私信、Demo 等）；

系统就能输出：
- 使用哪些流量引擎；
- 总创意与艺术方向；
- 人物/场景/道具设定；
- 精确到秒的脚本、对白/旁白；
- 每一个镜头的景别、角度、焦段、运动、灯光、构图；
- 演员微动作和表演；
- 转场、节奏、字幕、声音、音乐、SFX；
- 每镜头可复制的 AI 视频生成 Prompt；
- 起始帧/结束帧、连续性锚点、禁漂移项；
- 后期合成/UI 保真策略；
- 平台原生版本和 A/B 版本；
- 质量检查表。

最终目标不是“一段万能 Prompt”，而是一个 **AI Director Compiler / AI 导演编译器**。

---

# 2. 已重新读取的项目事实源

已从 `main` 回读：
- `.agents/skills/max-potential-multimodal-creative-agent/SKILL.md`
- `.agents/skills/creative-director-runtime/SKILL.md`
- `creative-runtime/STATE.md`
- `creative-runtime/LEARNINGS.md`
- `06-analysis/marketing-video-platform-research/自媒体平台流量机制地图-2026.md`
- `06-analysis/marketing-video-platform-research/多平台宣传视频逐条复盘与高热内容对标研究.md`

必须继续遵循：
- 每个镜头必须有戏剧任务；
- Camera movement 必须被事件/信息/情绪变化所驱动；
- 产品是因果机制，不是漂浮的 Hero Object；
- UI/Logo/文本需要保真时优先合成/2.5D，不让生成模型重画关键文字；
- 视频是时间中的变化，而不是漂亮静帧堆叠；
- 图片、视频、音乐、声音、字幕需要共享同一个情绪/信息曲线。

---

# 3. 第一阶段外部研究：AI 视频模型真正支持什么

## 3.1 Runway Gen-4 / Gen-4.5

官方提示指南：
- Gen-4 常见生成长度为 5s / 10s；
- 更适合把一次生成理解为一个 scene；
- 官方明确不建议在单个短 clip 里塞入多个场景变化、多个大动作和大量风格变化；
- Image-to-Video 时，输入图已经定义构图/主体/风格，文字 Prompt 应主要描述 motion；
- 建议从简单 Prompt 开始，一次增加一个变量；
- 正向描述比 negative prompt 更可靠。

结论：
> 长广告应拆成多个可控短镜头，不应该写一条“0–30秒逐秒变化”的巨大生成 Prompt。

## 3.2 Google Veo 3 / 3.1 + Flow

Google 官方 Prompt Guide 建议明确描述：
- framing / camera motion；
- style；
- lighting；
- character；
- location；
- action；
- dialogue；
- sound design。

Veo 3 可以在生成时处理 dialogue / audio。

Flow / Veo 3.1 进一步支持：
- Ingredients / reference consistency；
- start/end Frames to Video；
- camera controls；
- Scenebuilder；
- extend；
- native vertical；
- 1080p / 4K；
- 2026 更新强化角色与背景一致性。

Google I/O 2026 的内部制作案例也公开了：
- 先做 ingredient/reference sheets；
- 再 storyboard；
- 再生成动作；
- 最后 composite + time-remap raw generated motion。

结论：
> 专业 AI 视频不是“Prompt → 成片”，而是 **资产/参考 → 分镜 → shot generation → composite/edit**。

## 3.3 Higgsfield

官方公开 50+ camera controls，例如：
- crash zoom；
- crane；
- dolly；
- handheld；
- FPV drone；
- object POV；
- through-object；
- snorricam；
- bullet time；
- 360 orbit；
- whip pan 等。

其 2026 Camera Control 文档强调：
> Camera move 是起点、终点、速度曲线、镜头与主体关系的物理事件，而不是单独一个“cinematic”形容词。

结论：
> “艺术大胆”应该变成明确的 camera choreography，而不是堆高级摄影术语。

## 3.4 LTX Studio

2026 官方资料强调：
- script/concept → dynamic storyboard；
- Elements 保持人物/对象/场景一致；
- camera movement / keyframes / visual references；
- timeline editor / sound design；
- Flows 可把 prompt → image → video → audio → upscale 串成节点；
- 支持多模型路由和批量 variation；
- 改一个 node 时可只重跑受影响环节。

结论：
> 最终系统应把每一镜头定义成可替换的 node / packet，而不是把整个广告锁在一个不可维护 Prompt 里。

## 3.5 Adobe Firefly

2026 官方 Video Prompt 推荐结构：
> Shot Type + Character + Action + Location + Aesthetic

并允许通过 camera angle / motion 等参数控制视觉。

## 3.6 ElevenLabs

官方 Voice Design 建议明确：
- language / regional variant；
- gender / age；
- persona；
- emotion；
- timbre；
- pacing；
- delivery。

Eleven v3 / Dialogue mode 支持：
- 多 speaker；
- interruptions；
- emotional tags；
- whispers / laughs / sighs 等表演性提示。

Sound Effects 官方建议：
- 单一效果用清晰简短 Prompt；
- 复杂声音序列最好拆成独立 SFX 后在编辑器组合。

结论：
> 声音也应该 shot-by-shot 设计，不能把“音乐 + 对白 + 10 个音效”全塞给一个生成请求。

## 3.7 Sora 的当前状态

OpenAI 官方：
- Sora Web / App 于 2026-04-26 停止服务；
- Videos API / Sora 2 系列 API 在 2026-09-24 停止。

因此：
> 本系统不会以 Sora 作为当前推荐执行依赖。历史 Storyboard / Re-cut 等概念仍可作为流程启发，但最终导演语言必须 model-agnostic。

---

# 4. GitHub 外部方法补充

发现 MIT 项目：
`Rylaispirit/cinematic-video-prompt-skill`

优点：
- 700+ 电影摄影术语；
- 明确 Shot Size / Angle / Camera Movement / Lighting / Composition / Lens / Mood；
- 规则包括“每 clip 1 个主 camera movement、1 个主 action，复杂动作拆镜头”；
- MIT 可合法吸收方法结构。

本项目不需要复制其 700+ 术语库，因为 `creative-director-runtime` 已经有更强的“为什么移动镜头”的戏剧层。
可吸收的是：
- 术语标准化；
- shot prompt 的组织方式；
- “不要关键词堆砌”的约束；
- 情绪 → 摄影语言的 lookup 思路。

---

# 5. 当前核心设计：AI Director Compiler

最终系统应由 8 层组成：

## L0 — Traffic Strategy
输入：
- 平台；
- 内容目标；
- Spike / Shelf / Series；
- 主流量引擎；
- 1–2 个副引擎。

输出：
- 为什么点开；
- 为什么继续；
- 为什么互动；
- 为什么分享；
- 为什么回来；
- 为什么相信。

## L1 — Creative Thesis
输出：
- 一句话创意命题；
- 人的 desire / obstacle；
- 产品如何作为 causal hinge；
- 最终 remembered idea；
- Boldness Level。

## L2 — Story / Script
输出：
- Beat map；
- duration budget；
- 每秒事件；
- 台词/旁白；
- 信息曲线；
- 情绪曲线；
- 产品证明点。

## L3 — Character / World Bible
定义并冻结：
- 人脸/年龄/发型；
- 服装；
- 道具；
- 场景；
- 时间；
- 光线；
- 产品 UI / Logo；
- 色彩；
- 声音 motif。

## L4 — Director & Cinematography
每镜头：
- dramatic job；
- framing；
- angle；
- lens / DOF；
- composition；
- subject micro-action；
- camera movement + movement reason；
- lighting；
- environment motion；
- start/end state；
- transition / eye trace；
- sound intention。

## L5 — AI Generation Packet
每镜头单独生成：
- reference assets；
- immutable anchors；
- visual prompt；
- motion prompt；
- audio/dialogue prompt（若模型支持）；
- forbidden drift；
- seed / start-end frame / camera preset；
- generation model route。

## L6 — Post & Sound
- VO / dialogue；
- ambience；
- Foley；
- UI SFX；
- music energy curve；
- J/L cuts / sound bridges；
- subtitle timing；
- UI compositing；
- logo/end card；
- speed ramps / time remap。

## L7 — Critic / QA / A-B
检查：
- 身份连续；
- UI 真实；
- 镜头是否每一个都“有工作”；
- 是否存在装饰性镜头；
- 流量引擎是否在内容中真实发生；
- 产品是不是太早/太硬；
- 平台语法是否正确；
- 是否可拆出 A/B。

---

# 6. 时长必须成为系统的核心输入

初步建议用“shot budget range”，不是硬规则：

| 总时长 | 默认镜头数 | 叙事能力 |
|---|---:|---|
| 6s | 1–2 | Hook + Proof / single visual gag |
| 10s | 2–3 | Hook + action + payoff |
| 15s | 3–5 | Pressure → hinge → proof → payoff |
| 20s | 4–6 | 可以加入一个真实过程与人类反应 |
| 30s | 6–9 | 完整 mini-story + 2–3 proof beats |
| 45s | 8–12 | 教程/实测/情绪与产品可以并行 |
| 60s | 10–16 | 完整案例/实验/多层证明 |
| 90s | 14–22 | 可加入 context、objection、限制与 CTA |

这些只是制作预算。
最终切点必须由：
- information change；
- emotional change；
- movement；
- gaze；
- sound；
- proof
决定，而不是机械平均切割。

---

# 7. “艺术大胆”不能等同于“镜头乱飞”

计划建立 Boldness Ladder：

## B0 — Clear
纯功能清晰。
locked / simple push / true UI。

## B1 — Social Native
handheld / phone POV / fast reframing / jump-cut energy。

## B2 — Cinematic
motivated dolly / crane / rack focus / graphic match / controlled lighting arc。

## B3 — AI-Native Impossible
through-object；
object POV；
impossible macro-to-wide；
time freeze / bullet time；
environment morph；
scale transformation；
seamless impossible camera path。

## B4 — Surreal Metaphor
把抽象问题物理化：
- 合同风险变成裂纹/红线；
- 信息噪音变成淹没房间的纸；
- Agent 把混乱空间折叠成秩序；
- 时间压力具象为办公室墙壁向人挤压。

原则：
> 一条商业短片通常只需要 1 个真正不可思议的视觉铰链。所有镜头都“炫技”会削弱产品证明。

---

# 8. 计划中的关键模板

最终文档将提供：

1. **Universal Input Card**
2. **Duration Compiler（6/10/15/20/30/45/60/90s）**
3. **Traffic Engine → Film Grammar Matrix**
4. **Bold Camera / Transition Library**
5. **Character Bible**
6. **Shot Packet Template**
7. **Second-by-second Script Table**
8. **Dialogue / VO Performance Sheet**
9. **Sound Design Sheet**
10. **Model Routing Matrix**
11. **AI Continuity Checklist**
12. **UI/Product Truth Workflow**
13. **Platform Rewrite Rules**
14. **A/B Variant Compiler**
15. **完整 15s 示例**
16. **完整 30s 示例**
17. **完整 60s 示例**
18. **Final QA Gate**

---

# 9. 下一阶段

重新读取本 checkpoint 后继续：

1. 建立 “8 大流量引擎 → 导演/摄影/声音语言”映射；
2. 设计时长编译算法；
3. 设计“逐秒脚本 + shot packet”双表系统；
4. 加入大胆 AI-native 视觉理念，但确保每个炫技镜头有戏剧目的；
5. 建立模型路由：
   - Veo/Flow：对话/音频/Ingredients/Frames/Extend；
   - Runway：短 scene、图生视频、motion 精确；
   - Higgsfield：camera choreography；
   - LTX：storyboard / Elements / Flows / multi-model；
   - Firefly：品牌/商业安全生成路线；
   - ElevenLabs：VO / Dialogue / SFX；
6. 用 LegalLens 做 15 秒完整演示；
7. 再做一个 30 秒“AI真实翻车 → 产品解决”的高流量版本；
8. 生成正式 Markdown + DOCX；
9. DOCX 必须 render 全页检查后才交付；
10. 最终 diff 只保留知识文档与 checkpoint，不提交第三方素材或临时生成文件。
