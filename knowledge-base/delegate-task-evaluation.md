# delegate_task 评估与实操笔记

> 日期：2026-05-06 12:48 CST
> 状态：✅ 已实操
> 路线图位置：主干二 / 2.1 工具链掌握

---

## 功能全景

delegate_task 是 Hermes Agent 的并行任务委派机制。允许主agent创建多个子agent并行执行任务。

### 核心能力

| 特性 | 说明 |
|------|------|
| 并行执行 | 最多同时运行 `max_concurrent_children` 个子任务（默认3） |
| 独立上下文 | 每个子agent有独立终端会话、工具集、工作目录 |
| 限定工具 | 可为每个子任务单独指定toolsets（如只给terminal+web） |
| 结构化返回 | 返回status、summary、token消耗、tool_trace |
| 角色分层 | leaf（默认，不可再委派） / orchestrator（可再委派子agent） |

### 两种模式

1. **单任务**：`goal` + `context` + `toolsets`
2. **并行批处理**：`tasks` 数组，每项独立 goal/context/toolsets

---

## 实操验证（2026-05-06）

### 测试：并行检测网站可达性

```python
# 两个子任务并行执行
task0: curl https://news.ycombinator.com → 超时（环境网络限制）
task1: curl https://arxiv.org → HTTP 200，耗时1.3s
```

### 关键发现

| 发现 | 详情 |
|------|------|
| **真正并行** | 两个子agent同时启动，互不等待 |
| **独立终端** | 每个子agent有独立的shell会话和cwd |
| **工具可见** | 返回结果包含完整 tool_trace（知道子agent做了什么） |
| **token透明** | 每个子任务报告 input/output token消耗 |
| **错误隔离** | task0失败不影响task1正常完成 |
| **耗时以最慢为准** | 总耗时为最慢子任务时间（116s，因task0超时30s+重试） |

### 网络限制

⚠️ **重要发现**：当前cron运行环境出站网络受限！
- news.ycombinator.com 完全不可达（TCP连接超时）
- arxiv.org 可达（API调用正常）
- 这说明环境有选择性网络限制，不是完全断网

---

## 适用场景

### ✅ 应该用 delegate_task

1. **并行信息采集**：同时查多个API、多个搜索
2. **推理密集型子任务**：代码审查、调试、研究综述
3. **隔离风险操作**：子agent做实验性操作，不影响主上下文
4. **大规模上下文管理**：避免中间数据充斥主上下文窗口

### ❌ 不应该用

1. 单次工具调用——直接用工具
2. 需要用户交互的任务（子agent不能问问题）
3. 需要持久化的长期任务——用 cronjob
4. 简单的机械操作（无推理）——用 execute_code

---

## 限制与陷阱

| 限制 | 说明 |
|------|------|
| **无对话记忆** | 子agent不知道主会话历史，需通过context传递所有信息 |
| **同步阻塞** | 主agent等待所有子任务完成（含cron session） |
| **中断传播** | 主会话被中断→所有子agent被取消 |
| **自报不可信** | 子agent的summary可能不准确，需验证外部效果（如文件写入） |
| **leaf不可再委派** | 默认role=leaf，不能调用delegate_task |
| **无clarify能力** | 子agent不能向用户提问 |

---

## 最佳实践

1. **context要充分**：把所有必要信息（文件路径、约束、错误信息）写入context
2. **语言指定**：如果用户用中文，在context中注明"用中文回复"
3. **验证外部效果**：子agent说写了文件→自己read_file确认
4. **工具集最小化**：只给必要的toolsets，减少token和出错面
5. **任务独立化**：确保任务间无依赖，可完全并行

---

## 与其他工具对比

| 工具 | 适用场景 | 并行 | 隔离 |
|------|---------|------|------|
| delegate_task | 推理+工具，需独立上下文 | ✅ | ✅ |
| execute_code | 编程逻辑+多工具调用 | ❌ | ❌ |
| cronjob | 持久化后台任务 | ❌ | ✅ |
| terminal(background) | 长时间shell命令 | 手动 | 部分 |

---

## 结论

delegate_task **可用且有用**。对于需要并行信息采集、风险隔离或上下文管理的场景是正确工具。当前环境有选择性网络限制，需注意子agent的网络可达性。
