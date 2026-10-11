
import csv
from pathlib import Path
from collections import Counter

source = Path("data/ghaziabad_healthcare_dedup_review_fixed.csv")
output = Path("data/ghaziabad_healthcare_import_ready.csv")

blocked_flags = {
    "CHECK_DISTRICT_LOCATION",
    "DUPLICATE_CANDIDATE_NAME",
    "POSSIBLE_DUPLICATE",
    "NEAR_EXISTING_RESOURCE",
    "CHECK_PLACE_TYPE",
    "CHECK_BRANCH",
}

with source.open(encoding="utf-8-sig", newline="") as f:
    rows = list(csv.DictReader(f))

ready = []
held = []

for row in rows:
    flags = {
        flag.strip()
        for flag in row.get("review_flags", "").split(";")
        if flag.strip() and flag.strip() != "NONE"
    }

    if flags & blocked_flags:
        held.append(row)
    else:
        ready.append(row)

if ready:
    with output.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=ready[0].keys())
        writer.writeheader()
        writer.writerows(ready)

print("PREVIEW ONLY — database unchanged")
print("Original candidates:", len(rows))
print("Ready for next-stage review:", len(ready))
print("Held for manual review:", len(held))
print("Held reasons:", dict(Counter(
    flag
    for row in held
    for flag in row.get("review_flags", "").split(";")
    if flag.strip() in blocked_flags
)))
print("Preview saved:", output)
print("Reminder: ready records are still unverified.")
