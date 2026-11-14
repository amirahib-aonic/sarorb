import json
import re
import urllib.request
import xml.etree.ElementTree as ET
from email.utils import parsedate_to_datetime

try:
    import truststore

    truststore.inject_into_ssl()
except ImportError:
    pass

from gdelt_fire_news import OUT_DIR, tag_regencies

FEEDS = {
    "antara_kalbar": "https://kalbar.antaranews.com/rss/terkini.xml",
    "tribun_pontianak": "https://pontianak.tribunnews.com/rss",
    "detik_kalimantan": "https://www.detik.com/kalimantan/rss",
    "mongabay_kalbar": "https://news.mongabay.com/location/west-kalimantan/feed/",
    "dayak_daily": "https://dayakdaily.com/feed/",
    "google_news": "https://news.google.com/rss/search?q=karhutla+Kalbar&hl=id&gl=ID&ceid=ID:id",
}
REGIONAL_FEEDS = {"mongabay_kalbar", "google_news"}
FIRE_TERMS = re.compile(
    r"karhutla|kebakaran hutan|kebakaran lahan|kabut asap|titik panas|hotspot|haze|jerebu|open burning|peat fire|ISPU",
    re.IGNORECASE,
)
PLACE_TERMS = re.compile(r"kalbar|kalimantan barat|west kalimantan|pontianak|sarawak|kuching|borneo", re.IGNORECASE)


def fetch_feed(url):
    req = urllib.request.Request(url, headers={
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0 Safari/537.36",
        "Accept": "application/rss+xml, application/xml, text/xml, */*",
        "Accept-Language": "id,en;q=0.8",
    })
    with urllib.request.urlopen(req, timeout=30) as resp:
        return ET.fromstring(resp.read())


def parse_date(text):
    try:
        return parsedate_to_datetime(text).strftime("%Y%m%d")
    except (TypeError, ValueError):
        return ""


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    rows, seen, stats = [], set(), {}
    for name, url in FEEDS.items():
        try:
            items = fetch_feed(url).iter("item")
        except Exception as e:
            stats[name] = f"error: {e}"
            continue
        total = kept = 0
        for item in items:
            total += 1
            title = (item.findtext("title") or "").strip()
            desc = re.sub(r"<[^>]+>", " ", item.findtext("description") or "")
            text = f"{title} {desc}"
            if not FIRE_TERMS.search(text):
                continue
            if name not in REGIONAL_FEEDS and not PLACE_TERMS.search(text) and not tag_regencies(text):
                continue
            if name == "google_news":
                title = title.rsplit(" - ", 1)[0]
            key = re.sub(r"\W+", " ", title.lower()).strip()
            if key in seen:
                continue
            seen.add(key)
            kept += 1
            rows.append({
                "date": parse_date(item.findtext("pubDate")),
                "title": title,
                "url": item.findtext("link"),
                "source": name,
                "regencies": tag_regencies(text),
            })
        stats[name] = f"{kept}/{total}"
    rows.sort(key=lambda r: r["date"], reverse=True)
    (OUT_DIR / "rss_articles.json").write_text(json.dumps(rows, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(stats, indent=1))
    print(f"kept={len(rows)} -> {OUT_DIR / 'rss_articles.json'}")
    for r in rows[:10]:
        print(r["date"], r["source"], r["regencies"], r["title"][:90])


if __name__ == "__main__":
    main()
