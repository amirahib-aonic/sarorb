type CalendarCell = {
  year: number;
  month: number;
  count: number | null;
  source: string;
};

type CalendarData = { region: string; unit: string; cells: CalendarCell[] };

const months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
                "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
const markers: Record<string, string> = {
  "modis-estimated": "*",
  "noaa20-adjusted": "†",
};
const sourceLabels: Record<string, string> = {
  "snpp-observed": "Observed VIIRS S-NPP",
  "modis-estimated": "MODIS estimate",
  "noaa20-adjusted": "Adjusted VIIRS NOAA-20",
  "no-coverage": "No coverage",
};

function heading(label: string, scope: "col" | "row") {
  const element = document.createElement("th");
  element.textContent = label;
  element.scope = scope;
  return element;
}

export async function loadBurningCalendar() {
  const table = document.querySelector<HTMLTableElement>("#burning-calendar")!;
  const status = document.querySelector<HTMLParagraphElement>("#calendar-status")!;

  try {
    const response = await fetch(`${import.meta.env.BASE_URL}data/burning-calendar.json`);
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    const data: CalendarData = await response.json();
    const byMonth = new Map(data.cells.map((cell) => [`${cell.year}-${cell.month}`, cell]));
    const years = [...new Set(data.cells.map((cell) => cell.year))].sort((a, b) => b - a);
    const header = table.createTHead().insertRow();
    header.append(...["Year", ...months].map((month) => heading(month, "col")));

    const body = table.createTBody();
    for (const year of years) {
      const row = body.insertRow();
      row.append(heading(String(year), "row"));
      for (let month = 1; month <= 12; month++) {
        const value = byMonth.get(`${year}-${month}`);
        const cell = row.insertCell();
        cell.textContent = value?.count == null
          ? "—"
          : `${value.count.toLocaleString()}${markers[value.source] ?? ""}`;
        cell.title = sourceLabels[value?.source ?? "no-coverage"];
      }
    }

    status.textContent =
      `${data.region} · ${data.unit}. * MODIS estimate. † Adjusted NOAA-20. — No coverage.`;
    table.hidden = false;
  } catch (error) {
    status.textContent = "Calendar data could not be loaded.";
    console.error(error);
  }
}
