from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_home_route():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"status": "online"}

def test_invalid_parameter():
    response = client.get("/weather/?city_name=B")
    assert response.status_code == 422

def test_valid_city():
    response = client.get("/weather/?city_name=Boston")
    assert response.status_code == 200

    data = response.json()
    assert data["city_name"] == "Boston"
    assert isinstance(data["temperature"], float)
    assert isinstance(data["wind_speed"], (int, float))

def test_weather_history_crud_flow():
    response = client.post("/weather/history", json={"city_name": "Austin", "temperature": 90, "wind_speed": 9})
    assert response.status_code == 201
    data = response.json()
    assert isinstance(data["id"], int)
    assert data["created_at"]
    assert data["city_name"] == "Austin"
    assert data["temperature"] == 90
    assert data["wind_speed"] == 9

    history_id = data["id"]
    response = client.get(f"/weather/history/{history_id}")

    assert response.status_code == 200
    return_data = response.json()
    return_id = return_data["id"]
    assert history_id == return_id
    assert return_data["city_name"] == "Austin"

    response = client.patch(f"/weather/history/{history_id}", json={"temperature": 95})
    assert response.status_code == 200
    updated_data = response.json()
    assert updated_data["temperature"] == 95
    assert updated_data["city_name"] == "Austin"

    response = client.delete(f"/weather/history/{history_id}")
    assert response.status_code == 200
    assert response.json()["message"] == "Item deleted successfully"

    response = client.get(f"/weather/history/{history_id}")
    assert response.status_code == 404





