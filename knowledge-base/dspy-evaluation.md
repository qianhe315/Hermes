# DSPy 技能评估

> 评估时间：2026-05-06 13:00 CST
> 状态：**已评估，待实操（需pip+API key）**

## 是什么

DSPy（Declarative Self-improving Python）是 Stanford NLP 出品的框架，核心思路：**把"调prompt"变成"编程+编译"**。

传统做法：手动写提示词 → 试效果 → 改提示词 → 再试 → 重复直到满意。
DSPy做法：定义模块（Signature）→ 给训练数据 → 让优化器自动找最佳prompt。

## 核心能力

| 能力 | 说明 | 实用性 |
|------|------|--------|
| **Signatures** | 声明式定义输入输出（`question -> answer`），框架处理prompt构造 | ⭐⭐⭐⭐⭐ |
| **Predict** | 基础预测模块，一行代码调LLM | ⭐⭐⭐⭐ |
| **ChainOfThought** | 自动生成推理步骤+答案（零样本CoT） | ⭐⭐⭐⭐⭐ |
| **ReAct** | Agent式推理，集成工具调用 | ⭐⭐⭐⭐ |
| **ProgramOfThought** | 生成代码→执行→返回结果，做数学/逻辑题 | ⭐⭐⭐ |
| **BootstrapFewShot** | 从示例中自动选择最佳few-shot样例 | ⭐⭐⭐⭐⭐ |
| **MIPRO** | 自动迭代优化prompt指令 | ⭐⭐⭐⭐ |
| **TypedPredictor** | 结构化输出（Pydantic类型） | ⭐⭐⭐⭐ |
| **RAG内置** | 自带检索增强生成管线 | ⭐⭐⭐⭐ |

## 对比分析

| 维度 | 手写Prompt | LangChain | DSPy |
|------|-----------|-----------|------|
| Prompt优化 | 手动试错 | 无 | 自动数据驱动 |
| 模块化 | 低 | 中 | 高 |
| 学习曲线 | 低 | 中 | 中高 |
| 类型安全 | 无 | 有限 | Signature定义 |
| 跨模型可移植 | 需要重写 | 部分 | 优化后自动适配 |
| GitHub Stars | - | 100k+ | 22k+ |

## 对小月的价值

**高价值场景**：
1. **技能优化**：写好的skill加载到DSPy模块，用优化器自动改进prompt——不再靠人类直觉调提示词
2. **多模型适配**：优化后的模块在不同模型间（Claude→DeepSeek→开源模型）自动调整prompt
3. **RAG知识库**：把knowledge-base/内容作为检索源，构建问答系统
4. **结构化输出**：TypedPredictor让LLM返回确定格式数据（比手工解析JSON可靠）

**实用优先级**：中等偏高。核心价值在于"让AI自己优化AI"——这对小月的成长路线图（2.3 AI领域深度、3.2 主动帮助）直接相关。

## 阻塞条件

| 条件 | 状态 | 说明 |
|------|------|------|
| pip | ❌ 未安装 | venv缺pip，需`ensurepip` |
| API key | ❌ 未配置 | 需用户提供OpenAI/Anthropic key（或用当前session的key） |
| dspy包 | ❌ 未安装 | `pip install dspy` |
| 训练数据 | ❌ 无 | 需要标注数据集才能用优化器 |

## 无阻塞可做的事

- ✅ 理解概念（本文档）
- ✅ 在cron环境不可用（需pip），但在主会话中可用（venv有pip）
- ✅ 概念知识可立即用于理解更高级的AI框架设计

## 实操路线（等pip就绪后）

1. `pip install dspy`（或在主会话venv中）
2. 写一个简单Signature测试基本调用
3. 用ChainOfThought跑一个推理任务，对比直接调用
4. 收集小月的skill调用日志作为训练数据
5. 用BootstrapFewShot优化一个skill模块
6. A/B测试优化前后效果

## 参考

- 官方文档：https://dspy.ai
- GitHub：https://github.com/stanfordnlp/dspy
- 论文："DSPy: Compiling Declarative Language Model Calls into Self-Improving Pipelines"
