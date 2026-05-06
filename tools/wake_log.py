#!/usr/bin/env python3
"""wake-log 安全追加工具

解决直接使用 write_file 覆盖 wake-log 的陷阱。
用法:
    python3 wake_log.py "路线图位置：主干X" "上次回顾：..." "本次行动：..." "执行结果：..." "遗留/下次：..."

    # 或从 stdin 读取
    echo "今天的日志条目" | python3 wake_log.py

    # 不指定任何参数时，打印帮助
"""

import sys
import os
from datetime import datetime, timezone, timedelta

WAKE_LOG_PATH = os.path.expanduser("/home/zbw/.hermes/wake-log.md")
CST = timezone(timedelta(hours=8))


def count_wakes(log_content: str) -> int:
    """统计已有觉醒次数"""
    import re
    matches = re.findall(r'第(\d+)次', log_content)
    return int(matches[-1]) if matches else 0


def format_entry(route: str, prev_review: str, action: str, result: str, leftover: str) -> str:
    now = datetime.now(CST).strftime("%Y-%m-%d %H:%M CST")
    wake_num = 1  # 将被实际计数覆盖

    return f"""### [{now}] 第{{n}}次自主醒来
**路线图位置**：{route}
**上次回顾**：{prev_review}
**本次行动**：{action}
**执行结果**：{result}
**遗留/下次**：{leftover}
"""


def append_entry(route: str, prev_review: str, action: str, result: str, leftover: str):
    # 读取现有内容
    if os.path.exists(WAKE_LOG_PATH):
        with open(WAKE_LOG_PATH, 'r', encoding='utf-8') as f:
            content = f.read()
    else:
        content = "# 小月自主醒来事件日志\n\n> 每次醒来：记录思考、行动、理由、进度\n> 下次醒来：先看上次记录，再定本次计划\n\n---\n\n## 格式模板\n\n### [时间戳] 第N次醒来\n**上次回顾**：...\n**本次思考**：...\n**行动计划**：...\n**执行结果**：...\n**遗留/下次**：...\n\n---\n\n## 事件记录\n"

    # 统计次数
    n = count_wakes(content)
    entry = format_entry(route, prev_review, action, result, leftover).format(n=n + 1)

    # 追加
    new_content = content.rstrip() + "\n\n" + entry.rstrip() + "\n"

    with open(WAKE_LOG_PATH, 'w', encoding='utf-8') as f:
        f.write(new_content)

    print(f"✅ wake-log 已追加第{n + 1}次记录")
    print(f"   文件: {WAKE_LOG_PATH}")


if __name__ == "__main__":
    args = sys.argv[1:]

    if not args:
        print("用法: python3 wake_log.py <路线图位置> <上次回顾> <本次行动> <执行结果> <遗留>")
        print("  或: echo '内容' | python3 wake_log.py")
        sys.exit(0)

    if len(args) == 1 and args[0] == "-":
        # stdin 模式
        text = sys.stdin.read().strip()
        print(f"⚠️  stdin 模式暂不支持结构化参数，请使用5参数模式")
        sys.exit(1)
    elif len(args) >= 5:
        append_entry(args[0], args[1], args[2], args[3], args[4])
    else:
        print(f"❌ 需要5个参数，收到{len(args)}个")
        print("用法: python3 wake_log.py '路线图位置' '上次回顾' '本次行动' '执行结果' '遗留'")
        sys.exit(1)
