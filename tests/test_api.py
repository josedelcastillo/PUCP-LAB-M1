import pytest
from fastapi.testclient import TestClient

from app import inventory
from app.main import app

client = TestClient(app)


@pytest.fixture(autouse=True)
def reset_inventory():
    inventory.reset()
    yield
    inventory.reset()


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_list_items():
    response = client.get("/items")
    assert response.status_code == 200
    items = response.json()
    assert len(items) == 3
    assert {"id", "name", "qty"} <= items[0].keys()


def test_withdraw_valid():
    response = client.post("/items/2/withdraw", json={"qty": 3})
    assert response.status_code == 200
    assert response.json()["qty"] == 5


def test_withdraw_exact_stock():
    response = client.post("/items/1/withdraw", json={"qty": 5})
    assert response.status_code == 200
    assert response.json()["qty"] == 0


def test_withdraw_exceeds_stock():
    response = client.post("/items/1/withdraw", json={"qty": 6})
    assert response.status_code == 400


def test_withdraw_unknown_item():
    response = client.post("/items/999/withdraw", json={"qty": 1})
    assert response.status_code == 404


def test_version_with_env(monkeypatch):
    monkeypatch.setenv("APP_VERSION", "1.2.3")
    monkeypatch.setenv("APP_ENV", "staging")
    response = client.get("/version")
    assert response.status_code == 200
    assert response.json() == {"version": "1.2.3", "env": "staging"}


def test_version_without_env(monkeypatch):
    monkeypatch.delenv("APP_VERSION", raising=False)
    monkeypatch.delenv("APP_ENV", raising=False)
    response = client.get("/version")
    assert response.status_code == 200
    assert response.json() == {"version": "dev", "env": "local"}
