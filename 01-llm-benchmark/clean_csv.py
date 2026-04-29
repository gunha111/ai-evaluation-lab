"""
Remove Gemini error rows from responses.csv.
Keeps GPT and Claude rows + any successful Gemini rows.
"""

import csv
from pathlib import Path

CSV_PATH = Path(__file__).resolve().parent / "results" / "responses.csv"

with open(CSV_PATH, "r", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    rows = list(reader)

# Keep all non-error rows. Drop Gemini errors specifically.
cleaned = [r for r in rows if r["model"] != "gemini"]

removed = len(rows) - len(cleaned)
print(f"Original rows:  {len(rows)}")
print(f"Removed:        {removed} (Gemini errors)")
print(f"Remaining rows: {len(cleaned)}")

# Write back
with open(CSV_PATH, "w", encoding="utf-8", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=rows[0].keys())
    writer.writeheader()
    writer.writerows(cleaned)

print(f"\n✅ Saved: {CSV_PATH}")