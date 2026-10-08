from fastapi import Depends, FastAPI, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.orm import Session

from database import get_db
from models import Resource


app = FastAPI(
    title="Ankommen API",
    description="Local resource discovery and recommendation platform",
    version="0.1.0"
)


@app.get("/")
def home():
    return {
        "message": "Welcome to Ankommen!",
        "city": "Ghaziabad",
        "journeys": ["Settlement", "Tourism"],
        "status": "Backend is running"
    }


@app.get("/resources")
def get_resources(
    journey: str | None = Query(default=None),
    category: str | None = Query(default=None),
    db: Session = Depends(get_db)
):
    query = select(Resource)

    if journey:
        journey = journey.strip().lower()

        if journey not in ["settlement", "tourism"]:
            raise HTTPException(
                status_code=400,
                detail="Journey must be settlement or tourism"
            )

        query = query.where(Resource.journey == journey)

    if category:
        category = category.strip().lower()
        query = query.where(Resource.category == category)

    resources = db.execute(query).scalars().all()

    results = [
        {
            "id": resource.id,
            "name": resource.name,
            "category": resource.category,
            "journey": resource.journey,
            "city": resource.city,
            "description": resource.description,
            "address": resource.address,
            "latitude": resource.latitude,
            "longitude": resource.longitude,
            "website": resource.website,
            "min_budget": resource.min_budget,
            "max_budget": resource.max_budget,
        }
        for resource in resources
    ]

    return {
        "count": len(results),
        "results": results
    }