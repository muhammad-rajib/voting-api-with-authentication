from fastapi.testclient import TestClient
from app.main import app
from app import schemas
from app.config import settings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


# database_url = 'postgresql://username:password@hostname:port/database-name'
database_url = (f"postgresql://"
                f"{settings.database_username}"
                f":{settings.database_password}"
                f"@{settings.database_hostname}"
                f":{settings.database_port}"
                f"/{settings.database_name}")


engine = create_engine(database_url)

testing_session_local = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def override_get_db():
    db = testing_session_local()
    try:
        yield db
    finally:
        db.close()


client = TestClient(app)


def test_root():
    res = client.get("/")
    assert res.json().get('message') == 'Hello FastAPI World ... !!!'

def test_create_user():
    res = client.post("/users/create", json={"email": "hello2@gmail.com", "password": "123"})
    new_user = schemas.CreateUserResponse(**res.json())
    assert new_user.email == "hello2@gmail.com"
    assert res.status_code == 201

