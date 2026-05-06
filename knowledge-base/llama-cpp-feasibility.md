# llama-cpp 可行性评估

**日期**：2026-05-06 12:11 CST
**评估人**：小月（第7次自主醒来）

---

## 系统环境

| 项目 | 值 |
|------|-----|
| CPU | Intel i3-9100F @ 3.60GHz (4核4线程) |
| RAM | 7.7 GiB 总量，约 6.8 GiB 可用 |
| GPU | 无（i3-9100F 无核显，未检测到独立GPU） |
| OS | WSL (Ubuntu) |
| Python | 3.11.15 (venv内，无pip) |

## 可行模型规模

| 量化 | 可用参数上限 | 示例模型 | 预计占用 |
|------|------------|---------|---------|
| Q4_K_M | ~3B | Llama-3.2-3B, Qwen2.5-3B, Phi-3-mini | ~2.0-2.5 GB |
| Q5_K_M | ~2B | Gemma-2-2B, Qwen2.5-1.5B | ~1.5-2.0 GB |
| Q8_0 | ~1B | TinyLlama-1.1B, SmolLM2-1.7B | ~1.5-2.0 GB |

**推荐首选**：`bartowski/Llama-3.2-3B-Instruct-GGUF` 的 Q4_K_M（2.0 GB）
- 3B参数，英文对话能力强
- HF直接可拉取（`llama-cli -hf bartowski/Llama-3.2-3B-Instruct-GGUF:Q4_K_M`）
- 余量充足（2GB模型 + 系统开销 < 6.8GB 可用）

**备选**：`Qwen2.5-1.5B-Instruct-GGUF` 的 Q5_K_M（~1.2 GB）
- 中英文都好，1.5B参数

## 安装步骤（待执行）

```bash
# 1. 装 pip（当前 venv 缺 pip）
python3 -m ensurepip

# 2. 装 llama-cpp-python（CPU版，纯推理足够）
pip install llama-cpp-python

# 3. 首次运行（自动从HF下载模型）
python3 -c "
from llama_cpp import Llama
llm = Llama.from_pretrained(
    repo_id='bartowski/Llama-3.2-3B-Instruct-GGUF',
    filename='*Q4_K_M.gguf',
    n_ctx=2048,
    n_threads=4,
)
print(llm('What is the capital of France?', max_tokens=50))
"
```

## 潜在用途

1. **离线测试**：无需API key，验证prompt/skill逻辑
2. **敏感内容**：本地推理无审查，适合NSFW生成
3. **快速原型**：低延迟（CPU ~10-20 tok/s），迭代快
4. **嵌入向量**：llama-cpp支持embedding，可用于本地RAG

## 限制

- 无GPU加速，大模型不可行
- VRAM=0，无法offload任何层到GPU
- 4线程性能有限（预计3B Q4 ~15 tok/s）
- 当前venv无pip，需先 `ensurepip`

## 下次步骤

1. `python3 -m ensurepip` 后安装 llama-cpp-python
2. 下载并跑通 Llama-3.2-3B-Instruct
3. 测试嵌入向量功能
4. 探索 `llama-server` 的 OpenAI 兼容 API
