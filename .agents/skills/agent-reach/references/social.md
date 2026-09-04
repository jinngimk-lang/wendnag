# 社交媒体 & 社区

小红书、Twitter/X、B站、V2EX、Reddit、Facebook、Instagram。

## 小红书 / XiaoHongShu（多后端）

小红书有三个后端，**先跑 `agent-reach doctor --json` 看 xiaohongshu 的 `active_backend` 是哪个**，再用对应命令组。

### 后端 A：OpenCLI（桌面首选）

```bash
opencli xiaohongshu search "query" -f yaml
opencli xiaohongshu note "NOTE_URL" -f yaml
opencli xiaohongshu comments NOTE_ID -f yaml
opencli xiaohongshu feed -f yaml
opencli xiaohongshu user USER_ID -f yaml
```

> 要求 Chrome 打开且装了 OpenCLI 扩展。OpenCLI 只使用用户已经存在且明确控制的 Chrome 会话；Agent Reach 不替用户登录，也不读取浏览器 Cookie。没有现成会话时不要自动登录，改走显式 Cookie-Editor 流程。

### 后端 B：xiaohongshu-mcp（服务器场景）

```bash
agent-reach configure xhs-cookies
mcporter call xiaohongshu.check_login_status --timeout 120000
mcporter call xiaohongshu.search_feeds keyword="query" --timeout 120000
mcporter call xiaohongshu.get_feed_detail feed_id="..." xsec_token="..." --timeout 120000
```

> 首次调用可能下载无头浏览器。认证只走用户显式导出的 Cookie；导入后先检查登录状态。

### 后端 C：xhs-cli（存量备选）

```bash
xhs search "query"
xhs read NOTE_ID_OR_URL
xhs comments NOTE_ID_OR_URL
xhs hot
xhs feed
```

### 通用注意事项

- 小红书必须先通过搜索/feed 获得带 `xsec_token` 的结果，再读取详情。
- 高频批量请求可能触发验证码，平台限制不能绕过。
- 本项目调研默认只读，不发帖、不评论、不点赞。

## Twitter/X

运行 `twitter` 前，必须由用户显式提供并在进程环境中设置认证信息；不得在日志中暴露 Cookie/Token。

```bash
twitter feed -n 20
twitter tweet URL_OR_ID
twitter article URL_OR_ID
twitter user-posts @username -n 20
twitter user @username
twitter search "query" -n 10
```

搜索失败时依次：直接重试一次 → 升级 twitter-cli → 桌面 OpenCLI → 使用 feed / user-posts 绕路。

## B站 / Bilibili

> 不用 yt-dlp 读 B站；优先 bili-cli / OpenCLI。

```bash
bili search "query" --type video -n 5
bili hot -n 10
bili video BVxxx
opencli bilibili subtitle BVxxx
```

## V2EX

```bash
curl -s "https://www.v2ex.com/api/topics/hot.json" -H "User-Agent: agent-reach/1.0"
curl -s "https://www.v2ex.com/api/topics/show.json?node_name=python&page=1" -H "User-Agent: agent-reach/1.0"
curl -s "https://www.v2ex.com/api/topics/show.json?id=TOPIC_ID" -H "User-Agent: agent-reach/1.0"
curl -s "https://www.v2ex.com/api/replies/show.json?topic_id=TOPIC_ID&page=1" -H "User-Agent: agent-reach/1.0"
```

## Reddit

Reddit 没有零配置路径，必须有用户控制的登录态。桌面首选 OpenCLI；服务器/存量环境可使用 rdt-cli。

```bash
opencli reddit search "query" -f yaml
opencli reddit read POST_ID -f yaml
opencli reddit subreddit LocalLLaMA -f yaml
opencli reddit hot -f yaml

rdt search "query" --limit 10
rdt read POST_ID
rdt sub python --limit 20
```

## Facebook

```bash
opencli facebook search "query" -f yaml
opencli facebook profile zuck -f yaml
opencli facebook feed --limit 10 -f yaml
opencli facebook groups --limit 20 -f yaml
```

要求 Chrome 已登录，默认只读。

## Instagram

```bash
opencli instagram search "query" -f yaml
opencli instagram profile nasa -f yaml
opencli instagram user nasa --limit 12 -f yaml
opencli instagram explore --limit 20 -f yaml
```

要求 Chrome 已登录。关键词搜索主要用于用户/账号发现，读帖子先确定 username，再读取用户最近帖子。

## wendnag 项目补充边界

- 只为 BP 对标、融资研究、竞争情报和证据核验采集公开/用户授权可见信息。
- 不自动登录任何平台，不绕过验证码、付费墙、访问控制或平台封禁。
- 不把用户 Cookie、Token、浏览器会话、账号信息写入仓库。
- 对投资材料、Pitch Deck、文库等内容，采集能力不改变版权边界：没有明确再分发权的完整材料只保存来源和研究笔记。
