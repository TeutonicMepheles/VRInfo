#!/usr/bin/env python3
"""Generate year-to-date VR interaction research cards as Markdown.

This script is network-independent: it outputs actionable source-entry links
(arXiv / ACM / IEEE) and can embed fetched papers if `data/cards.json` has them.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
from pathlib import Path
from urllib.parse import quote_plus

ROOT = Path(__file__).resolve().parents[1]
CARDS_FILE = ROOT / "data" / "cards.json"


def build_query_links(topic: str, start: str, end: str) -> dict[str, str]:
    q = quote_plus(topic)
    return {
        "arXiv": f"https://arxiv.org/search/?query={q}&searchtype=all&abstracts=show&order=-announced_date_first&size=50",
        "ACM": f"https://dl.acm.org/action/doSearch?AllField={q}",
        "IEEE": f"https://ieeexplore.ieee.org/search/searchresult.jsp?queryText={q}",
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--start", default=f"{dt.date.today().year}-01-01")
    parser.add_argument("--end", default=dt.date.today().isoformat())
    parser.add_argument("--topic", default="virtual reality interaction design")
    args = parser.parse_args()

    cards = []
    if CARDS_FILE.exists():
        cards = json.loads(CARDS_FILE.read_text(encoding="utf-8"))

    links = build_query_links(args.topic, args.start, args.end)

    print(f"# VR 交互设计成果卡片（{args.start} 至 {args.end}）\n")
    print("- 说明：当前环境若无法直连论文 API，会优先输出官方数据库检索入口。")
    print("- 主题：", args.topic)
    print("\n## 检索入口")
    for name, url in links.items():
        print(f"- {name}: {url}")

    print("\n## 今日卡片")
    if cards:
        card = cards[0]
        print(f"- 日期：{card.get('date','')}")
        print(f"- 标题：{card.get('title','')}")
        print(f"- 摘要：{card.get('summary','')}")
        papers = card.get("papers", [])
        if papers:
            print("- 原文链接：")
            for p in papers:
                print(f"  - [{p.get('source','')}] {p.get('title','')} - {p.get('url','')}")
        else:
            print("- 原文链接：暂无（请使用上方三库检索入口查看当日最新结果）")
    else:
        print("- 暂无卡片数据，请先运行 scripts/generate_daily_card.py")


if __name__ == "__main__":
    main()
