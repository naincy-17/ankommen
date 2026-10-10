import os

from fastapi import Depends, FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import or_, select
from sqlalchemy.orm import Session

from database import get_db
from models import Resource


app = FastAPI(
    title="Ankommen API",
    description="Local resource discovery and recommendation platform",
    version="0.1.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        origin.strip()
        for origin in os.getenv(
            "CORS_ORIGINS",
            "http://localhost:5173,http://127.0.0.1:5173"
        ).split(",")
        if origin.strip()
    ],
    allow_methods=["GET"],
    allow_headers=["*"],
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
    city: str = Query(default="Ghaziabad", min_length=1, max_length=100),
    q: str | None = Query(default=None, max_length=200),
    limit: int = Query(default=50, ge=1, le=100),
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

    query = query.where(Resource.city.ilike(city.strip()))

    if category:
        category = category.strip().lower()
        query = query.where(Resource.category.ilike(category))

    search_terms = (q or "").strip().lower().split()
    if search_terms:
        search_fields = (
            Resource.name,
            Resource.category,
            Resource.description,
            Resource.address,
        )
        query = query.where(
            *(
                or_(*(field.ilike(f"%{term}%") for field in search_fields))
                for term in search_terms
            )
        )

    resources = db.execute(query).scalars().all()

    if search_terms:
        def relevance(resource: Resource) -> int:
            searchable = {
                "name": resource.name.lower(),
                "category": resource.category.lower(),
                "description": (resource.description or "").lower(),
                "address": (resource.address or "").lower(),
            }
            score = 0
            for term in search_terms:
                score += sum(
                    weight
                    for field, weight in (
                        ("name", 4),
                        ("category", 3),
                        ("description", 2),
                        ("address", 1),
                    )
                    if term in searchable[field]
                )
            return score

        resources.sort(key=lambda resource: (-relevance(resource), resource.id))
    else:
        resources.sort(key=lambda resource: resource.id)

    resources = resources[:limit]
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