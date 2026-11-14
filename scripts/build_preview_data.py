"""Write a small browser-readable preview of the offline FIRMS pipeline."""

import argparse
import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "web" / "public" / "data" / "preview.json"


def build_preview(paths: list[Path]) -> dict:
    sources = []
    for path in paths:
        with path.open(encoding="utf-8-sig", newline="") as source:
            rows = csv.DictReader(source)
            required = {"latitude", "longitude", "acq_date", "acq_time"}
            missing = required.difference(rows.fieldnames or [])
            if missing:
                raise ValueError(f"{path.name}: missing columns {', '.join(sorted(missing))}")
            sources.append({"file": path.name, "rows": sum(1 for _ in rows)})
    return {"sources": sources}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("csv_files", nargs="*", type=Path, help="FIRMS CSV inputs")
    args = parser.parse_args()

    try:
        payload = build_preview(args.csv_files)
        OUTPUT.parent.mkdir(parents=True, exist_ok=True)
        OUTPUT.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    except (OSError, ValueError, csv.Error) as error:
        parser.exit(1, f"{error}\n")

    print(f"Wrote {OUTPUT.relative_to(ROOT)} with {len(payload['sources'])} source(s).")


if __name__ == "__main__":
    main()
