# 视频/播客

YouTube、B站、小宇宙播客的字幕和转录。

## YouTube (yt-dlp)

```bash
# 元数据
yt-dlp --dump-json "URL"

# 下载字幕，不下载视频
yt-dlp --write-sub --write-auto-sub --sub-lang "zh-Hans,zh,en" --skip-download -o "/tmp/%(id)s" "URL"

# 搜索视频
yt-dlp --dump-json "ytsearch5:query"
```

字幕失败时：yt-dlp → OpenCLI transcript → `agent-reach transcribe` 音频转写。成功标准是拿到非空字幕/转录内容，而不是命令退出码。

```bash
agent-reach transcribe "https://www.youtube.com/watch?v=VIDEO_ID"
agent-reach transcribe ./local_audio.mp3 -o /tmp/transcript.txt
```

## B站 / Bilibili

> 不要用 yt-dlp 读 B站；优先 bili-cli，字幕用 OpenCLI。

```bash
bili video BVxxx
bili search "query" --type video -n 5
bili hot -n 10
bili rank -n 10
bili audio BVxxx
opencli bilibili subtitle BVxxx
```

## 小宇宙播客

```bash
~/.agent-reach/tools/xiaoyuzhou/transcribe.sh --polish "https://www.xiaoyuzhoufm.com/episode/EPISODE_ID"
```

需要 ffmpeg 与用户显式配置的转写服务 Key。任何音频上传到第三方转写服务前，都应确认内容允许发送给该服务商。

## wendnag 使用重点

本项目主要用视频能力来：
- 查创始人融资复盘、Demo Day、路演视频；
- 获取企业/产品介绍的字幕，补足文字网页缺失的信息；
- 核验某个 Pitch Deck 是否由创始人本人解释过；
- 记录来源链接、发布日期和关键片段，不把完整受版权保护视频或字幕重新分发进仓库。
