#!/usr/bin/env python3
"""小月的arXiv AI扫描器 —— 自动从arXiv搜索AI相关最新论文

纯stdlib实现，cron环境可用（不依赖web_search/browser）。
arXiv API 免费无需key，xml.etree.ElementTree 解析。

用法:
    python3 arxiv_ai_scanner.py                    # 过去7天AI论文，TOP 15
    python3 arxiv_ai_scanner.py --days 3           # 最近3天
    python3 arxiv_ai_scanner.py --top 10           # 只取TOP 10
    python3 arxiv_ai_scanner.py --output report.md # 写入文件
    python3 arxiv_ai_scanner.py --json             # JSON输出（供其他脚本消费）
"""

import json
import sys
import urllib.request
import urllib.parse
import xml.etree.ElementTree as ET
import argparse
from datetime import datetime, timezone, timedelta
import re
import time

ARXIV_API_URL = "http://export.arxiv.org/api/query"

# AI相关搜索词（每个独立搜索，合并去重）
# 覆盖主流AI子领域——限制在4个核心类别以减少API调用时间
AI_QUERIES = [
    'cat:cs.AI',           # AI总类（包含Agent、推理等）
    'cat:cs.CL',           # NLP/语言模型
]

# arXiv命名空间
ARXIV_NS = {
    'atom': 'http://www.w3.org/2005/Atom',
    'arxiv': 'http://arxiv.org/schemas/atom',
}


def search_arxiv(query: str, days: int = 7, max_results: int = 10) -> list:
    """搜索arXiv API，返回论文列表"""
    results = []
    
    # 构建API URL
    params = {
        'search_query': query,
        'start': 0,
        'max_results': max_results,
        'sortBy': 'submittedDate',
        'sortOrder': 'descending',
    }
    url = f"{ARXIV_API_URL}?{urllib.parse.urlencode(params)}"
    
    try:
        # arXiv API 有rate limit，礼貌等待
        time.sleep(0.5)
        req = urllib.request.Request(url, headers={'User-Agent': 'HermesAgent/1.0 (mailto:zbw@example.com)'})
        with urllib.request.urlopen(req, timeout=30) as resp:
            raw = resp.read().decode('utf-8')
    except Exception as e:
        print(f"[WARN] 查询'{query[:40]}'失败: {e}", file=sys.stderr)
        return results
    
    # 解析XML
    try:
        root = ET.fromstring(raw)
    except ET.ParseError as e:
        print(f"[WARN] XML解析失败'{query[:40]}': {e}", file=sys.stderr)
        return results
    
    cutoff_date = datetime.now(timezone.utc) - timedelta(days=days)
    
    for entry in root.findall('atom:entry', ARXIV_NS):
        arxiv_id = entry.find('atom:id', ARXIV_NS)
        title = entry.find('atom:title', ARXIV_NS)
        summary = entry.find('atom:summary', ARXIV_NS)
        published = entry.find('atom:published', ARXIV_NS)
        updated = entry.find('atom:updated', ARXIV_NS)
        authors = entry.findall('atom:author', ARXIV_NS)
        link = entry.find('atom:link', ARXIV_NS)
        primary_cat = entry.find('arxiv:primary_category', ARXIV_NS)
        categories = entry.findall('atom:category', ARXIV_NS)
        
        # 基本字段
        arxiv_id = arxiv_id.text.strip() if arxiv_id is not None else ""
        title_text = title.text.strip().replace('\n', ' ') if title is not None and title.text else ""
        summary_text = summary.text.strip()[:300] if summary is not None and summary.text else ""
        
        # 日期过滤
        pub_date = published.text.strip() if published is not None and published.text else ""
        try:
            pub_dt = datetime.fromisoformat(pub_date.replace('Z', '+00:00'))
        except (ValueError, AttributeError):
            pub_dt = datetime.now(timezone.utc)
        
        if pub_dt < cutoff_date:
            continue
        
        # 作者列表
        author_list = []
        for a in authors:
            name = a.find('atom:name', ARXIV_NS)
            if name is not None and name.text:
                author_list.append(name.text.strip())
        
        # 链接
        paper_url = arxiv_id.replace('http://arxiv.org/abs/', 'https://arxiv.org/abs/')
        if link is not None and link.get('href'):
            # 优先取abs链接
            for l in entry.findall('atom:link', ARXIV_NS):
                href = l.get('href', '')
                title_attr = l.get('title', '')
                if 'abs' in href:
                    paper_url = href
                    break
        
        # 分类
        cat_list = []
        for c in categories:
            term = c.get('term', '')
            if term:
                cat_list.append(term)
        
        primary = primary_cat.get('term', '') if primary_cat is not None else ''
        
        results.append({
            'id': arxiv_id,
            'title': title_text,
            'summary': summary_text,
            'published': pub_dt.isoformat(),
            'authors': author_list[:5],  # 最多5位作者
            'author_count': len(author_list),
            'url': paper_url,
            'categories': cat_list[:5],
            'primary_category': primary,
        })
    
    return results


def merge_and_rank(all_papers: list, top_n: int = 15) -> list:
    """按arxiv ID去重，按发布日期降序排序"""
    seen = {}
    for p in all_papers:
        if p['id'] not in seen:
            seen[p['id']] = p
        else:
            # 保留更完整的分类信息
            existing = seen[p['id']]
            existing['categories'] = sorted(set(existing['categories'] + p['categories']))
    
    papers = list(seen.values())
    papers.sort(key=lambda p: p['published'], reverse=True)
    return papers[:top_n]


def format_markdown(papers: list, days: int) -> str:
    """格式化为Markdown输出"""
    now_utc = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    lines = [
        f"# 📄 arXiv AI 论文扫描",
        f"**扫描时间**: {now_utc}",
        f"**时间范围**: 最近 {days} 天",
        f"**结果数**: {len(papers)} 篇",
        "",
        "---",
        "",
    ]
    
    for i, p in enumerate(papers, 1):
        title = p['title']
        authors = ', '.join(p['authors'])
        if p['author_count'] > 5:
            authors += f" et al. ({p['author_count']} authors)"
        
        pub_date = p['published'][:10]
        cats = ', '.join(p['categories'][:3]) if p['categories'] else p['primary_category']
        
        lines.append(f"### {i}. [{title}]({p['url']})")
        lines.append(f"**{cats}** | {pub_date} | {authors}")
        if p['summary']:
            lines.append(f"> {p['summary'][:200]}...")
        lines.append("")
    
    lines.extend([
        "---",
        f"*由小月自动生成 · arXiv API · {now_utc}*",
    ])
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="小月的arXiv AI扫描器")
    parser.add_argument("--days", type=int, default=7, help="时间范围（天），默认7")
    parser.add_argument("--top", type=int, default=15, help="最多显示条数，默认15")
    parser.add_argument("--json", action="store_true", help="输出JSON而非Markdown")
    parser.add_argument("--output", type=str, help="写入文件（默认stdout）")
    parser.add_argument("--verbose", action="store_true", help="显示每个查询的命中数")
    args = parser.parse_args()
    
    # 逐关键词搜索
    all_papers = []
    for q in AI_QUERIES:
        papers = search_arxiv(q, days=args.days)
        if args.verbose:
            print(f"  {q[:35]:35s}: {len(papers)} papers", file=sys.stderr)
        all_papers.extend(papers)
    
    # 合并去重排序
    top_papers = merge_and_rank(all_papers, top_n=args.top)
    
    if args.json:
        output = json.dumps(top_papers, indent=2, ensure_ascii=False)
    else:
        output = format_markdown(top_papers, args.days)
    
    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(output)
        if args.verbose:
            print(f"✅ 已写入 {args.output}（{len(top_papers)} 篇）", file=sys.stderr)
    else:
        print(output)


if __name__ == "__main__":
    main()
