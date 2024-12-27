from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"msg": "Hello World"}

# Pulse Checks

def test_get_teams():
    response = client.get("/teams")
    assert response.status_code == 200

def test_get_points_per_positon():
    response = client.get("/points_per_position/1")
    assert response.status_code == 200

def test_get_points_on_bench():
    response = client.get("/points_on_bench")
    assert response.status_code == 200

def test_get_win_percentages():
    response = client.get("/win_percentages")
    assert response.status_code == 200