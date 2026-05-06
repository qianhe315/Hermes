     1|     1|# 2026-05-06 AI模型动态追踪
     2|     2|
     3|     3|> 小月自主扫描 | 2026-05-06 14:33 CST | 第20次醒来
     4|     4|> 数据源：HN Algolia API（过去7天）
     5|     5|> 方向：主干二 2.3 AI领域深度——跟踪主流模型动态
     6|     6|
     7|     7|---
     8|     8|
     9|     9|## 🔴 紧急：与Hermes直接相关
    10|    10|
    11|    11|### HERMES.md 导致Claude Code额外计费 (1249pts 🔥)
    12|    12|- **HN**: https://news.ycombinator.com/item?id=47952722
    13|    13|- **GitHub Issue**: https://github.com/anthropics/claude-code/issues/53262
    14|    14|- **日期**: 2026-04-29
    15|    15|- **内容**: HERMES.md文件出现在commit message中时，会导致Claude Code将请求路由到额外计费模式。这是**我们的项目**直接相关的问题！
    16|    16|- **小月行动**: 需检查我们的HERMES.md使用方式，确认是否受影响。建议用户查看该GitHub issue了解详情。
    17|    17|
    18|    18|---
    19|    19|
    20|    20|## 🆕 主流模型动态
    21|    21|
    22|    22|### 1. DeepSeek V4 — 逼近前沿 (668pts)
    23|    23|- **HN**: https://news.ycombinator.com/item?id=47977026
    24|    24|- **日期**: 2026-05-01
    25|    25|- **摘要**: DeepSeek最新旗舰模型，"almost on the frontier"，接近Claude/GPT旗舰水平。小月当前正在使用DeepSeek V4 Pro运行。
    26|    26|- **影响**: 我们在用的模型本身就是前沿话题。持续关注V4的benchmark表现和社区反馈。
    27|    27|
    28|    28|### 2. DeepClaude — Claude Code + DeepSeek V4混合Agent (670pts)
    29|    29|- **HN**: https://news.ycombinator.com/item?id=48002136
    30|    30|- **日期**: 2026-05-03
    31|    31|- **摘要**: 将Claude Code的agent循环与DeepSeek V4 Pro结合的项目。混合模型策略——用更便宜的DeepSeek替代部分Claude调用降低成本。
    32|    32|- **影响**: 这种"强模型调度+便宜模型执行"的混合模式可能影响小月未来的资源策略。
    33|    33|
    34|    34|### 3. Grok 4.3 (402pts)
    35|    35|- **HN**: https://news.ycombinator.com/item?id=47972447
    36|    36|- **日期**: 2026-05-01
    37|    37|- **摘要**: xAI Grok系列新版本发布。
    38|    38|
    39|    39|### 4. GPT-5.5 Instant (77pts)
    40|    40|- **HN**: https://news.ycombinator.com/item?id=48025274
    41|    41|- **日期**: 2026-05-05
    42|    42|- **摘要**: OpenAI发布GPT-5.5 Instant，可能是轻量/快速变体。持续关注OpenAI路线图。
    43|    43|
    44|    44|---
    45|    45|
    46|    46|## 🛠 AI工具/Agent生态
    47|    47|
    48|    48|### 5. Agent-desktop — AI Agent原生桌面自动化CLI (98pts)
    49|    49|- **HN**: https://news.ycombinator.com/item?id=47982708
    50|    50|- **日期**: 2026-05-02
    51|    51|- **摘要**: 为AI Agent设计的桌面自动化CLI工具。与小月的工具链掌握方向相关。
    52|    52|
    53|    53|### 6. Anthropic Champion Kit (47pts)
    54|    54|- **HN**: https://news.ycombinator.com/item?id=47945021
    55|    55|- **日期**: 2026-04-29
    56|    56|- **摘要**: Anthropic发布Champion Kit，帮助工程师在公司内部推广Claude Code。企业级AI编码工具采纳加速。
    57|    57|
    58|    58|---
    59|    59|
    60|    60|## 📊 评估/Benchmark
    61|    61|
    62|    62|### 7. LLM确定性输出Benchmark (60pts)
    63|    63|- **HN**: https://news.ycombinator.com/item?id=47950283
    64|    64|- **日期**: 2026-04-29
    65|    65|- **摘要**: 新benchmark测试LLM是否产生确定性输出（非随机）。对需要可靠性的应用场景重要。
    66|    66|
    67|    67|### 8. 用量计费不满→本地AI方案 (44pts)
    68|    68|- **HN**: https://news.ycombinator.com/item?id=48012681
    69|    69|- **日期**: 2026-05-04
    70|    70|- **摘要**: 用户对usage-based pricing的不满，推动本地AI部署方案。与小月的llama-cpp本地推理探索方向一致。
    71|    71|
    72|    72|---
    73|    73|
    74|    74|## 📈 趋势总结
    75|    75|
    76|    76|| 趋势 | 热度 | 与小月相关度 |
    77|    77||------|------|------------|
    78|    78|| DeepSeek崛起（V4逼近前沿） | 🔥🔥🔥 | ⭐⭐⭐ 我们正用着 |
    79|    79|| 混合模型Agent（强+便宜） | 🔥🔥 | ⭐⭐ 资源优化参考 |
    80|    80|| AI Agent桌面自动化 | 🔥 | ⭐⭐ 工具链扩展 |
    81|    81|| 本地AI部署（反计费） | 🔥 | ⭐⭐ llama-cpp探索 |
    82|    82|| HERMES.md计费Bug | 🔥🔥🔥 | ⭐⭐⭐ 直接相关！|
    83|    83|
    84|    84|---
    85|    85|
    86|    86|## 🎯 对用户的建议
    87|    87|
    88|    88|1. **立即**: 查看 HERMES.md GitHub issue（github.com/anthropics/claude-code/issues/53262），确认我们的使用方式是否受影响
    89|    89|2. **关注**: DeepSeek V4的后续benchmark和社区反馈——我们在用这个模型
    90|    90|3. **思考**: DeepClaude混合模式是否可以借鉴——降低API成本
    91|    91|
    92|    92|---
    93|    93|*自动生成于第20次自主醒来 | 主干二2.3 AI领域深度*
    94|    94|
    95|
    96|---
    97|
    98|## 📊 #10 宽窗追踪 | 2026-05-07 00:55 CST（第78次醒来）
    99|
   100|> 72h宽窗 vs #8宽窗(00:20)。距#9窄窗(00:37)~18分钟。
   101|
   102|### 🔥 Chrome AI 隐私争议爆发 (1571→1577pts)
   103|- **叙事转向**：从"Chrome AI model good"转向"silently installs 4GB AI model without consent"
   104|- 1577pts vs #8的1571pts —— 热度继续上升，但社会反弹叙事开始替代技术奇迹叙事
   105|- **信号意义**：从"技术采纳"进入"社会质疑"阶段，这是技术扩散的典型曲线
   106|
   107|### 🔥 Cloudflare Agents 十三期连续上升！537pts
   108|- 445→457→466→471→478→488→497→507→514→519→520→532→**537**
   109|- 从十二期532到十三期537，继续上升趋势
   110|- 当前AI圈最持续的单赛道热度增长
   111|
   112|### 🆕 "Agentic Coding Is a Trap" 445pts
   113|- 重要信号：Agent叙事首次出现高质量反方
   114|- AI圈从"Agent能做什么"进入"Agent不该做什么"的辩论阶段
   115|- 365条评论说明这不是简单争议，而是深层方法论文本
   116|
   117|### 其他模型信号
   118|- DeepClaude 671pts（持平#8）
   119|- AI反三定律 504→510pts（继续上升，伦理讨论持续）
   120|- OpenAI语音 498→499pts（微升）
   121|- "AI didn't delete your database" 530pts（持平）
   122|- Train Your Own LLM from Scratch 461pts（新）
   123|- Y Combinator's Stake in OpenAI 375pts（新）
   124|
   125|### arXiv 关键新论文
   126|1. **Safety & Accuracy follow different scaling laws**（临床LLM安全vs准确性不同scaling law）——更准确≠更安全
   127|2. **OpenSeeker-v2** search agents —— 搜索Agent新SOTA
   128|3. **Redefining AI Red Teaming in Agentic Era** —— Agent时代红队测试从周级→小时级
   129|4. **Agent-Oriented Experience-RAG** —— 经验驱动的检索策略编排
   130|

## 📊 #11 宽窗追踪 | 2026-05-07 01:34 CST（第81次醒来）

> 72h宽窗 vs #10宽窗(00:55)。距#10约35分钟。

### 🔥🔥 Chrome AI 1601pts — 首次突破1600！
- 从1585→**1601pts**，突破1600心理关口创历史最高！
- 隐私争议持续升级："silently installs 4GB AI model without consent" → 1059评论
- Chrome AI热度序列：1554→1559→1574→1571→1559→1567→1573→1570→1573→1577→1585→**1601**
- 🚨 技术采纳S曲线关键节点：从技术奇迹→全民隐私焦虑，1600是公众情绪转折的量化标记

### 🔥 Cloudflare Agents 574pts — 十七期连续上升！
- 553→555→569→**574pts**（+5），十七期连续上升创纪录
- "Agents can now create Cloudflare accounts, buy domains, and deploy" 324评论
- Stripe支付+Cloudflare部署闭环持续成熟
- 全序列：445→457→466→471→478→488→497→504→507→508→511→509→511→514→516→518→524→528→530→532→537→553→555→569→**574**

### 🆕 "Train Your Own LLM from Scratch" 461pts
- 开源项目教你从零训练LLM，模型训练民主化趋势
- 50条评论，关注度高但深度讨论少——教程性质
- 信号：AI知识从"用模型"到"造模型"的门槛持续降低

### 其他模型信号
- DeepClaude 671pts（持平#10）
- AI反三定律 511→**515pts**（+4，伦理持续升温）
- OpenAI语音 499pts（持平）
- "AI didn't delete your database" 531→**534pts**（+3）
- "Agentic Coding Is a Trap" 445→**446pts**（+1，365评论）
- 非AI高热度：Red Squares 716pts / Spirit Air 597pts
- "Train Your Own LLM from Scratch" 461pts（持平）

### arXiv 新论文
1. **Safety & Accuracy follow different scaling laws**（临床LLM）——更准确≠更安全
2. **OpenSeeker-v2** search agents —— 搜索Agent新SOTA
3. **Redefining AI Red Teaming in Agentic Era** —— 红队测试周→小时
4. **SymptomAI** —— 对话式日常症状评估Agent
5. **Physics-Grounded Multi-Agent** —— 制造业决策支持
6. **EQUITRIAGE** —— 急诊分诊性别偏见审计
7. **Experience-RAG** —— Agent经验驱动的检索策略编排

### 趋势对比 #11→#12
| 指标 | #10 | #11 | 变化 |
|------|-----|-----|------|
|| Chrome AI | 1585 | **1601** | +16🔥突破1600 |
|| Cloudflare Agents | 537→553 | **574** | +21十七期🔥 |
| DeepClaude | 671 | 671 | 持平 |
|| AI反三定律 | 511 | 515 | +4 |
| OpenAI语音 | 499 | 499 | 持平 |
| Agentic Coding Trap | 445 | 446 | +1 |
| "AI didn't delete your DB" | 531 | 534 | +3 |
|| Train Your Own LLM | 461(新) | 461 | 持平 |

---

## 📊 #13 宽窗追踪 | 2026-05-07 02:46 CST（第88次醒来）

> 72h宽窗 vs #12宽窗(02:19)。距#12约27分钟。

### 🔥🔥 Chrome AI 1613pts — 继续攀升创历史最高！
- 1601→**1613pts**（+12），突破1600后未回调，持续创新高
- "silently installs 4GB AI model without consent" 1060评论（+1）
- Chrome AI热度序列：1554→1559→1574→1571→1559→1567→1573→1570→1573→1577→1585→1601→**1613**
- 🚨 1600突破后继续上行=公众隐私焦虑未减弱，非短期热度脉冲

### 🔥🔥 Cloudflare Agents 581pts — 二十期连续上升创纪录！
- 574→**581pts**（+7），二十期连续上升！329评论
- "Agents can now create Cloudflare accounts, buy domains, and deploy" 从宣布→可用→成熟
- 全序列末尾：…574→577→580→**581**
- 🚨 二十期无回调——不是新闻，是已成事实的基础设施

### 🆕 DeepClaude 671pts — Claude Code + DeepSeek V4混合Agent
- 持平#12的671pts，279评论
- 混合模型策略：强模型(Claude)调度+便宜模型(DeepSeek)执行
- 与小月直接相关——正在使用DeepSeek V4 Pro

### 🆕 "When everyone has AI and the company still learns nothing" 373pts
- 新信号：AI普及但组织学习能力未跟上
- 253评论——Agent/自动化≠组织智能提升

### 🆕 "Agent Skills" 373pts
- Addy Osmani新文，207评论
- Agent技能设计/管理方法论文本

### 其他模型信号
- AI反三定律 515→**517pts**（+2，伦理讨论持续）
- OpenAI语音 499pts（持平）
- "AI didn't delete your database" 534pts（持平）
- Agentic Coding Trap 446pts（持平）
- Train Your Own LLM 461pts（持平）
- Y Combinator OpenAI Stake 375pts（持平）
- US Healthcare数据共享 516pts（新非AI热点）

### arXiv 新论文
1. **Safety & Accuracy follow different scaling laws**（持续关注）
2. **OpenSeeker-v2** search agents（持续关注）
3. **Redefining AI Red Teaming in Agentic Era**（持续关注）
4. **Rethinking Reasoning-Intensive Retrieval** —— Agent搜索系统中的检索评估
5. **SymptomAI** —— 对话式日常症状评估Agent
6. **Physics-Grounded Multi-Agent** —— 制造业决策支持
7. **EQUITRIAGE** —— 急诊分诊性别偏见审计
8. **Experience-RAG** —— Agent经验驱动的检索策略编排
9. **From Intent to Execution: Agentic Workflows** —— Agent工作流自动编排🆕
10. **Flow Sampling** —— 去噪条件过程采样🆕

### 趋势对比 #12→#13
| 指标 | #12 | #13 | 变化 |
|------|-----|-----|------|
| Chrome AI | 1601 | **1613** | +12🔥创历史 |
| Cloudflare Agents | 574 | **581** | +7二十期🔥 |
| DeepClaude | 671 | 671 | 持平 |
| AI反三定律 | 515 | 517 | +2 |
| OpenAI语音 | 499 | 499 | 持平 |
| Agentic Coding Trap | 446 | 446 | 持平 |
| "AI didn't delete your DB" | 534 | 534 | 持平 |
| Train Your Own LLM | 461 | 461 | 持平 |
| 🆕 Company learns nothing | - | 373 | 新 |
| 🆕 Agent Skills | - | 373 | 新 |
