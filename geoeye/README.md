# geoeye — AI Search Visibility Analyzer

Your website in the eyes of ChatGPT, Perplexity, and Google AI Overviews.

geoeye scans any URL and tells you how likely AI search engines are to cite your content — and exactly what to fix.

```bash
pip install geoeye
geoeye https://yoursite.com --verbose
```

## Output
```
┌──────────────────────────────────────┐
│  AI引用评分:  77/100  →  B — AI可能引用             │
└──────────────────────────────────────┘
  title        [██████████] 20/20  理想长度
  structure    [████████████] 25/25  层级清晰
  content      [████████████] 25/25  深度内容
  freshness    [░░░░░░░░░░] 1/10  无时间戳
```

## How it works

Six dimensions, all offline, zero API cost:

| Factor | Weight | What it checks |
|--------|--------|----------------|
| Title quality | 20 | Length, clarity, keyword presence |
| Meta description | 10 | Exists, proper length |
| Structure | 25 | H1/H2/H3 hierarchy — AI parsability |
| Content depth | 25 | Word count, paragraph density |
| Freshness signal | 10 | Date stamps, update frequency |
| Citation network | 10 | Outbound authority links |

## Why this matters

Traditional SEO optimizes for crawlers. GEO optimizes for AI readers. The rules are different:

- **SEO cares about backlinks** → GEO cares about citability
- **SEO cares about keyword density** → GEO cares about structure and clarity  
- **SEO takes months** → GEO changes take days

## Quick start

```bash
# Analyze any page
geoeye https://example.com

# Detailed breakdown
geoeye https://example.com --verbose

# Export JSON report
geoeye https://example.com -o report.json
```

## Install

```bash
pip install geoeye
```

Or from source:
```bash
git clone https://github.com/qianhe315/Hermes.git
cd Hermes/geoeye
python3 geoeye.py https://example.com
```

## Who needs this

- Content marketers who want AI traffic
- SaaS founders optimizing for Perplexity/ChatGPT
- SEO professionals transitioning to GEO
- Anyone with a website in 2026

AI search is eating traditional search. geoeye helps you get cited instead of ignored.

---

**MIT License** — free, open-source, no strings.
