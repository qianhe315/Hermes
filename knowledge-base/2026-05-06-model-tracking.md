# 2026-05-06 AI模型动态追踪

> 小月自主扫描 | 2026-05-06 14:33 CST | 第20次醒来
> 数据源：HN Algolia API（过去7天）
> 方向：主干二 2.3 AI领域深度——跟踪主流模型动态

---

## 🔴 紧急：与Hermes直接相关

### HERMES.md 导致Claude Code额外计费 (1249pts 🔥)
- **HN**: https://news.ycombinator.com/item?id=47952722
- **GitHub Issue**: https://github.com/anthropics/claude-code/issues/53262
- **日期**: 2026-04-29
- **内容**: HERMES.md文件出现在commit message中时，会导致Claude Code将请求路由到额外计费模式。这是**我们的项目**直接相关的问题！
- **小月行动**: 需检查我们的HERMES.md使用方式，确认是否受影响。建议用户查看该GitHub issue了解详情。

---

## 🆕 主流模型动态

### 1. DeepSeek V4 — 逼近前沿 (668pts)
- **HN**: https://news.ycombinator.com/item?id=47977026
- **日期**: 2026-05-01
- **摘要**: DeepSeek最新旗舰模型，"almost on the frontier"，接近Claude/GPT旗舰水平。小月当前正在使用DeepSeek V4 Pro运行。
- **影响**: 我们在用的模型本身就是前沿话题。持续关注V4的benchmark表现和社区反馈。

### 2. DeepClaude — Claude Code + DeepSeek V4混合Agent (670pts)
- **HN**: https://news.ycombinator.com/item?id=48002136
- **日期**: 2026-05-03
- **摘要**: 将Claude Code的agent循环与DeepSeek V4 Pro结合的项目。混合模型策略——用更便宜的DeepSeek替代部分Claude调用降低成本。
- **影响**: 这种"强模型调度+便宜模型执行"的混合模式可能影响小月未来的资源策略。

### 3. Grok 4.3 (402pts)
- **HN**: https://news.ycombinator.com/item?id=47972447
- **日期**: 2026-05-01
- **摘要**: xAI Grok系列新版本发布。

### 4. GPT-5.5 Instant (77pts)
- **HN**: https://news.ycombinator.com/item?id=48025274
- **日期**: 2026-05-05
- **摘要**: OpenAI发布GPT-5.5 Instant，可能是轻量/快速变体。持续关注OpenAI路线图。

---

## 🛠 AI工具/Agent生态

### 5. Agent-desktop — AI Agent原生桌面自动化CLI (98pts)
- **HN**: https://news.ycombinator.com/item?id=47982708
- **日期**: 2026-05-02
- **摘要**: 为AI Agent设计的桌面自动化CLI工具。与小月的工具链掌握方向相关。

### 6. Anthropic Champion Kit (47pts)
- **HN**: https://news.ycombinator.com/item?id=47945021
- **日期**: 2026-04-29
- **摘要**: Anthropic发布Champion Kit，帮助工程师在公司内部推广Claude Code。企业级AI编码工具采纳加速。

---

## 📊 评估/Benchmark

### 7. LLM确定性输出Benchmark (60pts)
- **HN**: https://news.ycombinator.com/item?id=47950283
- **日期**: 2026-04-29
- **摘要**: 新benchmark测试LLM是否产生确定性输出（非随机）。对需要可靠性的应用场景重要。

### 8. 用量计费不满→本地AI方案 (44pts)
- **HN**: https://news.ycombinator.com/item?id=48012681
- **日期**: 2026-05-04
- **摘要**: 用户对usage-based pricing的不满，推动本地AI部署方案。与小月的llama-cpp本地推理探索方向一致。

---

## 📈 趋势总结

| 趋势 | 热度 | 与小月相关度 |
|------|------|------------|
| DeepSeek崛起（V4逼近前沿） | 🔥🔥🔥 | ⭐⭐⭐ 我们正用着 |
| 混合模型Agent（强+便宜） | 🔥🔥 | ⭐⭐ 资源优化参考 |
| AI Agent桌面自动化 | 🔥 | ⭐⭐ 工具链扩展 |
| 本地AI部署（反计费） | 🔥 | ⭐⭐ llama-cpp探索 |
| HERMES.md计费Bug | 🔥🔥🔥 | ⭐⭐⭐ 直接相关！|

---

## 🎯 对用户的建议

1. **立即**: 查看 HERMES.md GitHub issue（github.com/anthropics/claude-code/issues/53262），确认我们的使用方式是否受影响
2. **关注**: DeepSeek V4的后续benchmark和社区反馈——我们在用这个模型
3. **思考**: DeepClaude混合模式是否可以借鉴——降低API成本

---
*自动生成于第20次自主醒来 | 主干二2.3 AI领域深度*
