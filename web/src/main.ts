import "./style.css";

type PreviewData = {
  sources: { file: string; rows: number }[];
};

const status = document.querySelector<HTMLParagraphElement>("#status")!;
const sources = document.querySelector<HTMLUListElement>("#sources")!;

async function loadPreview() {
  try {
    const response = await fetch(`${import.meta.env.BASE_URL}data/preview.json`);
    if (!response.ok) {
      throw new Error(`HTTP ${response.status}`);
    }

    const data: PreviewData = await response.json();
    for (const source of data.sources) {
      const item = document.createElement("li");
      item.textContent = `${source.file} · ${source.rows.toLocaleString()} input rows`;
      sources.append(item);
    }

    sources.hidden = data.sources.length === 0;
    status.textContent = sources.hidden
      ? "Baseline loaded. No FIRMS inputs processed yet."
      : "FIRMS input row counts";
  } catch (error) {
    status.textContent = "Preview data could not be loaded.";
    console.error(error);
  }
}

void loadPreview();
