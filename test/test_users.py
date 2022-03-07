from fastapi.testclient import TestClient
from app.main import app
from app import schemas 

client = TestClient(app)


def test_root():
    res = client.get("/")
    assert res.json().get('message') == 'Hello FastAPI World ... !!!'

def test_create_user():
    res = client.post("/users/create", json={"email": "hello2@gmail.com", "password": "123"})
    new_user = schemas.CreateUserResponse(**res.json())
    assert new_user.email == "hello2@gmail.com"
    assert res.status_code == 201