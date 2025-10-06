"""
HTML report generation for analysis results
"""

import json
from pathlib import Path
from typing import List, Dict


class ReportGenerator:
    def __init__(self, output_dir: str):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def generate_report(self, detections: List[Dict], firmware_path: str) -> str:
        html_path = self.output_dir / "report.html"
        data_path = self.output_dir / "detections.json"
        data_path.write_text(json.dumps(detections, indent=2))
        html = self._render_html(firmware_path, detections)
        html_path.write_text(html)
        return str(html_path)

    def _render_html(self, firmware_path: str, detections: List[Dict]) -> str:
        rows = "\n".join(
            f"<tr><td>{i+1}</td><td>{d.get('function')}</td><td>{d.get('label')}</td><td>{d.get('confidence')}</td></tr>"
            for i, d in enumerate(detections)
        )
        return f"""
<!DOCTYPE html>
<html>
<head>
  <meta charset=\"utf-8\" />
  <title>Crypto Finder Report</title>
  <style>
    body {{ font-family: Arial, sans-serif; margin: 2rem; }}
    table {{ border-collapse: collapse; width: 100%; }}
    th, td {{ border: 1px solid #ccc; padding: 8px; text-align: left; }}
    th {{ background: #f6f6f6; }}
  </style>
  </head>
<body>
  <h1>Crypto Finder Report</h1>
  <p><strong>Firmware:</strong> {firmware_path}</p>
  <table>
    <thead><tr><th>#</th><th>Function</th><th>Label</th><th>Confidence</th></tr></thead>
    <tbody>
    {rows}
    </tbody>
  </table>
  <p>Raw detections saved alongside as detections.json</p>
</body>
</html>
"""


