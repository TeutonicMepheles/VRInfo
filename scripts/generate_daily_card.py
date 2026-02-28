#!/usr/bin/env python3
"""Generate a daily VR interaction design result card.

Data sources:
- arXiv API
- Crossref API (filtered by publisher keyword for ACM/IEEE)
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path
from urllib.error import URLError

ROOT = Path(__file__).resolve().parents[1]
CARDS_FILE = ROOT / "data" / "cards.json"


def fetch_json(url: str) -> dict:
    req = urllib.request.Request(url, headers={"User-Agent": "VRInfoBot/1.0"})
    with urllib.request.urlopen(req, timeout=20) as r:
        return json.loads(r.read().decode("utf-8"))


def fetch_text(url: str) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": "VRInfoBot/1.0"})
    with urllib.request.urlopen(req, timeout=20) as r:
        return r.read().decode("utf-8")


def fetch_arxiv() -> list[dict]:
    query = 'all:"virtual reality" AND all:"interaction design"'
    params = {
        "search_query": query,
        "start": 0,
        "max_results": 5,
        "sortBy": "submittedDate",
        "sortOrder": "descending",
    }
    url = "https://export.arxiv.org/api/query?" + urllib.parse.urlencode(params)
    xml_str = fetch_text(url)

    ns = {"a": "http://www.w3.org/2005/Atom"}
    root = ET.fromstring(xml_str)
    papers = []
    for entry in root.findall("a:entry", ns):
        title = (entry.findtext("a:title", default="", namespaces=ns) or "").strip().replace("\n", " ")
        link = ""
        for lk in entry.findall("a:link", ns):
            href = lk.attrib.get("href", "")
            if "abs" in href:
                link = href
                break
        published = entry.findtext("a:published", default="", namespaces=ns)[:10]
        if title and link and published >= "2025-01-01":
            papers.append({"title": title, "source": "arXiv", "url": link, "published": published})
    return papers[:2]


def fetch_crossref(query: str, publisher_hint: str) -> list[dict]:
    params = {
        "query.bibliographic": query,
        "rows": 20,
        "sort": "published",
        "order": "desc",
        "filter": "from-pub-date:2025-01-01",
        "mailto": "noreply@example.com",
    }
    url = "https://api.crossref.org/works?" + urllib.parse.urlencode(params)
    data = fetch_json(url)
    items = data.get("message", {}).get("items", [])

    out = []
    hint = publisher_hint.lower()
    for item in items:
        publisher = (item.get("publisher") or "").lower()
        container = " ".join(item.get("container-title") or []).lower()
        if hint not in publisher and hint not in container:
            continue
        title_list = item.get("title") or []
        if not title_list:
            continue
        doi = item.get("DOI")
        if not doi:
            continue
        published_parts = (item.get("published-print") or item.get("published-online") or {}).get("date-parts", [[None, None, None]])[0]
        yyyy = str(published_parts[0]) if published_parts and published_parts[0] else ""
        mm = f"{published_parts[1]:02d}" if len(published_parts) > 1 and published_parts[1] else "01"
        dd = f"{published_parts[2]:02d}" if len(published_parts) > 2 and published_parts[2] else "01"
        out.append(
            {
                "title": title_list[0],
                "source": "ACM" if hint == "acm" else "IEEE",
                "url": f"https://doi.org/{doi}",
                "published": f"{yyyy}-{mm}-{dd}" if yyyy else "",
            }
        )
        if len(out) >= 1:
            break
    return out


def build_card(date_s: str) -> dict:
    summary = "今日卡片聚焦近期 VR 交互设计论文：关注多模态输入融合、协同任务设计和可访问性提升。"
    try:
        arxiv = fetch_arxiv()
        acm = fetch_crossref("virtual reality interaction design", "acm")
        ieee = fetch_crossref("virtual reality interaction design", "ieee")
        papers = (arxiv + acm + ieee)[:3]
    except URLError:
        papers = []
        summary = "今日抓取受网络限制影响，暂未拉取到论文；请稍后重试以获取带完整原文链接的最新成果。"

    if not papers:
        summary = "今日暂未抓取到 2025 年及之后的可用结果；请稍后重试以获取带完整原文链接的最新成果。"

    return {
        "date": date_s,
        "topic": "VR交互设计",
        "title": "每日成果卡片：多模态、协同与可访问性交互",
        "summary": summary,
        "papers": papers,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--date", default=dt.date.today().isoformat())
    args = parser.parse_args()

    CARDS_FILE.parent.mkdir(parents=True, exist_ok=True)
    card = build_card(args.date)

    cards = []
    if CARDS_FILE.exists():
        cards = json.loads(CARDS_FILE.read_text(encoding="utf-8"))

    cards = [c for c in cards if c.get("date") != args.date]
    cards.insert(0, card)
    CARDS_FILE.write_text(json.dumps(cards, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Updated {CARDS_FILE} with card for {args.date}")


if __name__ == "__main__":
    main()
