import pytest
from app import app


@pytest.fixture
def client():
    app.config.update(
        TESTING=True,
        SECRET_KEY="test-only-secret-key"
    )

    with app.test_client() as client:
        yield client


def login(client, username, password):
    return client.post(
        "/api/login",
        json={
            "username": username,
            "password": password
        }
    )


def test_alice_can_access_own_invoice(client):
    login_response = login(
        client, "alice", "alice-demo-password"
    )

    assert login_response.status_code == 200

    response = client.get("/api/invoices/101")

    assert response.status_code == 200
    assert response.json["owner_id"] == 1


def test_alice_cannot_access_bobs_invoice(client):
    login(client, "alice", "alice-demo-password")

    response = client.get("/api/invoices/102")

    assert response.status_code == 403
    assert response.json["error"] == "Access denied"


def test_bob_can_access_own_invoice(client):
    login(client, "bob", "bob-demo-password")

    response = client.get("/api/invoices/102")

    assert response.status_code == 200
    assert response.json["owner_id"] == 2


def test_unauthenticated_user_is_rejected(client):
    response = client.get("/api/invoices/101")

    assert response.status_code == 401


def test_nonexistent_invoice_returns_404(client):
    login(client, "alice", "alice-demo-password")

    response = client.get("/api/invoices/999")

    assert response.status_code == 404


def test_invalid_login_is_rejected(client):
    response = login(
        client, "alice", "wrong-password"
    )

    assert response.status_code == 401