from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_login_authenticated():
    response = client.post(
        "/api/auth/login",
        data={"username": "mehmet", "password": "mehmet"},
    )
    assert response.status_code == 200
    assert "token" in response.json()


def test_login_unauthenticated():
    response = client.post(
        "/api/auth/login",
        data={"username": "nonexistinguser", "password": "testpassword"},
    )
    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid credentials"


def test_read_user_me():
    # Assuming you have authentication implemented to get a valid token
    token = "valid_access_token"
    headers = {"Authorization": f"Bearer {token}"}
    response = client.get("/api/auth/me", headers=headers)
    assert response.status_code == 200
    assert "username" in response.json()


def test_signup():
    new_user_data = {
        "firstName": "Ahmet",
        "lastName": "Güçlü",
        "username": "ahmed",
        "password": "ahmed",
    }
    response = client.post("/api/auth/signup", json=new_user_data)
    assert response.status_code == 200
    assert "id" in response.json()
    assert response.json()["username"] == "ahmed"
