# 多平台宣传视频深挖 — Checkpoint 02

日期：2026-09-23  
分支：`research/video-content-deep-dive-20260923`

## 目标

在 Checkpoint 01 和《多平台宣传内容增长逻辑与实验手册》基础上，进一步直接检查用户表格中的已发布视频链接，并引入相关题材的高热度/高互动公开视频作为对照样本。最终输出一份正式文档，重点回答：

1. 原视频实际上用了什么开头、画面、节奏、产品植入和 CTA；
2. 原视频高/低流量与内容结构之间有哪些可观察关系；
3. 同题材高热视频真正共用什么结构，而不是只抄标题或热点；
4. 哪些规律跨平台成立，哪些必须平台原生改写；
5. 下一轮应该如何做可证伪的内容实验。

## 已回读事实源

已从 `main` 重新读取：
- `06-analysis/marketing-video-platform-research/README.md`
- `06-analysis/marketing-video-platform-research/2026-09-23-checkpoint-01.md`
- `06-analysis/marketing-video-platform-research/多平台宣传内容增长逻辑与实验手册.md`

继续沿用证据层级：第一方数据 > 平台/监管官方材料 > 学术研究 > 公开高热样本 > 经验性观点。

## 用户表格中的可访问链接清单

### 2026-06-15 — 宠物/交友个人站
- 小红书：https://xhslink.cn/o/8TkVRmKKrF
- 抖音：https://v.douyin.com/1K9W0DPXTLk/
- 快手：https://v.kuaishou.com/K72MuhI9
- 视频号：https://weixin.qq.com/sph/ANJCECUH3B
- 表内浏览量：58 / 371 / 182 / 289

### 2026-06-16 — AI Agent × 金融分析
- 小红书：https://xhslink.cn/o/4WOsmCGw9rY
- 抖音：https://v.douyin.com/iIlQN970zYE/
- 快手：https://v.kuaishou.com/njcJZm1T
- 视频号：https://weixin.qq.com/sph/AOmaOSklFH
- 表内浏览量：220 / 10,002 / 79 / 514

### 2026-06-17 — AI Agent × 金融数据通道
- 小红书：https://xhslink.cn/o/P7lrkfJcQP
- 抖音：https://v.douyin.com/Qt2PcG-mF3c/
- 快手：https://v.kuaishou.com/Jn7T9JDc
- 视频号：https://weixin.qq.com/sph/AQmWRuHsGF
- 表内浏览量：185 / 8,475 / 131 / 237

### 2026-06-19 凌晨 — AI Agent × 金融分析
- 小红书：https://xhslink.cn/o/3klOx76ahZs
- 抖音：https://v.douyin.com/bGF3BJdJ9LY/
- 快手：https://v.kuaishou.com/nUbXP6Ht
- 视频号：https://weixin.qq.com/sph/AdayDa8Zni
- 表内浏览量：173 / 1,271 / 132 / 222

### 2026-06-19 晚间 — AI Agent × 金融分析/积极封面
- 小红书：https://xhslink.cn/o/2cm8mrkrBpj
- 抖音：https://v.douyin.com/I5KkpBlXrSg/
- 快手：https://v.kuaishou.com/KdtJ9SWP
- 视频号：https://weixin.qq.com/sph/AzrU0FWLCe
- 表内浏览量：1,105 / 11,100 / 2 / 428

## 当前访问状态

- 当前对话的通用 Web 访问与本地容器对上述国内平台短链存在 DNS/反爬限制，不能把“打不开”解释成视频不存在。
- 已开始改用 GitHub 上可复现的公开视频解析工具，并计划使用 GitHub Actions 的网络环境做小规模、仅限上述用户提供链接的研究性解析。
- 不做大规模抓取，不绕过付费墙，不处理 DRM 或会员专享内容。

## 工具筛选结论

### 首选：zyipeng/video-downloader
- MIT License。
- 支持抖音、小红书、快手等 9 个平台。
- 抖音与快手有自研 SSR 分享页解析；小红书走 yt-dlp。
- 提供 probe（只解析元数据，不下载）和低清/兼容模式下载。
- 适合作为本轮小规模研究工具。

### 不采用：NanmiCoder/MediaCrawler
- 功能强，支持小红书/抖音/快手关键词、帖子、评论和媒体下载。
- 但许可证是 NON-COMMERCIAL LEARNING LICENSE 1.1，明确限制商业用途。
- 本任务服务于商业宣传研究，因此不执行其代码，仅把其能力作为工具生态参考。

### 其他备选
- jiji262/douyin-downloader：MIT，但其 README 明确提示当前抖音单条 CLI 下载受请求校验阻断，不作为首选。
- JoeanAmier/KS-Downloader：GPL-3.0，可处理快手分享链接，作为快手降级方案。
- JoeanAmier/XHS-Downloader：GPL-3.0，可处理小红书分享链接，作为小红书降级方案。

## 已发现的交叉平台线索

公开搜索索引中已发现与表格同一创作者/同一标题体系的 Bilibili 内容：
- “vibecoding 这个金融分析师只要我们问的详细就越全面”，创作者显示为“Git菌”，约 45 秒；搜索快照中的播放数随抓取时间变化，因此只作为存在性与结构线索，不把快照数字当稳定事实。
- “vibecoding 每个人都可以拥有自己的金融分析团队”，同样显示为“Git菌”，约 44 秒。这个标题从“一个金融分析师”升级为“每个人拥有自己的金融分析团队”，更清晰地表达用户收益，值得作为后续结构比较对象。

## 下一步

1. 在本分支添加临时 GitHub Actions workflow，对 5 组抖音/快手/小红书短链做 probe，并在允许时下载低清研究副本。
2. 将解析元数据、失败日志和媒体作为临时 artifact；不把第三方/平台视频二进制提交进仓库。
3. 对成功取得的视频抽取少量代表帧进行镜头/信息结构分析。
4. 搜索 AI Agent、vibe coding、AI办公/B2B产品演示、AI金融分析等高热公开视频，记录公开互动指标快照和结构，不复制受版权保护内容。
5. 在完成第一批直接视频观察后立即更新 Checkpoint 03，并从 GitHub 重新读取，再继续综合。
