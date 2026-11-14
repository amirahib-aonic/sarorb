import json
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

ENDPOINT = "https://api.gdeltproject.org/api/v2/doc/doc"
QUERY = (
    '(karhutla OR "kebakaran hutan" OR "kabut asap" OR "titik panas" OR haze OR jerebu) '
    '(Kalbar OR "Kalimantan Barat" OR Pontianak OR Ketapang OR Sintang OR Sarawak OR "West Kalimantan")'
)
REGENCIES = [
    "Ketapang", "Sintang", "Kubu Raya", "Sanggau", "Kapuas Hulu", "Melawi", "Sekadau",
    "Landak", "Bengkayang", "Sambas", "Mempawah", "Kayong Utara", "Pontianak", "Singkawang",
    "Kuching", "Tebedu", "Serian", "Sri Aman",
]
OUT_DIR = Path(__file__).resolve().parent.parent / "data" / "news"


def fetch(mode, timespan, extra=None):
    params = {"query": QUERY, "mode": mode, "format": "json", "timespan": timespan}
    params.update(extra or {})
    url = f"{ENDPOINT}?{urllib.parse.urlencode(params)}"
    req = urllib.request.Request(url, headers={"User-Agent": "burning-calendar-research"})
    body = ""
    for attempt in range(5):
        try:
            with urllib.request.urlopen(req, timeout=60) as resp:
                body = resp.read().decode("utf-8", errors="replace")
            break
        except urllib.error.HTTPError as e:
            if e.code != 429 or attempt == 4:
                raise
            time.sleep(10 * (attempt + 1))
    try:
        return json.loads(body)
    except json.JSONDecodeError:
        raise RuntimeError(f"GDELT returned non-JSON: {body[:200]}")


def tag_regencies(title):
    lowered = title.lower()
    return [r for r in REGENCIES if r.lower() in lowered]


def main():
    timespan = sys.argv[1] if len(sys.argv) > 1 else "3months"
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    articles = fetch("artlist", timespan, {"maxrecords": "250", "sort": "datedesc"}).get("articles", [])
    seen = set()
    rows = []
    for a in articles:
        key = a.get("title", "").strip().lower()
        if not key or key in seen:
            continue
        seen.add(key)
        rows.append({
            "date": a.get("seendate", "")[:8],
            "title": a.get("title"),
            "url": a.get("url"),
            "domain": a.get("domain"),
            "language": a.get("language"),
            "source_country": a.get("sourcecountry"),
            "regencies": tag_regencies(a.get("title", "")),
        })
    (OUT_DIR / "articles.json").write_text(json.dumps(rows, ensure_ascii=False, indent=2), encoding="utf-8")

    time.sleep(6)
    timeline = fetch("timelinevol", timespan, {"timelinesmooth": "0"})
    series = timeline.get("timeline", [{}])[0].get("data", [])
    daily = [{"date": p["date"][:8], "volume_pct": p["value"]} for p in series]
    (OUT_DIR / "timeline.json").write_text(json.dumps(daily, indent=2), encoding="utf-8")

    tagged = sum(1 for r in rows if r["regencies"])
    print(f"articles={len(rows)} tagged={tagged} timeline_days={len(daily)} -> {OUT_DIR}")
    for r in rows[:8]:
        print(r["date"], r["language"], r["regencies"], r["title"][:90])


if __name__ == "__main__":
    main()
