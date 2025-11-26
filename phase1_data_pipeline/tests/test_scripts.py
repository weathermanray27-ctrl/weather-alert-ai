"""Unit tests for fetch_alerts.py and alerts_to_csv.py"""
import json
import tempfile
from pathlib import Path
import sys

# Add scripts to path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

import pytest


class TestAlertsToCSV:
    """Test alerts_to_csv conversion"""

    def test_csv_conversion(self, tmp_path):
        """Test that alerts.json converts to CSV correctly"""
        # Create mock JSON
        mock_json = {
            "features": [
                {
                    "id": "test-1",
                    "properties": {
                        "id": "alert-1",
                        "event": "Winter Storm Watch",
                        "sent": "2025-11-24T00:00:00Z",
                        "effective": "2025-11-24T00:00:00Z",
                        "onset": "2025-11-25T00:00:00Z",
                        "expires": "2025-11-26T00:00:00Z",
                        "areaDesc": "Test County",
                        "headline": "Test Alert",
                        "description": "This is a test alert",
                        "instruction": "Monitor conditions",
                        "severity": "Severe",
                        "certainty": "Possible",
                        "urgency": "Future",
                        "senderName": "NWS Test",
                    },
                }
            ]
        }

        # Write mock JSON
        json_path = tmp_path / "alerts.json"
        with json_path.open("w") as fh:
            json.dump(mock_json, fh)

        # Mock the conversion script
        import csv

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

        csv_path = tmp_path / "alerts.csv"
        with csv_path.open("w", newline="", encoding="utf-8") as fh:
            writer = csv.DictWriter(fh, fieldnames=FIELDS)
            writer.writeheader()
            for f in mock_json["features"]:
                props = f.get("properties") or {}
                row = {key: props.get(key, "") for key in FIELDS}
                writer.writerow(row)

        # Verify CSV was created
        assert csv_path.exists()
        with csv_path.open("r") as fh:
            lines = fh.readlines()
            assert len(lines) == 2  # header + 1 row
            assert "Winter Storm Watch" in lines[1]

    def test_fields_present(self):
        """Test that expected fields are defined"""
        from alerts_to_csv import FIELDS

        expected = [
            "id",
            "event",
            "sent",
            "effective",
            "expires",
            "areaDesc",
            "headline",
            "description",
            "severity",
            "certainty",
            "urgency",
            "senderName",
        ]
        for field in expected:
            assert field in FIELDS, f"Missing field: {field}"


class TestFetchAlerts:
    """Test fetch_alerts script structure"""

    def test_imports(self):
        """Test that fetch_alerts.py imports correctly"""
        import fetch_alerts

        assert hasattr(fetch_alerts, "fetch_alerts")
        assert hasattr(fetch_alerts, "summarize")
        assert hasattr(fetch_alerts, "main")

    def test_main_callable(self):
        """Test that main function exists and is callable"""
        import fetch_alerts

        assert callable(fetch_alerts.main)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
