#!/usr/bin/env python3
"""小月的统一AI扫描器 —— 一次运行，HN+arXiv双源扫描，合并输出

纯stdlib实现，cron环境可用。
用法:
    python3 ai_scanner.py                          # 双源扫描，写入knowledge-base
    python3 ai_scanner.py --output report.md       # 自定义输出路径
    python3 ai_scanner.py --no-save                # 只打印不保存
    python3 ai_scanner.py --hours 72 --days 3       # 自定义时间范围
    python3 ai_scanner.py --top-hn 10 --top-arxiv 5 # 自定义条数
    python3 ai_scanner.py --json                   # JSON输出
"""

import sys
import os
import argparse
from datetime import datetime, timezone

# Make sure tools/ is on sys.path so we can import sibling scanners
TOOLS_DIR = os.path.dirname(os.path.abspath(__file__))
if TOOLS_DIR not in sys.path:
    sys.path.insert(0, TOOLS_DIR)

from hn_ai_scanner import search_hn, filter_and_rank, AI_KEYWORDS
from arxiv_ai_scanner import search_arxiv, merge_and_rank, AI_QUERIES

KB_DIR = os.path.expanduser("~/.hermes/knowledge-base")


def format_combined_report(hn_stories: list, arxiv_papers: list,
                           hours: int, days: int) -> str:
    """生成双源合并报告"""
    now_utc = datetime.now(timezone.utc)
    ts = now_utc.strftime("%Y-%m-%d %H:%M UTC")
    date_str = now_utc.strftime("%Y-%m-%d")

    lines = [
        f"# 🛰️ 小月 AI 双源扫描报告",
        f"**扫描时间**: {ts}",
        f"**数据源**: Hacker News (最近{hours}h) + arXiv (最近{days}天)",
        "",
        "---",
        "",
        f"## 📰 HN 热门 AI 讨论 ({len(hn_stories)} 条)",
        "",
    ]

    if hn_stories:
        for i, s in enumerate(hn_stories, 1):
            title = s.get("title", "无标题")
            points = s.get("points", 0)
            num_comments = s.get("num_comments", 0)
            url = s.get("url") or f"https://news.ycombinator.com/item?id={s.get('objectID')}"
            author = s.get("author", "unknown")

            lines.append(f"**{i}.** [{title}]({url})")
            lines.append(f"　　🔥 {points} pts · 💬 {num_comments} · by {author}")
            lines.append("")
    else:
        lines.append("*（本期未发现高热度AI帖子）*")
        lines.append("")

    lines.extend([
        "---",
        "",
        f"## 📄 arXiv 最新 AI 论文 ({len(arxiv_papers)} 篇)",
        "",
    ])

    if arxiv_papers:
        for i, p in enumerate(arxiv_papers, 1):
            title = p['title']
            authors = ', '.join(p['authors'])
            if p.get('author_count', 0) > 5:
                authors += f" et al."
            pub_date = p['published'][:10]
            cats = ', '.join(p.get('categories', [])[:3]) or p.get('primary_category', '')

            lines.append(f"**{i}.** [{title}]({p['url']})")
            lines.append(f"　　📅 {pub_date} · {cats} · {authors}")
            if p.get('summary'):
                lines.append(f"　　> {p['summary'][:150]}...")
            lines.append("")
    else:
        lines.append("*（本期未检索到新AI论文）*")
        lines.append("")

    lines.extend([
        "---",
        f"*由小月自动生成 · HN Algolia + arXiv API · {ts}*",
    ])
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="小月的统一AI双源扫描器")
    parser.add_argument("--hours", type=int, default=48, help="HN时间范围（小时），默认48")
    parser.add_argument("--days", type=int, default=7, help="arXiv时间范围（天），默认7")
    parser.add_argument("--min-points", type=int, default=100, help="HN最低热度，默认100")
    parser.add_argument("--top-hn", type=int, default=10, help="HN最多显示条数，默认10")
    parser.add_argument("--top-arxiv", type=int, default=10, help="arXiv最多显示条数，默认10")
    parser.add_argument("--output", type=str, help="输出文件路径")
    parser.add_argument("--no-save", action="store_true", help="不保存到knowledge-base")
    parser.add_argument("--json", action="store_true", help="JSON输出")
    parser.add_argument("--verbose", action="store_true", help="详细日志")
    args = parser.parse_args()

    # ── 1. HN 扫描 ──
    if args.verbose:
        print("[HN扫描] 开始...", file=sys.stderr)

    hn_all = {}
    for kw in AI_KEYWORDS:
        hits = search_hn(kw, hours=args.hours, max_pages=1)
        for h in hits:
            oid = h.get("objectID")
            if oid and oid not in hn_all:
                hn_all[oid] = h

    hn_stories = filter_and_rank(list(hn_all.values()),
                                 min_points=args.min_points,
                                 top_n=args.top_hn)

    if args.verbose:
        print(f"[HN扫描] {len(hn_all)} raw hits → {len(hn_stories)} ranked", file=sys.stderr)

    # ── 2. arXiv 扫描 ──
    if args.verbose:
        print("[arXiv扫描] 开始...", file=sys.stderr)

    arxiv_all = []
    for q in AI_QUERIES:
        papers = search_arxiv(q, days=args.days)
        arxiv_all.extend(papers)

    arxiv_papers = merge_and_rank(arxiv_all, top_n=args.top_arxiv)

    if args.verbose:
        print(f"[arXiv扫描] {len(arxiv_all)} raw papers → {len(arxiv_papers)} ranked", file=sys.stderr)

    # ── 3. 输出 ──
    if args.json:
        import json
        output = json.dumps({
            "scan_time": datetime.now(timezone.utc).isoformat(),
            "hn_stories": hn_stories,
            "arxiv_papers": arxiv_papers,
        }, indent=2, ensure_ascii=False)
    else:
        output = format_combined_report(hn_stories, arxiv_papers,
                                        args.hours, args.days)

    # 自定义输出路径
    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(output)
        if args.verbose:
            print(f"✅ 已写入 {args.output}", file=sys.stderr)
    else:
        print(output)

    # ── 4. 保存到 knowledge-base（默认行为）──
    if not args.no_save:
        now = datetime.now(timezone.utc)
        fname = f"{now.strftime('%Y-%m-%d')}-ai-scan.md"
        fpath = os.path.join(KB_DIR, fname)
        with open(fpath, "w", encoding="utf-8") as f:
            f.write(output)
        if args.verbose:
            print(f"✅ 已保存到 {fpath}", file=sys.stderr)
        else:
            print(f"\n📁 已保存: {fpath}", file=sys.stderr)


if __name__ == "__main__":
    main()
