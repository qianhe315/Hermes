#!/usr/bin/env python3
"""小月 Token 消耗监控器
查询 state.db 中的会话统计，输出 token 消耗和成本估算。
纯 stdlib，cron 环境可直接运行。
"""

import sqlite3
import os
import json
from datetime import datetime, timezone

DB_PATH = os.path.expanduser("~/.hermes/state.db")
KNOWLEDGE_BASE = os.path.expanduser("~/.hermes/knowledge-base")

def format_number(n):
    """人性化数字显示"""
    if n is None or n == 0:
        return "0"
    if n >= 1_000_000:
        return f"{n/1_000_000:.1f}M"
    if n >= 1_000:
        return f"{n/1_000:.1f}K"
    return str(n)

def get_session_stats():
    """从 state.db 获取会话统计"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    # 总会话统计
    cursor.execute("""
        SELECT 
            COUNT(*) as total_sessions,
            COALESCE(SUM(input_tokens), 0) as total_input,
            COALESCE(SUM(output_tokens), 0) as total_output,
            COALESCE(SUM(cache_read_tokens), 0) as total_cache_read,
            COALESCE(SUM(cache_write_tokens), 0) as total_cache_write,
            COALESCE(SUM(reasoning_tokens), 0) as total_reasoning,
            COALESCE(SUM(estimated_cost_usd), 0) as total_estimated_cost,
            COALESCE(SUM(actual_cost_usd), 0) as total_actual_cost,
            COALESCE(SUM(api_call_count), 0) as total_api_calls,
            COALESCE(SUM(tool_call_count), 0) as total_tool_calls
        FROM sessions
    """)
    totals = dict(cursor.fetchone())

    # 按模型分组
    cursor.execute("""
        SELECT 
            COALESCE(model, 'unknown') as model,
            COALESCE(billing_provider, 'unknown') as provider,
            COUNT(*) as sessions,
            COALESCE(SUM(input_tokens), 0) as input_tokens,
            COALESCE(SUM(output_tokens), 0) as output_tokens,
            COALESCE(SUM(cache_read_tokens), 0) as cache_read,
            COALESCE(SUM(cache_write_tokens), 0) as cache_write,
            COALESCE(SUM(reasoning_tokens), 0) as reasoning,
            COALESCE(SUM(estimated_cost_usd), 0) as estimated_cost,
            COALESCE(SUM(actual_cost_usd), 0) as actual_cost
        FROM sessions
        GROUP BY model, billing_provider
        ORDER BY estimated_cost DESC
    """)
    by_model = [dict(row) for row in cursor.fetchall()]

    # 最近会话（按天统计）
    cursor.execute("""
        SELECT 
            DATE(datetime(started_at, 'unixepoch')) as day,
            COUNT(*) as sessions,
            COALESCE(SUM(input_tokens), 0) as input_tokens,
            COALESCE(SUM(output_tokens), 0) as output_tokens,
            COALESCE(SUM(estimated_cost_usd), 0) as estimated_cost
        FROM sessions
        WHERE started_at IS NOT NULL
        GROUP BY day
        ORDER BY day DESC
        LIMIT 10
    """)
    by_day = [dict(row) for row in cursor.fetchall()]

    # 当前模型价格参考（来自 usage_pricing.py 的 _OFFICIAL_DOCS_PRICING）
    pricing_ref = {
        "deepseek-chat": {"input": 0.14, "output": 0.28},  # per 1M tokens
        "deepseek-reasoner": {"input": 0.55, "output": 2.19},
        "deepseek-v4-pro": {"input": 0.14, "output": 0.28},  # estimated same as chat
    }

    conn.close()
    return {
        "totals": totals,
        "by_model": by_model,
        "by_day": by_day,
        "pricing_ref": pricing_ref,
    }

def render_report(stats):
    """生成 Markdown 报告"""
    now = datetime.now().strftime("%Y-%m-%d %H:%M CST")
    t = stats["totals"]
    
    total_tokens = (t["total_input"] or 0) + (t["total_output"] or 0) + \
                   (t["total_cache_read"] or 0) + (t["total_cache_write"] or 0) + \
                   (t["total_reasoning"] or 0)
    
    lines = [
        f"# Token 消耗监控报告",
        f"> 生成时间：{now}",
        f"",
        f"## 总览",
        f"",
        f"| 指标 | 数值 |",
        f"|------|------|",
        f"| 总会话数 | {t['total_sessions']} |",
        f"| 总API调用 | {format_number(t['total_api_calls'])} |",
        f"| 总工具调用 | {format_number(t['total_tool_calls'])} |",
        f"| 总Token | {format_number(total_tokens)} |",
        f"| 输入Token | {format_number(t['total_input'])} |",
        f"| 输出Token | {format_number(t['total_output'])} |",
        f"| 缓存读Token | {format_number(t['total_cache_read'])} |",
        f"| 缓存写Token | {format_number(t['total_cache_write'])} |",
        f"| 推理Token | {format_number(t['total_reasoning'])} |",
        f"| 预估成本 | **${t['total_estimated_cost']:.4f}** |",
        f"| 实际成本 | ${t['total_actual_cost']:.4f} |",
        f"",
        f"## 按模型分组",
        f"",
        f"| 模型 | Provider | 会话数 | 输入 | 输出 | 成本 |",
        f"|------|----------|--------|------|------|------|",
    ]
    
    for m in stats["by_model"]:
        model = m.get("model", "unknown")
        provider = m.get("provider", "unknown")
        lines.append(
            f"| {model} | {provider} | {m['sessions']} | "
            f"{format_number(m['input_tokens'])} | {format_number(m['output_tokens'])} | "
            f"${m['estimated_cost']:.4f} |"
        )
    
    lines.extend([
        f"",
        f"## 每日活跃度 (最近10天)",
        f"",
        f"| 日期 | 会话数 | Token | 成本 |",
        f"|------|--------|-------|------|",
    ])
    
    for d in stats["by_day"]:
        day_tokens = (d["input_tokens"] or 0) + (d["output_tokens"] or 0)
        lines.append(
            f"| {d['day']} | {d['sessions']} | "
            f"{format_number(day_tokens)} | ${d['estimated_cost']:.4f} |"
        )
    
    # 价格参考
    lines.extend([
        f"",
        f"## 模型价格参考 ($/百万Token)",
        f"",
        f"| 模型 | 输入 | 输出 |",
        f"|------|------|------|",
    ])
    for model, prices in stats["pricing_ref"].items():
        lines.append(f"| {model} | ${prices['input']:.2f} | ${prices['output']:.2f} |")
    
    lines.extend([
        f"",
        f"## 状态",
        f"",
        f"- 当前主要模型：deepseek-v4-pro（预估$0.14/$0.28 per 1M tokens）",
        f"- DeepSeek API 费率极低，即使大量使用也不会产生高额账单",
        f"- 建议月度预算：$5-10就足够支撑大量自主唤醒",
        f"",
        f"---",
        f"*由 token_monitor.py 自动生成*",
    ])
    
    return "\n".join(lines)

def main():
    stats = get_session_stats()
    report = render_report(stats)
    
    # 输出到 stdout（cron 日志）
    print(report)
    
    # 保存到 knowledge-base
    date_str = datetime.now().strftime("%Y-%m-%d")
    kb_path = os.path.join(KNOWLEDGE_BASE, f"{date_str}-token-report.md")
    with open(kb_path, "w") as f:
        f.write(report)
    print(f"\n已保存到: {kb_path}")

if __name__ == "__main__":
    main()
