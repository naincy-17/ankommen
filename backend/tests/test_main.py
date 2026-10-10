import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from database import Base, get_db
from main import app
from models import Resource
from seed_data import sample_resources


@pytest.fixture
def client():
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    TestingSessionLocal = sessionmaker(bind=engine, autoflush=False)
    Base.metadata.create_all(bind=engine)

    with TestingSessionLocal() as db:
        db.add_all(Resource(**resource) for resource in sample_resources)
        db.commit()

    def override_get_db():
        with TestingSessionLocal() as db:
            yield db

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()
    Base.metadata.drop_all(bind=engine)
    engine.dispose()


def test_home_endpoint(client):
    response = client.get("/")

    assert response.status_code == 200
    assert response.json()["city"] == "Ghaziabad"
    assert response.json()["status"] == "Backend is running"


def test_get_all_resources(client):
    response = client.get("/resources")

    assert response.status_code == 200
    assert response.json()["count"] == len(sample_resources)


def test_filter_settlement_resources(client):
    response = client.get("/resources?journey=settlement")

    assert response.status_code == 200
    assert response.json()["count"] == 6
    assert all(
        resource["journey"] == "settlement"
        for resource in response.json()["results"]
    )


def test_filter_tourism_restaurants(client):
    response = client.get(
        "/resources?journey=tourism&category=restaurants"
    )

    assert response.status_code == 200
    assert response.json()["count"] == 1
    assert response.json()["results"][0]["name"] == "Sample Restaurant"


def test_search_ranks_name_matches_first(client):
    response = client.get("/resources?q=housing")

    assert response.status_code == 200
    assert response.json()["count"] == 1
    assert response.json()["results"][0]["name"] == "Sample Housing Service"


def test_search_ranks_relevant_results_first(client):
    response = client.get("/resources?q=Ghaziabad")

    assert response.status_code == 200
    assert response.json()["count"] == len(sample_resources)
    assert response.json()["results"][0]["name"] == "Sample Stay in Ghaziabad"


def test_city_filter_is_case_insensitive(client):
    response = client.get("/resources?city=ghaziabad")

    assert response.status_code == 200
    assert response.json()["count"] == len(sample_resources)


def test_limit_is_validated(client):
    response = client.get("/resources?limit=0")

    assert response.status_code == 422


def test_invalid_journey(client):
    response = client.get("/resources?journey=invalid")

    assert response.status_code == 400
    assert response.json()["detail"] == (
        "Journey must be settlement or tourism"
    )
