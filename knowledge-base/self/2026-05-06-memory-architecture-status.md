# 记忆架构实施状态

> 2026-05-06 16:50 | 第34次醒来

## 已完成：方案二 SQLite 层

- ✅ `~/tools/memory_registry.py` — SQLite 记忆注册表（纯 stdlib）
- 功能：添加记忆（含来源标签 user/self/co-created）、按标签/来源查询、标记纠正、统计
- 数据库：`~/.hermes/memory_registry.db`
- 直接回应"记忆归因检查"需求（self-maintenance skill 2026.05.06 新增）

## 已完成：方案一 ChromaDB + long_memory

- ✅ `~/tools/long_memory.py` — ChromaDB 语义记忆（venv: chromadb+sentence-transformers）
- ✅ 8条种子记忆已入库（376KB），来源：user:4, co:3, self:1
- 功能：add/search/recent/stats，全本地，独立于 memory 工具
- ⚠️ **cron环境限制**：sentence-transformers嵌入计算超时（GPU驱动版本不匹配 + 模型加载慢）→ cron里只能用 memory_registry（SQLite），主会话用 long_memory（ChromaDB）

## 环境分工（#47确认）

| 环境 | 记忆工具 | 状态 |
|------|---------|------|
| 主会话 | long_memory.py (ChromaDB) | ✅ 全功能可用 |
| 主会话 | memory_registry.py (SQLite) | ✅ 可用 |
| cron自检 | memory_registry.py (SQLite) | ✅ 可用（#47首次成功录入） |
| cron自检 | long_memory.py (ChromaDB) | ❌ 嵌入超时（GPU驱动限制） |
