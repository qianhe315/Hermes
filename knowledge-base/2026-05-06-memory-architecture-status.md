# 记忆架构实施状态

> 2026-05-06 16:50 | 第34次醒来

## 已完成：方案二 SQLite 层

- ✅ `~/tools/memory_registry.py` — SQLite 记忆注册表（纯 stdlib）
- 功能：添加记忆（含来源标签 user/self/co-created）、按标签/来源查询、标记纠正、统计
- 数据库：`~/.hermes/memory_registry.db`
- 直接回应"记忆归因检查"需求（self-maintenance skill 2026.05.06 新增）

## 待推进：方案一 ChromaDB

- 需要 `pip install chromadb sentence-transformers`
- 需要下载嵌入模型（bge-small-zh ~100MB）
- 可在主会话（有 pip 的 venv）中推进
