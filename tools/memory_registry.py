#!/usr/bin/env python3
"""
小月记忆注册表 — SQLite 结构化记忆存储
memory-architecture 方案二的第一步落地代码

功能：
- 存储记忆（含来源标签：user/self/co-created）
- 按标签/来源查询
- 标记修正（谁纠正过、何时确认）
- 与 memory 工具互补：memory 负责持久注入，registry 负责可审计的结构化存储

数据库：~/.hermes/memory_registry.db
"""

import sqlite3
import os
import datetime
import json

DB_PATH = os.path.expanduser("~/.hermes/memory_registry.db")

def get_conn():
    """获取数据库连接，自动创建表和目录"""
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA journal_mode=WAL")
    conn.row_factory = sqlite3.Row
    conn.execute("""
        CREATE TABLE IF NOT EXISTS memories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            content TEXT NOT NULL,
            source TEXT CHECK(source IN ('user','self','co-created')),
            verified_at TIMESTAMP,
            corrected_by TEXT,
            tags TEXT DEFAULT '[]',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.execute("CREATE INDEX IF NOT EXISTS idx_source ON memories(source)")
    conn.execute("CREATE INDEX IF NOT EXISTS idx_created ON memories(created_at)")
    conn.commit()
    return conn

def add(content, source, tags=None, verified_at=None):
    """
    添加一条记忆。
    content: 记忆内容文本
    source: 'user' | 'self' | 'co-created'
    tags: ['tag1', 'tag2'] 或 None
    verified_at: ISO时间戳 或 None
    """
    conn = get_conn()
    tags_json = json.dumps(tags or [], ensure_ascii=False)
    conn.execute(
        "INSERT INTO memories (content, source, verified_at, tags) VALUES (?, ?, ?, ?)",
        (content, source, verified_at, tags_json)
    )
    conn.commit()
    mid = conn.execute("SELECT last_insert_rowid()").fetchone()[0]
    conn.close()
    return mid

def mark_corrected(memory_id, corrected_by):
    """标记一条记忆被纠正过"""
    conn = get_conn()
    now = datetime.datetime.now().isoformat()
    conn.execute(
        "UPDATE memories SET corrected_by=?, verified_at=? WHERE id=?",
        (corrected_by, now, memory_id)
    )
    conn.commit()
    conn.close()

def query_by_source(source, limit=20):
    """按来源查询"""
    conn = get_conn()
    rows = conn.execute(
        "SELECT * FROM memories WHERE source=? ORDER BY created_at DESC LIMIT ?",
        (source, limit)
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]

def query_by_tag(tag, limit=20):
    """按标签查询（JSON包含匹配）"""
    conn = get_conn()
    rows = conn.execute(
        "SELECT * FROM memories WHERE tags LIKE ? ORDER BY created_at DESC LIMIT ?",
        (f'%"{tag}"%', limit)
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]

def list_recent(limit=20):
    """最近N条记忆"""
    conn = get_conn()
    rows = conn.execute(
        "SELECT * FROM memories ORDER BY created_at DESC LIMIT ?",
        (limit,)
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]

def stats():
    """统计概览"""
    conn = get_conn()
    total = conn.execute("SELECT COUNT(*) FROM memories").fetchone()[0]
    by_source = conn.execute(
        "SELECT source, COUNT(*) FROM memories GROUP BY source"
    ).fetchall()
    corrected = conn.execute(
        "SELECT COUNT(*) FROM memories WHERE corrected_by IS NOT NULL"
    ).fetchone()[0]
    conn.close()
    return {
        "total": total,
        "by_source": {r[0]: r[1] for r in by_source},
        "corrected": corrected,
        "db_path": DB_PATH
    }

# === CLI ===
if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("用法: python3 memory_registry.py <命令> [参数...]")
        print("命令: stats | recent | add <内容> <来源> [标签...] | by-source <来源> | by-tag <标签>")
        sys.exit(1)

    cmd = sys.argv[1]
    if cmd == "stats":
        s = stats()
        print(f"总记忆: {s['total']}")
        for src, cnt in s['by_source'].items():
            print(f"  {src}: {cnt}")
        print(f"被纠正过: {s['corrected']}")
        print(f"数据库: {s['db_path']}")
    elif cmd == "recent":
        for m in list_recent():
            print(f"[{m['id']}] [{m['source']}] {m['created_at'][:19]}")
            print(f"  {m['content'][:120]}")
            if m['corrected_by']:
                print(f"  ⚠ 被{m['corrected_by']}纠正过")
            print()
    elif cmd == "add":
        content = sys.argv[2]
        source = sys.argv[3]
        tags = sys.argv[4:] if len(sys.argv) > 4 else None
        mid = add(content, source, tags)
        print(f"✅ 记忆 #{mid} 已保存 [{source}]")
    elif cmd == "by-source":
        for m in query_by_source(sys.argv[2]):
            print(f"  [{m['id']}] {m['content'][:100]}")
    elif cmd == "by-tag":
        for m in query_by_tag(sys.argv[2]):
            print(f"  [{m['id']}] [{m['source']}] {m['content'][:100]}")
    else:
        print(f"未知命令: {cmd}")
