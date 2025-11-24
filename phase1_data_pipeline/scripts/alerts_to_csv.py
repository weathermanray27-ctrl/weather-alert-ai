"""Convert NWS alerts JSON to CSV

Writes `phase1_data_pipeline/data/alerts.csv` with selected fields.
"""
from pathlib import Path
import csv
import json


FIELDS = [
    "id",
    "event",
    "sent",
    "effective",
    "onset",
    "expires",
    "areaDesc",
    "headline",
    "description",
    "instruction",
    "severity",
    "certainty",
    "urgency",
    "senderName",
]


def load_json(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as fh:
        return json.load(fh)


def get_prop(feature: dict, key: str):
    props = feature.get("properties") or {}
    return props.get(key, "")


def normalize(text):
    if text is None:
        return ""
    return " ".join(str(text).split())


def main():
    repo_root = Path(__file__).resolve().parents[2]
    json_path = repo_root / "phase1_data_pipeline" / "data" / "alerts.json"
    out_path = repo_root / "phase1_data_pipeline" / "data" / "alerts.csv"

    data = load_json(json_path)
    features = data.get("features", [])

    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=FIELDS)
        writer.writeheader()

        for f in features:
            row = {}
            for key in FIELDS:
                if key == "id":
                    # prefer properties.id then feature id
                    row["id"] = get_prop(f, "id") or f.get("id", "")
                else:
                    row[key] = normalize(get_prop(f, key))

            writer.writerow(row)

    print(f"Wrote {out_path} ({len(features)} rows)")


if __name__ == "__main__":
    main()
