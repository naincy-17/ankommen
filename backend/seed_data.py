from database import SessionLocal
from models import Resource


sample_resources = [
    {
        "name": "Sample Healthcare Centre",
        "category": "healthcare",
        "journey": "settlement",
        "city": "Ghaziabad",
        "description": "Illustrative healthcare resource for Ankommen development and testing.",
        "address": "Sample Address, Ghaziabad",
        "latitude": 28.6692,
        "longitude": 77.4538,
        "website": None,
        "min_budget": None,
        "max_budget": None,
    },
    {
        "name": "Sample Housing Service",
        "category": "housing",
        "journey": "settlement",
        "city": "Ghaziabad",
        "description": "Illustrative housing resource for Ankommen development and testing.",
        "address": "Sample Address, Ghaziabad",
        "latitude": 28.6692,
        "longitude": 77.4538,
        "website": None,
        "min_budget": None,
        "max_budget": None,
    },
    {
        "name": "Sample Tourist Attraction",
        "category": "attractions",
        "journey": "tourism",
        "city": "Ghaziabad",
        "description": "Illustrative tourist attraction for Ankommen development and testing.",
        "address": "Sample Address, Ghaziabad",
        "latitude": 28.6692,
        "longitude": 77.4538,
        "website": None,
        "min_budget": None,
        "max_budget": None,
    },
    {
        "name": "Sample Restaurant",
        "category": "restaurants",
        "journey": "tourism",
        "city": "Ghaziabad",
        "description": "Illustrative restaurant resource for Ankommen development and testing.",
        "address": "Sample Address, Ghaziabad",
        "latitude": 28.6692,
        "longitude": 77.4538,
        "website": None,
        "min_budget": None,
        "max_budget": None,
    },
]


def seed_database():
    db = SessionLocal()

    try:
        for data in sample_resources:
            existing_resource = (
                db.query(Resource)
                .filter(Resource.name == data["name"])
                .first()
            )

            if existing_resource:
                print(f"Already exists: {data['name']}")
                continue

            resource = Resource(**data)
            db.add(resource)

        db.commit()
        print("Sample data inserted successfully!")

    except Exception as error:
        db.rollback()
        print("Failed to insert sample data.")
        print(error)

    finally:
        db.close()


if __name__ == "__main__":
    seed_database()