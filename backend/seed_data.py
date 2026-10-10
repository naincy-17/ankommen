from database import Base, SessionLocal, engine
from models import Resource

Base.metadata.create_all(bind=engine)


sample_resources = [
    {
        "name": "Sample Healthcare Centre",
        "category": "healthcare",
        "journey": "settlement",
        "city": "Ghaziabad",
        "description": "Demo listing for exploring healthcare options. Verify providers and availability before visiting.",
        "address": "Raj Nagar, Ghaziabad (demo area)",
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
        "description": "Demo listing for exploring housing options. Confirm current rent, terms, and availability directly.",
        "address": "Indirapuram, Ghaziabad (demo area)",
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
        "description": "Demo listing for a local outing. Check opening hours and visitor information before travelling.",
        "address": "City centre, Ghaziabad (demo area)",
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
        "description": "Demo listing for dining nearby. Confirm menu, hours, and location before visiting.",
        "address": "Vaishali, Ghaziabad (demo area)",
        "latitude": 28.6692,
        "longitude": 77.4538,
        "website": None,
        "min_budget": None,
        "max_budget": None,
    },
    {
        "name": "Sample Job Search Support",
        "category": "jobs",
        "journey": "settlement",
        "city": "Ghaziabad",
        "description": "Demo resource for finding job-search guidance and local employment services.",
        "address": "Kaushambi, Ghaziabad (demo area)",
        "latitude": 28.6457,
        "longitude": 77.3242,
        "website": None,
        "min_budget": None,
        "max_budget": None,
    },
    {
        "name": "Sample Learning Centre",
        "category": "education",
        "journey": "settlement",
        "city": "Ghaziabad",
        "description": "Demo resource for exploring local education and language-learning options.",
        "address": "Vasundhara, Ghaziabad (demo area)",
        "latitude": 28.6603,
        "longitude": 77.3673,
        "website": None,
        "min_budget": None,
        "max_budget": None,
    },
    {
        "name": "Sample Public Transport Guide",
        "category": "transport",
        "journey": "settlement",
        "city": "Ghaziabad",
        "description": "Demo resource for getting oriented with public transport around Ghaziabad.",
        "address": "Ghaziabad railway station area (demo area)",
        "latitude": 28.6619,
        "longitude": 77.4326,
        "website": None,
        "min_budget": None,
        "max_budget": None,
    },
    {
        "name": "Sample Government Services Guide",
        "category": "government",
        "journey": "settlement",
        "city": "Ghaziabad",
        "description": "Demo resource for discovering local government and civic services.",
        "address": "Ghaziabad (demo area)",
        "latitude": 28.6692,
        "longitude": 77.4538,
        "website": None,
        "min_budget": None,
        "max_budget": None,
    },
    {
        "name": "Sample Stay in Ghaziabad",
        "category": "accommodation",
        "journey": "tourism",
        "city": "Ghaziabad",
        "description": "Demo listing for exploring places to stay. Verify rates, amenities, and availability directly.",
        "address": "Indirapuram, Ghaziabad (demo area)",
        "latitude": 28.6415,
        "longitude": 77.3714,
        "website": None,
        "min_budget": None,
        "max_budget": None,
    },
    {
        "name": "Sample Local Market Walk",
        "category": "activities",
        "journey": "tourism",
        "city": "Ghaziabad",
        "description": "Demo idea for exploring local markets and neighbourhood food. Check current hours before visiting.",
        "address": "Raj Nagar, Ghaziabad (demo area)",
        "latitude": 28.6872,
        "longitude": 77.4406,
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
        raise RuntimeError("Failed to insert demo resources.") from error

    finally:
        db.close()


if __name__ == "__main__":
    seed_database()