#!/usr/bin/env python3
"""geoeye — AI搜索引擎引用概率分析工具 (GEO)

检测你的网站在ChatGPT/Perplexity/Google AI Overviews中被引用的可能性。
纯离线分析，零API费用。

用法:
    geoeye https://example.com
    geoeye https://example.com --output report.json
    geoeye https://example.com --verbose
"""

import sys
import re
import json
import argparse
from urllib.request import urlopen, Request
from urllib.parse import urlparse
from html.parser import HTMLParser
from collections import Counter

class ContentExtractor(HTMLParser):
    def __init__(self):
        super().__init__()
        self.title = ""
        self.headings = []
        self.paragraphs = []
        self.meta_desc = ""
        self.in_title = False
        self.in_script = False
        self.in_style = False
        self.current_h = None
        self.current_p = []
        self.text_buffer = []

    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)
        if tag in ("script", "style"):
            self.in_script = True
        elif tag == "title":
            self.in_title = True
        elif tag in ("h1", "h2", "h3"):
            self.current_h = tag
        elif tag == "p":
            self.current_p = []
        elif tag == "meta" and attrs_dict.get("name", "").lower() == "description":
            self.meta_desc = attrs_dict.get("content", "")

    def handle_endtag(self, tag):
        if tag in ("script", "style"):
            self.in_script = False
        elif tag == "title":
            self.in_title = False
        elif tag in ("h1", "h2", "h3") and self.current_h:
            text = " ".join(self.text_buffer).strip()
            if text:
                self.headings.append({"level": self.current_h, "text": text})
            self.text_buffer = []
            self.current_h = None
        elif tag == "p":
            text = " ".join(self.current_p).strip()
            if text:
                self.paragraphs.append(text)
            self.current_p = []

    def handle_data(self, data):
        if self.in_script or self.in_style:
            return
        data = data.strip()
        if not data:
            return
        if self.in_title:
            self.title += data
        elif self.current_h is not None:
            self.text_buffer.append(data)
        elif self.current_p is not None:
            self.current_p.append(data)


def fetch_page(url):
    headers = {"User-Agent": "geoeye/1.0 (GEO analysis bot; contact@example.com)"}
    req = Request(url, headers=headers)
    with urlopen(req, timeout=15) as resp:
        return resp.read().decode("utf-8", errors="replace")


def analyze_citability(extractor, url, raw_html):
    """核心分析：判断AI搜索引擎引用该页面的概率"""
    scores = {}
    details = {}

    # 1. 标题质量 (0-20)
    title = extractor.title.strip()
    title_len = len(title)
    if 20 <= title_len <= 70:
        title_score = 20
        title_note = "理想长度"
    elif 10 <= title_len < 20:
        title_score = 14
        title_note = "偏短，信息量可能不足"
    elif 70 < title_len <= 100:
        title_score = 12
        title_note = "偏长，AI可能截断"
    elif title_len > 100:
        title_score = 5
        title_note = "过长，严重截断风险"
    else:
        title_score = 3
        title_note = "过短或无标题"
    scores["title"] = title_score
    details["title"] = {"score": title_score, "length": title_len, "note": title_note, "content": title[:80]}

    # 2. Meta描述 (0-10)
    meta = extractor.meta_desc.strip()
    if meta:
        if 50 <= len(meta) <= 160:
            meta_score = 10
            meta_note = "理想长度"
        else:
            meta_score = 5
            meta_note = f"长度{len(meta)}，非最佳"
    else:
        meta_score = 0
        meta_note = "缺失meta description"
    scores["meta"] = meta_score
    details["meta"] = {"score": meta_score, "note": meta_note}

    # 3. 结构化程度 (0-25)
    headings = extractor.headings
    h1_count = sum(1 for h in headings if h["level"] == "h1")
    h2_count = sum(1 for h in headings if h["level"] == "h2")
    total_h = len(headings)

    if h1_count >= 1 and h2_count >= 2:
        structure_score = 25
        structure_note = "层级清晰，AI友好"
    elif h1_count >= 1 and total_h >= 3:
        structure_score = 18
        structure_note = "有基本结构，可改进"
    elif total_h >= 2:
        structure_score = 10
        structure_note = "结构简单"
    else:
        structure_score = 3
        structure_note = "缺少标题结构，AI难以解析"
    scores["structure"] = structure_score
    details["structure"] = {"score": structure_score, "h1": h1_count, "h2": h2_count,
                            "total_headings": total_h, "note": structure_note}

    # 4. 内容深度 (0-25)
    paragraphs = extractor.paragraphs
    total_words = sum(len(p.split()) for p in paragraphs)
    avg_para_len = total_words / max(len(paragraphs), 1)

    if total_words > 1000 and avg_para_len > 30:
        content_score = 25
        content_note = "深度内容，高引用价值"
    elif total_words > 500:
        content_score = 18
        content_note = "中等深度"
    elif total_words > 100:
        content_score = 8
        content_note = "内容较少"
    else:
        content_score = 2
        content_note = "内容严重不足"
    scores["content"] = content_score
    details["content"] = {"score": content_score, "total_words": total_words,
                          "avg_para_len": round(avg_para_len, 1), "paragraphs": len(paragraphs),
                          "note": content_note}

    # 5. 时效性信号 (0-10)
    html_lower = raw_html.lower()
    date_patterns = [
        r'<time[^>]*datetime=["\']([^"\']+)',
        r'last[- ]?updated[:\s]*([\d]{4}[-/][\d]{2}[-/][\d]{2})',
        r'published[:\s]*([\d]{4}[-/][\d]{2}[-/][\d]{2})',
        r'"dateModified":\s*"([^"]+)"',
        r'"datePublished":\s*"([^"]+)"',
    ]
    found_date = None
    for pattern in date_patterns:
        match = re.search(pattern, html_lower, re.IGNORECASE)
        if match:
            found_date = match.group(1)[:10]
            break

    if found_date:
        # 检查是否是近期的
        import datetime
        try:
            date_obj = datetime.datetime.strptime(found_date, "%Y-%m-%d")
            days_ago = (datetime.datetime.now() - date_obj).days
            if days_ago < 30:
                freshness_score = 10
                freshness_note = f"最近更新({days_ago}天前)"
            elif days_ago < 180:
                freshness_score = 6
                freshness_note = f"较新({days_ago}天前)"
            else:
                freshness_score = 3
                freshness_note = f"较旧({days_ago}天前)"
        except:
            freshness_score = 5
            freshness_note = f"检测到日期{found_date}"
    else:
        freshness_score = 1
        freshness_note = "无时间戳，AI可能质疑时效性"
    scores["freshness"] = freshness_score
    details["freshness"] = {"score": freshness_score, "date_found": found_date, "note": freshness_note}

    # 6. 链接引用 (0-10)
    link_count = len(re.findall(r'<a\s[^>]*href=["\']https?://', raw_html))
    if link_count > 20:
        link_score = 10
        link_note = "丰富的外部引用"
    elif link_count > 5:
        link_score = 6
        link_note = f"{link_count}个外部链接"
    else:
        link_score = 2
        link_note = "外部链接少"
    scores["links"] = link_score
    details["links"] = {"score": link_score, "external_links": link_count, "note": link_note}

    total = sum(scores.values())
    max_possible = 100

    if total >= 80:
        grade = "A — AI极可能引用"
    elif total >= 60:
        grade = "B — AI可能引用"
    elif total >= 40:
        grade = "C — AI偶尔引用"
    elif total >= 20:
        grade = "D — AI很少引用"
    else:
        grade = "F — AI几乎不引用"

    return {
        "url": url,
        "total_score": total,
        "max_score": max_possible,
        "grade": grade,
        "breakdown": details,
        "scoring": {k: v for k, v in scores.items()}
    }


def main():
    parser = argparse.ArgumentParser(
        description="geoeye — AI搜索引擎引用概率分析",
        epilog="示例: geoeye https://example.com --verbose"
    )
    parser.add_argument("url", help="要分析的网页URL")
    parser.add_argument("--output", "-o", help="输出JSON报告到文件")
    parser.add_argument("--verbose", "-v", action="store_true", help="详细输出")
    args = parser.parse_args()

    url = args.url
    if not url.startswith("http"):
        url = "https://" + url

    print(f"🔍 geoeye 正在分析: {url}\n")

    try:
        raw_html = fetch_page(url)
    except Exception as e:
        print(f"❌ 无法获取页面: {e}")
        sys.exit(1)

    extractor = ContentExtractor()
    extractor.feed(raw_html)

    result = analyze_citability(extractor, url, raw_html)

    # 输出
    print(f"┌──────────────────────────────────────┐")
    print(f"│  AI引用评分: {result['total_score']:>3d}/100  →  {result['grade']:22s} │")
    print(f"└──────────────────────────────────────┘")
    print()

    if args.verbose:
        for key, detail in result['breakdown'].items():
            bar = "█" * (detail['score'] // 2) + "░" * (10 - detail['score'] // 2)
            print(f"  {key:12s} [{bar}] {detail['score']}/20+  {detail.get('note', '')}")
        print()

    # 改进建议
    suggestions = []
    if result['breakdown']['title']['score'] < 15:
        suggestions.append("📝 优化标题至20-70字符，包含核心关键词")
    if result['breakdown']['meta']['score'] < 8:
        suggestions.append("📝 添加meta description (50-160字符)")
    if result['breakdown']['structure']['score'] < 15:
        suggestions.append("🏗️  增加H2/H3子标题，提升内容结构")
    if result['breakdown']['content']['score'] < 18:
        suggestions.append("📄 扩展内容深度，目标1000+词")
    if result['breakdown']['freshness']['score'] < 5:
        suggestions.append("🕐 添加发布日期/最后更新标记")
    if result['breakdown']['links']['score'] < 6:
        suggestions.append("🔗 增加权威外部引用链接")

    if suggestions:
        print("改进建议:")
        for s in suggestions:
            print(f"  {s}")
    else:
        print("✅ 各方面表现良好！")

    # JSON输出
    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        print(f"\n📊 报告已保存: {args.output}")

    return result


if __name__ == "__main__":
    main()
