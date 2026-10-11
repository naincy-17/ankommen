
import csv
from pathlib import Path

source = Path("data/ghaziabad_healthcare_final_candidate.csv")
output = Path("data/ghaziabad_healthcare_dedup_review.csv")

with source.open(encoding="utf-8-sig", newline="") as f:
    rows = list(csv.DictReader(f))

# Keep one entry from each likely duplicate pair.
# Hold the other entries for manual review instead of deleting them.
seen = set()
review = []

for row in rows:
    name = row["name"].strip().casefold()
    if name in {"shanti gopal hospital", "manipal hospital"}:
        if name in seen:
            row["review_flags"] = (
                row.get("review_flags", "") + ";POSSIBLE_DUPLICATE"
            ).strip(";")
        else:
            seen.add(name)
    if name in {"jeevan hospital"}:
        row["review_flags"] = (
            row.get("review_flags", "") + ";CHECK_BRANCH"
        ).strip(";")
    review.append(row)

with output.open("w", encoding="utf-8-sig", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=review[0].keys())
    writer.writeheader()
    writer.writerows(review)

print("Saved review file:", output)
print("Rows preserved:", len(review))
print("Original file unchanged.")