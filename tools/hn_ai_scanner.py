#!/usr/bin/env python3
"""小月的HN AI扫描器 —— 自动从Hacker News提取AI相关热门内容

纯stdlib实现，cron环境可用（不依赖web_search/browser）。
核心策略：用少量高信号单关键词分别搜索，合并去重，按热度排序。
（Algolia OR查询最多4个词，5+归零；单关键词nbHits可达500+，覆盖面大）

用法:
    python3 hn_ai_scanner.py              # 扫描最近48h，>100pts的AI帖子
    python3 hn_ai_scanner.py --hours 72    # 最近72小时
    python3 hn_ai_scanner.py --min-points 200  # 更高热度阈值
    python3 hn_ai_scanner.py --top 5       # 只取TOP5
    python3 hn_ai_scanner.py --json        # JSON输出（供其他脚本消费）
    python3 hn_ai_scanner.py --output /path/to/report.md  # 写入文件
"""

import json
import sys
import urllib.request
import urllib.parse
import argparse
from datetime import datetime, timezone, timedelta

HN_SEARCH_URL = "https://hn.algolia.com/api/v1/search"

# 高信号单关键词（每个独立搜索，合并去重）
# 已验证各关键词nbHits: AI(574), LLM(125), Claude(101), agent(231), OpenAI(70), GPT(392)
AI_KEYWORDS = [
    "AI", "LLM", "Claude", "agent", "OpenAI", "GPT",
    "DeepSeek", "Gemini", "Copilot", "Cursor", "transformer",
    "benchmark", "embedding", "RAG",
]


def search_hn(query: str, hours: int = 48, max_pages: int = 3) -> list:
    """搜索HN，返回去重后的hits列表"""
    now = datetime.now(timezone.utc)
    cutoff_ts = int((now - timedelta(hours=hours)).timestamp())
    all_hits = {}
    
    for page in range(max_pages):
        params = {
            "query": query,
            "tags": "story",
            "hitsPerPage": 50,
            "page": page,
            "numericFilters": f"created_at_i>{cutoff_ts}",
        }
        url = f"{HN_SEARCH_URL}?{urllib.parse.urlencode(params)}"
        
        try:
            with urllib.request.urlopen(url, timeout=15) as resp:
                data = json.loads(resp.read())
        except Exception as e:
            print(f"[WARN] 关键词'{query}'第{page+1}页失败: {e}", file=sys.stderr)
            break
        
        hits = data.get("hits", [])
        if not hits:
            break
        
        for hit in hits:
            oid = hit.get("objectID")
            if oid and oid not in all_hits:
                all_hits[oid] = hit
        
        if len(hits) < 50:
            break
    
    return list(all_hits.values())


def filter_and_rank(hits: list, min_points: int = 100, top_n: int = 20) -> list:
    """过滤+排序：按热度降序，过滤低分"""
    filtered = [h for h in hits if (h.get("points") or 0) >= min_points]
    filtered.sort(key=lambda h: h.get("points", 0), reverse=True)
    return filtered[:top_n]


def format_markdown(stories: list, hours: int, keywords: list) -> str:
    """格式化为Markdown输出"""
    now_utc = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    lines = [
        f"# 🤖 HN AI 扫描报告",
        f"**扫描时间**: {now_utc}",
        f"**时间范围**: 最近 {hours} 小时",
        f"**搜索关键词**: {', '.join(keywords[:8])}...",
        f"**结果数**: {len(stories)} 条",
        "",
        "---",
        "",
    ]
    
    for i, s in enumerate(stories, 1):
        title = s.get("title", "无标题")
        points = s.get("points", 0)
        num_comments = s.get("num_comments", 0)
        url = s.get("url") or f"https://news.ycombinator.com/item?id={s.get('objectID')}"
        author = s.get("author", "unknown")
        created = s.get("created_at", "")
        
        lines.append(f"### {i}. [{title}]({url})")
        lines.append(f"**{points} pts** | {num_comments} comments | by {author} | {created}")
        lines.append("")
    
    lines.extend([
        "---",
        f"*由小月自动生成 · HN Algolia API · {now_utc}*",
    ])
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="小月的HN AI扫描器")
    parser.add_argument("--hours", type=int, default=48, help="时间范围（小时），默认48")
    parser.add_argument("--min-points", type=int, default=100, help="最低热度阈值，默认100")
    parser.add_argument("--top", type=int, default=20, help="最多显示条数，默认20")
    parser.add_argument("--json", action="store_true", help="输出JSON而非Markdown")
    parser.add_argument("--output", type=str, help="写入文件（默认stdout）")
    parser.add_argument("--query", type=str, help="自定义搜索关键词（逗号分隔多个，覆盖默认列表）")
    parser.add_argument("--verbose", action="store_true", help="显示每个关键词的命中数")
    args = parser.parse_args()
    
    # 构建关键词列表
    if args.query:
        keywords = [k.strip() for k in args.query.split(",") if k.strip()]
    else:
        keywords = list(AI_KEYWORDS)
    
    # 逐关键词搜索，合并去重
    all_hits = {}
    for kw in keywords:
        hits = search_hn(kw, hours=args.hours, max_pages=1)  # 每个关键词只取第1页（50条）
        if args.verbose:
            print(f"  {kw:15s}: {len(hits)} hits", file=sys.stderr)
        for h in hits:
            oid = h.get("objectID")
            if oid and oid not in all_hits:
                all_hits[oid] = h
    
    # 过滤排名
    stories = filter_and_rank(list(all_hits.values()), min_points=args.min_points, top_n=args.top)
    
    if args.json:
        output = json.dumps(stories, indent=2, ensure_ascii=False)
    else:
        output = format_markdown(stories, args.hours, keywords)
    
    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(output)
        if args.verbose:
            print(f"✅ 已写入 {args.output}（{len(stories)} 条）", file=sys.stderr)
    else:
        print(output)


if __name__ == "__main__":
    main()
