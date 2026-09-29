from fastapi import FastAPI, HTTPException, Query

app = FastAPI(
    title="Ankommen API",
    description="Local resource discovery and recommendation platform",
    version="0.1.0"
)

resources = [
    {
        "id": 1,
        "name": "Sample Healthcare Centre",
        "category": "healthcare",
        "journey": "settlement",
        "city": "Ghaziabad"
    },
    {
        "id": 2,
        "name": "Sample Housing Service",
        "category": "housing",
        "journey": "settlement",
        "city": "Ghaziabad"
    },
    {
        "id": 3,
        "name": "Sample Tourist Attraction",
        "category": "attractions",
        "journey": "tourism",
        "city": "Ghaziabad"
    },
    {
        "id": 4,
        "name": "Sample Restaurant",
        "category": "restaurants",
        "journey": "tourism",
        "city": "Ghaziabad"
    }
]


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
    category: str | None = Query(default=None)
):
    results = resources

    if journey:
        journey = journey.strip().lower()

        if journey not in ["settlement", "tourism"]:
            raise HTTPException(
                status_code=400,
                detail="Journey must be settlement or tourism"
            )

        results = [
            resource for resource in results
            if resource["journey"] == journey
        ]

    if category:
        category = category.strip().lower()
        results = [
            resource for resource in results
            if resource["category"] == category
        ]

    return {
        "count": len(results),
        "results": results
    }