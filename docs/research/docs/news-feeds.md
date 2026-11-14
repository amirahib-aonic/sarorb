# News feeds to enrich the West Kalimantan burning calendar

Status: initial research, 2026-11-13. Endpoints have not been tested yet.

## Why news helps a satellite-based burning calendar

Hotspot data (FIRMS/VIIRS) shows **where and when** fires happen. News adds what satellites cannot see:

1. **Impact:** school closures, flight disruptions and API readings in Sarawak. In Aug 2026, Tebedu passed API 200 and six schools closed.
2. **Ground truth and cause:** land clearing, peat fires, arrests and concession names.
3. **Response:** emergency status declarations, water bombing and burning bans. These help explain why hotspot counts drop.
4. **A seasonal signal:** monthly news volume on "kebakaran hutan Kalbar" should rise and fall with hotspot counts. That makes it a second line on the calendar.

## Candidate sources

| Source | Cost | History | Language / geo | Fit |
|---|---|---|---|---|
| **GDELT DOC 2.0 API** (`api.gdeltproject.org/api/v2/doc/doc`) | Free, no key | Rolling ~3 months | 65 languages including Indonesian; `sourcecountry:ID`, `sourcelang:ind` | **Best first choice.** Use `mode=timelinevol` for monthly volume and `mode=artlist&format=json` for headlines |
| **GDELT GKG / Events via BigQuery** | Free tier, 1 TB/month of queries | 2015 onward | Geocoded to ADM1 (Kalimantan Barat) | Multi-year seasonality. Use it to build the historical calendar layer |
| **Regional RSS**: Mongabay, Ekuatorial (WP JSON at `/wp-json/wp/v2/posts`), Bernama Sarawak, The Star ASEAN+, RRI Pontianak, Antara Kalbar, Pontianak Post | Free | Varies | Local, high relevance | Curated, high-precision feed. Small scraper plus keyword filter |
| **NewsAPI.org** | Free tier only for dev use, delayed by 24h, 1 month of history | Short | Weak Indonesian coverage | Skip |
| **GNews / NewsData.io / Mediastack** | Free tiers with about 100–200 requests a day | Short | Some coverage for ID/MY | Fallback only |
| **Google News RSS** (`news.google.com/rss/search?q=...&hl=id&gl=ID`) | Free, unofficial | Recent | Strong Indonesian coverage | Quick prototype. The terms of service are grey, so don't use it in production |
| **ReliefWeb API** | Free | Many years | Humanitarian reports, ASEAN haze | Official situation reports for major haze years (2015, 2019, 2023) |
| **ASMC (ASEAN Specialised Met Centre)** haze outlooks | Free | Seasonal | Regional | Not news, but a strong authoritative layer for the calendar |

## Feeds that responded in BrowserOS (2026-11-13)

Each of these returned XML. Only the first few hundred characters of each were read, so item contents and relevance have not been checked.

| Feed | URL | Notes |
|---|---|---|
| Antara Kalbar | `https://kalbar.antaranews.com/rss/terkini.xml` | State news agency. Covers BPBD emergency-status extensions such as "perpanjang tanggap darurat karhutla" |
| Tribun Pontianak | `https://pontianak.tribunnews.com/rss` | Daily BPBD hotspot updates by regency (Ketapang and others) |
| detikKalimantan | `https://www.detik.com/kalimantan/rss` | Kalimantan-wide coverage. Needs a Kalbar keyword filter |
| Mongabay, West Kalimantan | `https://news.mongabay.com/location/west-kalimantan/feed/` | Already filtered to the region. Peat, concessions and causes |
| Dayak Daily (Sarawak) | `https://dayakdaily.com/feed/` | NREB Sarawak hotspot counts. Aug 2026: 148 hotspots in Sarawak against 7,286 in Kalimantan |
| Google News RSS | `https://news.google.com/rss/search?q=karhutla+Kalbar&hl=id&gl=ID&ceid=ID:id` | Gathers all of the above and more |

Also found, without a confirmed feed: Malay Mail (haze in Sarawak, AQI 191 in Pontianak, more than 4,000 Kalbar hotspots) and The Star ASEAN+.

Not reachable: SiPongi, the official Indonesian hotspot portal. Neither `sipongi.kemenhut.go.id` nor `sipongi.menlhk.go.id` resolved in DNS. The current domain needs to be confirmed.

## Suggested queries

- Indonesian: `("kebakaran hutan" OR karhutla OR "titik panas" OR kabut asap) (Kalbar OR "Kalimantan Barat" OR Pontianak OR Ketapang OR Sintang)`
- English and Malay: `(haze OR jerebu OR "open burning") (Sarawak OR Kuching OR "West Kalimantan")`

## Proposed pipeline

1. A daily job pulls GDELT DOC artlist and RSS, dedupes by URL and title, and keeps items that match the keywords.
2. Tag each item with a regency (Ketapang, Sintang, Kubu Raya, and so on) using a gazetteer match, then attach it to that regency and day.
3. Join with FIRMS hotspot counts per regency and day. The calendar cell shows hotspot intensity plus a news-count badge, with headlines on hover.
4. Backfill multi-year seasonality from GDELT GKG in BigQuery.
5. Optional: classify each article with an LLM as impact, cause, response or noise, so the badge shows the article type.

## Open questions

- Is the calendar a static analysis or a live dashboard? A live dashboard needs a scheduler.
- Is Sarawak impact news in scope, or only fire activity inside West Kalimantan?

## Sources

- [Mongabay: Indonesia's wildfire season surges as haze spreads into Malaysia (Aug 2026)](https://news.mongabay.com/2026/08/indonesias-wildfire-season-surges-as-haze-spreads-into-malaysia/)
- [The Star: Kalimantan fires rage as response lags](https://www.thestar.com.my/aseanplus/aseanplus-news/2026/08/22/kalimantan-fires-rage-as-response-lags)
- [The Star: Thick haze disrupts flights on Borneo](https://www.thestar.com.my/aseanplus/aseanplus-news/2026/09/14/thick-haze-disrupts-flights-on-indonesia039s-borneo-island-poor-visibility-also-hampers-firefighting-efforts)
- [RRI: Hundreds of hotspots across 12 West Kalimantan regencies](https://rri.co.id/voice-of-indonesia/archipelago/2609638/hundreds-of-hotspots-detected-across-12-west-kalimantan-regencies)
- [Ekuatorial WP JSON feed](https://www.ekuatorial.com/en/wp-json/wp/v2/posts/64348)
- [Bernama Sarawak region news](https://bernama.com/en/region/news.php?id=2603131)
