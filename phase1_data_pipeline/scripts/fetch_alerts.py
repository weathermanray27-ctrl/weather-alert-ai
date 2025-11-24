"""Weather Alert Fetch Script

Fetches active alerts from the US National Weather Service (NWS) API
and saves the response JSON to `../data/alerts.json`.

This is a small, self-contained script intended to be run from the
repository root. It requires `requests` (already listed in
`requirements.txt`).
"""

from pathlib import Path
import json
import sys

import requests


def fetch_alerts(save_path: Path) -> dict:
	url = "https://api.weather.gov/alerts/active"
	headers = {"User-Agent": "weather-alert-ai (raysc)"}
	resp = requests.get(url, headers=headers, timeout=30)
	resp.raise_for_status()
	data = resp.json()

	save_path.parent.mkdir(parents=True, exist_ok=True)
	with save_path.open("w", encoding="utf-8") as fh:
		json.dump(data, fh, indent=2)

	return data


def summarize(data: dict) -> None:
	features = data.get("features", [])
	total = len(features)
	print(f"Fetched {total} active alerts")

	# Count by event type
	counts = {}
	for f in features:
		props = f.get("properties") or {}
		event = props.get("event") or "(unknown)"
		counts[event] = counts.get(event, 0) + 1

	top = sorted(counts.items(), key=lambda x: x[1], reverse=True)[:10]
	if top:
		print("Top alert types:")
		for name, c in top:
			print(f"  {name}: {c}")


def main():
	repo_root = Path(__file__).resolve().parents[2]
	out = repo_root / "phase1_data_pipeline" / "data" / "alerts.json"

	try:
		data = fetch_alerts(out)
		summarize(data)
	except requests.HTTPError as e:
		print("HTTP error fetching alerts:", e, file=sys.stderr)
		sys.exit(2)
	except Exception as e:
		print("Error fetching alerts:", e, file=sys.stderr)
		sys.exit(3)


if __name__ == "__main__":
	main()

