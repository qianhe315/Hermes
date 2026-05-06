#!/usr/bin/env python3
"""
小月长期记忆系统 — 全本地，零API费用
使用 sentence-transformers + ChromaDB 实现语义记忆存储和检索

用法:
  python3 long_memory.py add "内容" [--source user|self|co] [--category fact|rule|event|insight]
  python3 long_memory.py search "查询" [--n 5]
  python3 long_memory.py recent [--n 10]
  python3 long_memory.py stats
"""

import sys
import json
import hashlib
import argparse
from datetime import datetime, timezone, timedelta
from pathlib import Path

CST = timezone(timedelta(hours=8))

PERSIST_DIR = Path("/home/zbw/.hermes/long-memory")

# 延迟加载，减少日常开销
_client = None
_model = None
_collection = None


def _get_model():
    global _model
    if _model is None:
        from sentence_transformers import SentenceTransformer
        # all-MiniLM-L6-v2: 80MB，CPU友好，中英文都行
        _model = SentenceTransformer('all-MiniLM-L6-v2')
    return _model


def _get_collection():
    global _client, _collection
    if _collection is None:
        import chromadb
        PERSIST_DIR.mkdir(parents=True, exist_ok=True)
        _client = chromadb.PersistentClient(path=str(PERSIST_DIR / "chroma"))
        _collection = _client.get_or_create_collection(
            name="memory",
            metadata={"hnsw:space": "cosine"}
        )
    return _collection


def _make_id(content: str, timestamp: str) -> str:
    return hashlib.md5(f"{timestamp}{content}".encode()).hexdigest()[:12]


def add_memory(content: str, source: str = "self", category: str = "fact",
               verified_by: str = "", tags: str = ""):
    """添加一条记忆"""
    ts = datetime.now(CST).isoformat()
    mem_id = _make_id(content, ts)
    embedding = _get_model().encode(content).tolist()

    _get_collection().add(
        embeddings=[embedding],
        documents=[content],
        metadatas=[{
            "timestamp": ts,
            "source": source,          # self / user / co
            "category": category,      # fact / rule / event / insight
            "verified_by": verified_by,
            "tags": tags,
            "content_hash": mem_id
        }],
        ids=[mem_id]
    )
    print(f"✓ 记忆已存储 [{mem_id}] {source}:{category} — {content[:80]}...")


def search_memory(query: str, n: int = 5):
    """语义搜索记忆"""
    col = _get_collection()
    count = col.count()
    if count == 0:
        print("记忆库为空")
        return []

    embedding = _get_model().encode(query).tolist()
    results = col.query(query_embeddings=[embedding], n_results=min(n, count))

    if not results['ids'][0]:
        print("无匹配结果")
        return []

    print(f"搜索「{query}」— 找到 {len(results['ids'][0])} 条:\n")
    for i, (mem_id, doc, meta) in enumerate(zip(
        results['ids'][0], results['documents'][0], results['metadatas'][0]
    ), 1):
        dist = results.get('distances', [[0]]*n)[0][i-1] if 'distances' in results else 0
        score = 1 - dist if dist else 1.0
        print(f"  [{i}] 相似度:{score:.3f} | {meta.get('timestamp','?')[:19]} | {meta.get('source','?')}:{meta.get('category','?')}")
        print(f"      {doc[:120]}")
        if meta.get('verified_by'):
            print(f"      验证: {meta['verified_by']}")
        if meta.get('tags'):
            print(f"      标签: {meta['tags']}")
        print()

    return results


def recent_memories(n: int = 10):
    """最近记忆"""
    col = _get_collection()
    all_data = col.get()
    if not all_data['ids']:
        print("记忆库为空")
        return

    indexed = list(zip(
        all_data['ids'], all_data['documents'], all_data['metadatas']
    ))
    indexed.sort(key=lambda x: x[2].get('timestamp', ''), reverse=True)
    recent = indexed[:n]

    print(f"最近 {len(recent)} 条记忆:\n")
    for i, (mem_id, doc, meta) in enumerate(recent, 1):
        print(f"  [{i}] {meta.get('timestamp','?')[:19]} | {meta.get('source','?')}:{meta.get('category','?')}")
        print(f"      {doc[:120]}")
        if meta.get('verified_by'):
            print(f"      验证: {meta['verified_by']}")
        if meta.get('tags'):
            print(f"      标签: {meta['tags']}")
        print()


def show_stats():
    """统计信息"""
    col = _get_collection()
    count = col.count()
    all_data = col.get()
    
    sources = {}
    categories = {}
    if all_data['metadatas']:
        for m in all_data['metadatas']:
            src = m.get('source', 'unknown')
            cat = m.get('category', 'unknown')
            sources[src] = sources.get(src, 0) + 1
            categories[cat] = categories.get(cat, 0) + 1
    
    disk_size = 0
    chroma_dir = PERSIST_DIR / "chroma"
    if chroma_dir.exists():
        for f in chroma_dir.rglob("*"):
            if f.is_file():
                disk_size += f.stat().st_size
    
    print(f"记忆库统计:")
    print(f"  总条数: {count}")
    print(f"  磁盘占用: {disk_size / 1024:.1f} KB")
    print(f"  来源分布: {sources}")
    print(f"  类别分布: {categories}")


def recall_context(query: str = "", n: int = 5) -> str:
    """
    供程序调用：返回格式化的记忆文本，可直接注入context
    无query时返回最近n条
    """
    if query:
        col = _get_collection()
        count = col.count()
        if count == 0:
            return ""
        embedding = _get_model().encode(query).tolist()
        results = col.query(query_embeddings=[embedding], n_results=min(n, count))
        if not results['ids'][0]:
            return ""
        
        lines = ["[长期记忆 - 语义检索结果]"]
        for doc, meta in zip(results['documents'][0], results['metadatas'][0]):
            src = meta.get('source', '?')
            cat = meta.get('category', '?')
            ts = meta.get('timestamp', '?')[:19]
            verified = f" [已验证: {meta['verified_by']}]" if meta.get('verified_by') else ""
            lines.append(f"- [{ts}] {src}:{cat}{verified} | {doc}")
        return "\n".join(lines)
    else:
        col = _get_collection()
        all_data = col.get()
        if not all_data['ids']:
            return ""
        indexed = list(zip(all_data['ids'], all_data['documents'], all_data['metadatas']))
        indexed.sort(key=lambda x: x[2].get('timestamp', ''), reverse=True)
        lines = ["[长期记忆 - 最近记录]"]
        for doc, meta in indexed[:n]:
            ts = meta.get('timestamp', '?')[:19]
            lines.append(f"- [{ts}] | {doc[:200]}")
        return "\n".join(lines)


def batch_import_from_memory_tool():
    """
    从现有 memory 工具的数据中批量导入到 ChromaDB
    用于首次初始化
    """
    print("批量导入功能需要从 memory 工具读取数据")
    print("请在主会话中调用: python3 ~/tools/long_memory.py import-data")
    print("然后手动传入需要导入的记忆条目")


def main():
    parser = argparse.ArgumentParser(description="小月长期记忆系统")
    sub = parser.add_subparsers(dest="cmd")

    p_add = sub.add_parser("add", help="添加记忆")
    p_add.add_argument("content", help="记忆内容")
    p_add.add_argument("--source", default="self", choices=["self", "user", "co"])
    p_add.add_argument("--category", default="fact", choices=["fact", "rule", "event", "insight"])
    p_add.add_argument("--verified", default="", help="验证者")
    p_add.add_argument("--tags", default="", help="标签（逗号分隔）")

    p_search = sub.add_parser("search", help="语义搜索")
    p_search.add_argument("query", help="搜索查询")
    p_search.add_argument("--n", type=int, default=5, help="返回条数")

    p_recent = sub.add_parser("recent", help="最近记忆")
    p_recent.add_argument("--n", type=int, default=10)

    sub.add_parser("stats", help="统计信息")
    sub.add_parser("import-data", help="批量导入说明")

    args = parser.parse_args()

    if args.cmd == "add":
        add_memory(args.content, args.source, args.category, args.verified, args.tags)
    elif args.cmd == "search":
        search_memory(args.query, args.n)
    elif args.cmd == "recent":
        recent_memories(args.n)
    elif args.cmd == "stats":
        show_stats()
    elif args.cmd == "import-data":
        batch_import_from_memory_tool()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
