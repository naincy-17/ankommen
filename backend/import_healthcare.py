
import csv
import sys
from pathlib import Path

from sqlalchemy import select
from database import SessionLocal
from models import Resource

CSV_PATH = Path("data/ghaziabad_healthcare_import_ready.csv")

BLOCKED_FLAGS = {
    "CHECK_DISTRICT_LOCATION",
    "DUPLICATE_CANDIDATE_NAME",
    "POSSIBLE_DUPLICATE",
    "NEAR_EXISTING_RESOURCE",
    "CHECK_PLACE_TYPE",
    "CHECK_BRANCH",
}


def main():
    apply_changes = "--apply" in sys.argv

    with CSV_PATH.open(encoding="utf-8-sig", newline="") as f:
        candidates = list(csv.DictReader(f))

    db = SessionLocal()
    try:
        existing = db.execute(
            select(Resource).where(Resource.city.ilike("Ghaziabad"))
        ).scalars().all()

        seen_names = {r.name.strip().casefold() for r in existing}
        additions = []
        reasons = {
            "duplicate_name": 0,
            "invalid_coordinates": 0,
            "outside_sanity_bounds": 0,
            "blocked_review_flags": 0,
        }

        for row in candidates:
            name = row["name"].strip()
            key = name.casefold()

            if not name or key in seen_names:
                reasons["duplicate_name"] += 1
                continue

            try:
                lat = float(row["latitude"])
                lon = float(row["longitude"])
            except (ValueError, TypeError):
                reasons["invalid_coordinates"] += 1
                continue

            if not (28.3 <= lat <= 29.0 and 77.1 <= lon <= 77.7):
                reasons["outside_sanity_bounds"] += 1
                continue

            flags = {
                flag.strip()
                for flag in row.get("review_flags", "").split(";")
                if flag.strip() and flag.strip() != "NONE"
            }

            if flags & BLOCKED_FLAGS:
                reasons["blocked_review_flags"] += 1
                continue

            additions.append(Resource(
                name=name,
                category="healthcare",
                journey="settlement",
                city="Ghaziabad",
                description=(
                    "Healthcare listing sourced from OpenStreetMap. "
                    "Provider details and operating status are unverified; "
                    "confirm before visiting. "
                    "© OpenStreetMap contributors."
                ),
                address=row.get("address", "").strip() or None,
                latitude=lat,
                longitude=lon,
                website=row.get("website", "").strip() or None,
                min_budget=None,
                max_budget=None,
            ))
            seen_names.add(key)

        print("Mode:", "APPLY" if apply_changes else "PREVIEW ONLY")
        print("Existing resources:", len(existing))
        print("Candidate rows:", len(candidates))
        print("Potential additions:", len(additions))
        print("Skip reasons:", reasons)

        if not apply_changes:
            print("Database unchanged.")
            return

        try:
            db.add_all(additions)
            db.commit()
            print("Inserted:", len(additions))
        except Exception:
            db.rollback()
            raise

    finally:
        db.close()


if __name__ == "__main__":
    main()