const BBOX = "108.5,-5,119.5,7.5";
const CHUNK = 5;
const MAX_DAYS = 30;
const SOURCES = [
  ["VIIRS_SNPP_NRT", "VIIRS S-NPP"],
  ["VIIRS_NOAA20_NRT", "VIIRS NOAA-20"],
];

const isoDay = (d) => d.toISOString().slice(0, 10);

async function fetchSource(key, product, start, end) {
  const rows = [];
  for (let d = new Date(start); d <= end; d.setUTCDate(d.getUTCDate() + CHUNK)) {
    const span = Math.min(CHUNK, Math.round((end - d) / 864e5) + 1);
    const url = `https://firms.modaps.eosdis.nasa.gov/api/area/csv/${key}/${product}/${BBOX}/${span}/${isoDay(d)}`;
    const r = await fetch(url);
    const text = await r.text();
    if (!r.ok || !text.startsWith("latitude")) throw new Error(`FIRMS ${product} ${r.status}: ${text.slice(0, 120)}`);
    const [head, ...lines] = text.trim().split("\n");
    const col = Object.fromEntries(head.split(",").map((h, i) => [h, i]));
    for (const line of lines) {
      const f = line.split(",");
      if (f[col.confidence] === "l") continue;
      rows.push([+f[col.latitude], +f[col.longitude], f[col.acq_date]]);
    }
  }
  return rows;
}

export default async function handler(req, res) {
  const key = process.env.FIRMS_MAP_KEY;
  if (!key) return res.status(503).json({ error: "FIRMS_MAP_KEY is not set" });
  const after = String(req.query.after || "");
  if (!/^\d{4}-\d{2}-\d{2}$/.test(after)) return res.status(400).json({ error: "after=YYYY-MM-DD is required" });

  const start = new Date(after + "T00:00:00Z");
  start.setUTCDate(start.getUTCDate() + 1);
  const today = new Date(isoDay(new Date()) + "T00:00:00Z");
  const end = new Date(Math.min(today, start.getTime() + (MAX_DAYS - 1) * 864e5));
  if (start > end) return res.status(200).json({ source: null, rows: [] });

  try {
    for (const [product, source] of SOURCES) {
      const rows = await fetchSource(key, product, start, end);
      if (rows.length) {
        res.setHeader("Cache-Control", "public, s-maxage=1800, stale-while-revalidate=3600");
        return res.status(200).json({ source, from: isoDay(start), to: isoDay(end), rows });
      }
    }
    res.setHeader("Cache-Control", "public, s-maxage=900");
    return res.status(200).json({ source: null, from: isoDay(start), to: isoDay(end), rows: [] });
  } catch (e) {
    return res.status(502).json({ error: String(e.message || e) });
  }
}
