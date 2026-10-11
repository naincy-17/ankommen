
import csv
from pathlib import Path

from sqlalchemy import select
from database import SessionLocal
from models import Resource

CSV_PATH = Path("data/ghaziabad_healthcare_final_candidate.csv")


def main():
    with CSV_PATH.open(encoding="utf-8-sig", newline="") as file:
        candidates = list(csv.DictReader(file))

    db = SessionLocal()
    try:
        existing = db.execute(
            select(Resource).where(Resource.city.ilike("Ghaziabad"))
        ).scalars().all()

        existing_names = {
            r.name.strip().casefold() for r in existing
        }

        ready = []
        skipped_existing = []
        held_for_location_review = []

        for row in candidates:
            if "CHECK_DISTRICT_LOCATION" in row["review_flags"]:
                held_for_location_review.append(row["name"])
            elif row["name"].strip().casefold() in existing_names:
                skipped_existing.append(row["name"])
            else:
                ready.append(row["name"])

        print("PREVIEW ONLY — no database changes made")
        print("Current resources:", len(existing))
        print("Candidate records:", len(candidates))
        print("Ready for import:", len(ready))
        print("Skipped due to existing name:", len(skipped_existing))
        print("Held for location review:", len(held_for_location_review))

        print("\nFirst 10 proposed additions:")
        for name in ready[:10]:
            print("-", name)

        print("\nHeld for location review:")
        for name in held_for_location_review:
            print("-", name)

    finally:
        db.close()


if __name__ == "__main__":
    main()