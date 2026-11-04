# Visual research and architecture decision — 2026-11-03

目的：跳出原有 broadcast dashboard 的优化陷阱，探索「资本流向即一切」的互动范式。

| 候选方向 | 强项 | 缺点 | 本轮结论 |
|---|---|---|---|
| 控制室 / 策略看板 | 信任、精确、专业 | 观感较静态；用户不易感受金钱结果 | 保留第一版作为分析模式 |
| 赌场灯光 / 金库舞台 | 可感知的即时输赢、强记忆点 | 易让人混淆模拟与真实收益 | **V0.2 验证**，强制风险披露 |
| WebGL 粒子构成资金河 | 大规模钞票、深度、物理真实感更强 | 性能、设备兼容、调试成本高 | 待动效价值验证再引入 |
| 电影级原创摄影背景 + UI 合成 | 光影和材质真实；适合 Hero/揭幕 | 静态镜头不能承担动态结算事实；需要明确资产权属 | 下一轮可在确认布局后试用 |

## GitHub 候选技术（研究，不等于安装）

1. [pbakaus/radiant](https://github.com/pbakaus/radiant)：MIT，独立 Canvas/WebGL shader，无打包运行模式；适合高级舞台环境光和背景，不用于金额计算。
2. [pixijs-userland/particle-emitter](https://github.com/pixijs-userland/particle-emitter)：MIT，可精确控制资金粒子生命周期；它依赖 PixiJS 的上下文与版本，需要升级评估。
3. [PSCactux/webgl-shader-lab](https://github.com/PSCactux/webgl-shader-lab)：MIT，含 GPGPU curl flow、玻璃、金属和景深参照，适合 future VFX spike；依赖更重。
4. [Gaploid/stardust](https://github.com/Gaploid/stardust)：MIT，高密度 WebGL 粒子场；适合作为「从抽象粒子组成现金」的概念研究，不用于资产定价。
5. [cazala/party](https://github.com/cazala/party)：MIT，CPU/WebGPU 双运行时，适合交互性更高的物理现金场，但目前没必要将其整个运行时搬入产品。

以上仓库的 README 与 LICENSE 已经通过 GitHub 连接器核查；未复制他们的源码。未来要真的集成，须重新确认仓库版本、运行时依赖和第三方资产许可，做性能 benchmark 并写入归属记录。

## 视觉语法

- 所有「入账」「流失」根据确定性账面净值 delta 发令；动效不产生假资金。
- 音效只在用户允许后启用，不使用强迫观看或无限滚动的赌博强化机制。
- 视觉资源优先原创：本轮所有舞台元素和钞票形状均为 CSS/SVG 编码；没有复制真实美元的复杂防伪细节，也没有导入受版权保护的素材。
- 真实感分级：V0.2 是 2.5D 概念质感，不宣称实拍照片、真实 3D 资产或真实交易记录。
- 下一轮 A/B：用户能否在 5 秒内说出盈利、亏损、最后赢家及“模拟”的含义；与看板版对比。

## 设计工具现实约束

Figma 连接状态为 Starter 的 View seat，未获得可编辑 Design 席位。没有在 Figma 写入资产，也没有调用付费图像生成。此版本的 HTML/CSS/JS 是事实上的设计源，可供将来通过 Figma MCP 转化并逐屏对照。