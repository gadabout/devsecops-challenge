import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture(scope="module")
def client():
    return TestClient(app)


@pytest.fixture(scope="module")
def token(client):
    response = client.post(
        "/auth/login",
        json={"email": "dana@cascadekayak.example", "password": "kayak123"},
    )
    assert response.status_code == 200
    return response.json()["access_token"]


def test_healthz(client):
    response = client.get("/healthz")

    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_login_rejects_bad_password(client):
    response = client.post(
        "/auth/login",
        json={"email": "dana@cascadekayak.example", "password": "wrong"},
    )

    assert response.status_code == 401


def test_activity_search(client):
    response = client.get("/activities", params={"search": "kayak"})

    assert response.status_code == 200
    assert "Sunrise Kayak Paddle" in [a["title"] for a in response.json()]


def test_list_bookings_returns_own_operator_only(client, token):
    response = client.get("/bookings", headers={"Authorization": f"Bearer {token}"})

    assert response.status_code == 200
    assert {b["operator_id"] for b in response.json()} == {1}


def test_create_booking(client):
    response = client.post(
        "/bookings",
        json={
            "activity_id": 1,
            "customer_name": "Jess Carter",
            "customer_email": "jess.carter@example.com",
            "customer_phone": "+1-503-555-0188",
            "party_size": 2,
        },
    )

    assert response.status_code == 201
    assert response.json()["status"] == "confirmed"
    assert response.json()["amount_cents"] == 13000


def test_create_booking_rejects_unknown_activity(client):
    response = client.post(
        "/bookings",
        json={
            "activity_id": 9999,
            "customer_name": "Jess Carter",
            "customer_email": "jess.carter@example.com",
            "party_size": 1,
        },
    )

    assert response.status_code == 404
