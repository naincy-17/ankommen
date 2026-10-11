
import csv
from pathlib import Path
from collections import Counter, defaultdict
from math import radians, sin, cos, asin, sqrt

from sqlalchemy import select
from database import SessionLocal
from models import Resource

CSV_PATH = Path("data/ghaziabad_healthcare_import_candidate.csv")
REPORT_PATH = Path("data/ghaziabad_healthcare_review_report.csv")


def distance_m(lat1, lon1, lat2, lon2):
    """Approximate distance between two coordinates, in metres."""
    lat1, lon1, lat2, lon2 = map(
        radians, (lat1, lon1, lat2, lon2)
    )
    dlat, dlon = lat2 - lat1, lon2 - lon1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    return 6371000 * 2 * asin(sqrt(a))


def main():
    with CSV_PATH.open(encoding="utf-8-sig", newline="") as file:
        rows = list(csv.DictReader(file))

    db = SessionLocal()
    try:
        existing = db.execute(
            select(Resource).where(Resource.city.ilike("Ghaziabad"))
        ).scalars().all()

        existing_names = {
            r.name.strip().casefold() for r in existing
        }

        candidate_name_groups = defaultdict(list)
        for r in rows:
            candidate_name_groups[r["name"].strip().casefold()].append(r)

        duplicate_names = {
            name for name, group in candidate_name_groups.items()
            if name and len(group) > 1
        }

        output = []
        for r in rows:
            name = r["name"].strip()
            lat, lon = float(r["latitude"]), float(r["longitude"])
            flags = []

            if name.casefold() in existing_names:
                flags.append("MATCHES_EXISTING_NAME")

            if name.casefold() in duplicate_names:
                flags.append("DUPLICATE_CANDIDATE_NAME")

            if not r.get("address", "").strip():
                flags.append("NO_ADDRESS")

            if not r.get("website", "").strip():
                flags.append("NO_WEBSITE")

            if not r.get("phone", "").strip():
                flags.append("NO_PHONE")

            if any(word in name.casefold() for word in
                   ("homeopathic medicines", "homopathic medicines")):
                flags.append("CHECK_PLACE_TYPE")

            nearby = []
            for old in existing:
                if old.latitude is None or old.longitude is None:
                    continue
                metres = distance_m(
                    lat, lon, old.latitude, old.longitude
                )
                if metres <= 150:
                    nearby.append((old.name, round(metres)))

            if nearby:
                flags.append("NEAR_EXISTING_RESOURCE")

            output.append({
                **r,
                "review_flags": ";".join(flags) if flags else "NONE",
                "nearby_existing_resources": "; ".join(
                    f"{n} ({d} m)" for n, d in nearby
                ),
            })

        columns = list(output[0].keys()) if output else []
        with REPORT_PATH.open(
            "w", encoding="utf-8-sig", newline=""
        ) as file:
            writer = csv.DictWriter(file, fieldnames=columns)
            writer.writeheader()
            writer.writerows(output)

        counts = Counter(
            flag
            for r in output
            for flag in r["review_flags"].split(";")
            if flag != "NONE"
        )

        print("REVIEW ONLY — database unchanged")
        print("Candidates reviewed:", len(rows))
        print("Existing Ghaziabad resources:", len(existing))
        print("Duplicate candidate-name groups:", len(duplicate_names))
        print("Records with review flags:", sum(
            r["review_flags"] != "NONE" for r in output
        ))
        print("\nReview flags:")
        for flag, count in counts.most_common():
            print(f"{flag}: {count}")
        print("\nReport saved to:", REPORT_PATH)

    finally:
        db.close()


if __name__ == "__main__":
    main()