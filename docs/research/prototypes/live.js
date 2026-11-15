window.PROTO_READY = (async () => {
  const D = window.PROTO_DATA;
  const R = D.r;
  const monthKey = (date) => date.slice(0, 7);

  const inRing = (x, y, ring) => {
    let inside = false;
    for (let i = 0, j = ring.length - 1; i < ring.length; j = i++) {
      const [xi, yi] = ring[i], [xj, yj] = ring[j];
      if (yi > y !== yj > y && x < ((xj - xi) * (y - yi)) / (yj - yi) + xi) inside = !inside;
    }
    return inside;
  };
  const polygons = D.presets
    .filter((p) => p.level === 1)
    .flatMap((p) => (p.geom.type === "Polygon" ? [p.geom.coordinates] : p.geom.coordinates));
  const inBorneo = (lon, lat) => polygons.some((pl) => inRing(lon, lat, pl[0]) && !pl.slice(1).some((h) => inRing(lon, lat, h)));

  let live;
  try {
    const ctl = new AbortController();
    const timer = setTimeout(() => ctl.abort(), 8000);
    const res = await fetch("api/firms?after=" + D.lastDate, { signal: ctl.signal });
    clearTimeout(timer);
    if (!res.ok) return;
    live = await res.json();
  } catch {
    return;
  }
  if (!live.source || !live.rows.length) return;

  const cellId = new Map(D.cells.map(([x, y], i) => [x + "," + y, i]));
  const added = {};
  let last = D.lastDate;
  for (const [lat, lon, date] of live.rows) {
    if (date <= D.lastDate || !inBorneo(lon, lat)) continue;
    const gx = Math.floor(lon / D.cell), gy = Math.floor(lat / D.cell), id = gx + "," + gy;
    if (!cellId.has(id)) {
      cellId.set(id, D.cells.length);
      D.cells.push([gx, gy]);
    }
    const k = monthKey(date), c = cellId.get(id);
    (added[k] ||= new Map()).set(c, (added[k].get(c) || 0) + 1);
    if (date > last) last = date;
  }
  if (last === D.lastDate) return;

  const weight = live.source === "VIIRS NOAA-20" ? 1 / R : 1;
  for (const [k, cells] of Object.entries(added)) {
    let rec = D.months[k];
    if (!rec) rec = D.months[k] = { s: live.source, w: weight, c: [] };
    const scale = weight / rec.w;
    const merged = new Map(rec.c);
    for (const [c, n] of cells) merged.set(c, (merged.get(c) || 0) + n * scale);
    rec.c = [...merged];
  }

  const curKey = monthKey(last), cutDay = +last.slice(8, 10), curMonth = curKey.slice(5);
  for (const [k, rec] of Object.entries(D.months)) {
    delete rec.p;
    if (k === curKey) rec.p = rec.c.slice();
    else if (k.slice(5) === curMonth && rec.d) {
      const p = new Map();
      for (const [c, d, n] of rec.d) if (d <= cutDay) p.set(c, (p.get(c) || 0) + n);
      rec.p = [...p];
    }
  }
  D.current = curKey;
  D.cutDay = cutDay;
  D.live = { source: live.source, from: D.lastDate, rows: live.rows.length };
  D.lastDate = last;
})();
