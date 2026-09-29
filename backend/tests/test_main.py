
from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_home_endpoint():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json()["city"] == "Ghaziabad"
    assert response.json()["status"] == "Backend is running"


def test_get_all_resources():
    response = client.get("/resources")

    assert response.status_code == 200
    assert response.json()["count"] == 4


def test_filter_settlement_resources():
    response = client.get("/resources?journey=settlement")

    assert response.status_code == 200
    assert response.json()["count"] == 2

    for resource in response.json()["results"]:
        assert resource["journey"] == "settlement"


def test_filter_tourism_restaurants():
    response = client.get(
        "/resources?journey=tourism&category=restaurants"
    )

    assert response.status_code == 200
    assert response.json()["count"] == 1
    assert response.json()["results"][0]["name"] == "Sample Restaurant"


def test_invalid_journey():
    response = client.get("/resources?journey=invalid")

    assert response.status_code == 400
    assert response.json()["detail"] == (
        "Journey must be settlement or tourism"
    )