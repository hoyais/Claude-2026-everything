#!/usr/bin/env python3
"""아침 뉴스 10선 — RSS 후보 수집기 (표준 라이브러리만 사용).

수집 창(전날 08:00 ~ 기준일 08:00 KST)에 들어오는 기사를 피드별로 모아
마크다운 후보 목록으로 출력한다. 선정·요약은 하지 않는다.

사용법:
    python3 scripts/collect_rss.py                # 오늘(KST) 기준
    python3 scripts/collect_rss.py 2026-10-24     # 기준일 지정
    python3 scripts/collect_rss.py --out /tmp/candidates.md
    python3 scripts/collect_rss.py --desc         # 기사 요약까지 출력 (파일이 커진다)
"""
import argparse
import datetime as dt
import email.utils
import html
import re
import sys
import urllib.request
import xml.etree.ElementTree as ET

KST = dt.timezone(dt.timedelta(hours=9))

# (이름, 구분, URL). 피드를 추가·제거할 때는 이 목록만 고친다.
# 종합 피드(연합 news.xml 등)는 최근 7~8시간만 담아 24시간 창을 못 채우므로 섹션 피드를 쓴다.
GN_KR = "hl=ko&gl=KR&ceid=KR:ko"
GN_US = "hl=en-US&gl=US&ceid=US:en"
FEEDS = [
    ("Google 뉴스 주요", "국내", f"https://news.google.com/rss?{GN_KR}"),
    ("Google 뉴스 국내", "국내", f"https://news.google.com/rss/headlines/section/topic/NATION?{GN_KR}"),
    ("Google 뉴스 경제", "국내", f"https://news.google.com/rss/headlines/section/topic/BUSINESS?{GN_KR}"),
    ("연합뉴스 정치", "국내", "https://www.yna.co.kr/rss/politics.xml"),
    ("연합뉴스 북한", "국내", "https://www.yna.co.kr/rss/northkorea.xml"),
    ("연합뉴스 경제", "국내", "https://www.yna.co.kr/rss/economy.xml"),
    ("연합뉴스 마켓", "국내", "https://www.yna.co.kr/rss/market.xml"),
    ("연합뉴스 산업", "국내", "https://www.yna.co.kr/rss/industry.xml"),
    ("연합뉴스 사회", "국내", "https://www.yna.co.kr/rss/society.xml"),
    ("한국경제 경제", "국내", "https://www.hankyung.com/feed/economy"),
    ("한국경제 증권", "국내", "https://www.hankyung.com/feed/finance"),
    ("한국경제 IT", "국내", "https://www.hankyung.com/feed/it"),
    ("SBS 정치", "국내", "https://news.sbs.co.kr/news/SectionRssFeed.do?sectionId=01"),
    ("SBS 경제", "국내", "https://news.sbs.co.kr/news/SectionRssFeed.do?sectionId=02"),
    ("SBS 사회", "국내", "https://news.sbs.co.kr/news/SectionRssFeed.do?sectionId=03"),
    ("연합뉴스 국제", "해외", "https://www.yna.co.kr/rss/international.xml"),
    ("Google News Top", "해외", f"https://news.google.com/rss?{GN_US}"),
    ("Google News World", "해외", f"https://news.google.com/rss/headlines/section/topic/WORLD?{GN_US}"),
    ("Google News Business", "해외", f"https://news.google.com/rss/headlines/section/topic/BUSINESS?{GN_US}"),
    ("Google News Tech", "해외", f"https://news.google.com/rss/headlines/section/topic/TECHNOLOGY?{GN_US}"),
    ("BBC World", "해외", "https://feeds.bbci.co.uk/news/world/rss.xml"),
    ("BBC Business", "해외", "https://feeds.bbci.co.uk/news/business/rss.xml"),
    ("NYT World", "해외", "https://rss.nytimes.com/services/xml/rss/nyt/World.xml"),
    ("NYT Business", "해외", "https://rss.nytimes.com/services/xml/rss/nyt/Business.xml"),
    ("Al Jazeera", "해외", "https://www.aljazeera.com/xml/rss/all.xml"),
]

DC_DATE = "{http://purl.org/dc/elements/1.1/}date"


def window(base: dt.date):
    end = dt.datetime.combine(base, dt.time(8, 0), KST)
    return end - dt.timedelta(days=1), end


def parse_date(text):
    if not text:
        return None
    try:
        d = email.utils.parsedate_to_datetime(text)
    except (TypeError, ValueError):
        try:
            d = dt.datetime.fromisoformat(text.replace("Z", "+00:00"))
        except ValueError:
            return None
    return d if d.tzinfo else d.replace(tzinfo=KST)


def clean(text):
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", text or ""))).strip()


def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": "morning-news-briefing/1.0"})
    with urllib.request.urlopen(req, timeout=20) as r:
        return r.read()


def collect(name, url, start, end):
    root = ET.fromstring(fetch(url))
    out = []
    for it in root.iter("item"):
        d = parse_date(it.findtext("pubDate") or it.findtext(DC_DATE))
        if d is None or not (start <= d < end):
            continue
        src = it.find("source")
        link = (it.findtext("link") or "").strip()
        if "news.google.com" in link:
            # 구글 뉴스 링크는 긴 리다이렉트라 브리핑에 못 쓴다. 보도량 신호로만 쓰고 링크는 비운다.
            link = ""
        elif "bbc.co.uk" in link or "aljazeera.com" in link:
            link = link.split("?", 1)[0]  # 추적용 쿼리 제거
        out.append({
            "time": d.astimezone(KST),
            "title": clean(it.findtext("title")),
            "link": link,
            "outlet": clean(src.text) if src is not None and src.text else name,
            "desc": clean(it.findtext("description"))[:160],
        })
    out.sort(key=lambda x: x["time"], reverse=True)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("date", nargs="?", help="기준일 YYYY-MM-DD (기본: 오늘 KST)")
    ap.add_argument("--out", help="결과 파일 경로 (기본: 표준출력)")
    ap.add_argument("--desc", action="store_true", help="기사 요약(description)도 출력")
    args = ap.parse_args()

    base = dt.date.fromisoformat(args.date) if args.date else dt.datetime.now(KST).date()
    start, end = window(base)
    lines = [f"# RSS 후보 — {base}", "",
             f"수집 창: {start:%Y-%m-%d %H:%M} ~ {end:%Y-%m-%d %H:%M} KST", ""]
    status, total, seen = [], 0, set()
    for name, region, url in FEEDS:
        try:
            items = collect(name, url, start, end)
        except Exception as e:  # 피드 하나가 죽어도 나머지는 계속 수집한다
            status.append(f"- ❌ {name}: {type(e).__name__}: {e}")
            continue
        # 여러 섹션 피드에 같은 기사가 실리므로 링크·제목 기준으로 한 번만 남긴다
        unique = []
        for x in items:
            keys = {k for k in (x["link"], x["title"]) if k}
            if keys & seen:
                continue
            seen |= keys
            unique.append(x)
        items = unique
        status.append(f"- ✅ {name} ({region}): {len(items)}건")
        total += len(items)
        lines += [f"## {name} `[{region}]`", ""]
        for x in items:
            line = f"- {x['time']:%m-%d %H:%M} | {x['outlet']} | {x['title']}"
            lines.append(f"{line} | {x['link']}" if x["link"] else line)
            if args.desc and x["desc"] and x["desc"] != x["title"]:
                lines.append(f"  - {x['desc']}")
        lines.append("")

    head = ["## 피드 상태", "", *status, "", f"총 후보: {total}건", ""]
    text = "\n".join(lines[:4] + head + lines[4:])
    if args.out:
        with open(args.out, "w", encoding="utf-8") as f:
            f.write(text)
    else:
        sys.stdout.write(text)
    # 살아 있는 피드가 하나도 없으면 실패로 끝낸다
    sys.exit(0 if total else 1)


if __name__ == "__main__":
    main()
