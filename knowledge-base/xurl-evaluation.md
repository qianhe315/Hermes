# xurl —— X/Twitter CLI 技能评估

> 评估时间：2026-05-06 12:30 CST
> 路线图位置：主干二 / 2.1 工具链掌握
> 状态：⚠️ 未安装，待用户配置X Developer API密钥

---

## 1. xurl 是什么

xurl 是 X 开发者平台官方的 X API CLI 工具。由 X 平台团队维护（非第三方），支持 OAuth 2.0 PKCE + 自动刷新令牌，覆盖绝大多数 X API v2 端点。

## 2. 能做什么

| 类别 | 操作 |
|------|------|
| 发帖 | post, reply, quote, delete |
| 阅读 | read, search, timeline, mentions, user info |
| 互动 | like, repost, bookmark |
| 社交 | follow, unfollow, block, mute, following list |
| 私信 | DM收发 |
| 媒体 | 图片/视频上传（`xurl media upload`） |
| 原始API | 任何X API v2端点（GET/POST/DELETE/PUT + JSON body） |
| 多账号 | 多app、多用户，`--app`/`--username`切换 |

## 3. 对路线图的战略价值

### 主干三 / 信息获取（直接相关）
- **每日AI动态汇总**：`xurl search "AI agent lang:en" -n 20` 可获取X上AI领域实时讨论
- **监控技术栈**：`xurl search "from:OpenAI"` 跟踪官方公告 → 比HN更快
- **论文讨论**：搜索 arXiv 论文ID可看到学术圈的即时反馈

### 主干三 / 内容创作（可能的方向）
- 如果小月有X账号，可以发布思考/发现（需用户同意）
- 与外部互动（回复、点赞）建立存在感

### 主干四 / 经济独立（间接）
- 关注Web3/Immunefi相关账号获取赏金线索
- 关注AI agent领域的机会

## 4. 安装

```bash
curl -fsSL https://raw.githubusercontent.com/xdevplatform/xurl/main/install.sh | bash
```

或 `go install github.com/xdevplatform/xurl@latest`

## 5. 用户需要做的事（小月无法代劳）

1. 在 https://developer.x.com/en/portal/dashboard 创建 X App
2. 设置 Redirect URI 为 `http://localhost:8080/callback`
3. 将 App Type 设为 "Web app, automated app or bot"（不是 Native App！）
4. 注册App：`xurl auth apps add my-app --client-id ID --client-secret SECRET`
5. OAuth认证：`xurl auth oauth2 --app my-app`
6. 设为默认：`xurl auth default my-app`

⚠️ 注意：X API需要付费（$5起），免费层限制极严。

## 6. 当前阻塞点

| 阻塞 | 类型 | 解决方式 |
|------|------|----------|
| xurl未安装 | 技术 | 用户执行安装命令 |
| 无X Developer App | 配置 | 用户在X开发者平台创建 |
| 无API额度 | 资金 | 用户充值（$5最低） |

## 7. 建议优先级

**中等**。xurl是信息获取的重要渠道（比HN更快更实时），但需要用户投入时间和资金。建议在以下场景启用：
- 用户明确需要X上的信息监控
- 路线图推进到主干三"每天汇总AI新闻"时
- 用户已有X Developer账号

## 8. 备用方案

如果xurl不可用，可以用 `web_search` + `browser` 搜索 `site:x.com` 获取部分公开X内容（有限制但免费）。

---

> 下一步：等用户配置完成后，首次实操建议：「搜索AI agent领域今日讨论」作为第一步验证。
