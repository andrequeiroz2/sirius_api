import os
from dotenv import find_dotenv, load_dotenv
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.db import Base, get_db
from main import app

load_dotenv(find_dotenv(filename=".env", raise_error_if_not_found=True))

username_test: str = os.getenv("USER_DB_TEST")
password_test: str = os.getenv("PASSWORD_DB_TEST")
host_test: str = os.getenv("DATABASE_HOST_TEST")
port_test: int = int(os.getenv("DATABASE_PORT_TEST"))
database_name_test: str = os.getenv("DATABASE_NAME_TEST")
SQLALCHEMY_DATABASE_URI_TEST = f"postgresql+psycopg2://{username_test}:{password_test}@{host_test}:{port_test}/{database_name_test}"

engine = create_engine(SQLALCHEMY_DATABASE_URI_TEST)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()
        

app.dependency_overrides[get_db] = override_get_db


client = TestClient(app)


def test_create_user():
    #testing post method
    response_post_200 = client.post(
        "/users/",
        json={"name": "Sirius", "email": "sirius@sirius.com", "password": "siriususerapi"}
    )
    assert response_post_200.status_code == 200, response_post_200.text
    data = response_post_200.json()
    assert data["name"] == "Sirius"
    assert data["email"] == "sirius@sirius.com"
    assert "id" in data
    user_id = data["id"]

    #testing get method
    response_get_200 = client.get(
        f"/users/{user_id}"
    )
    assert response_get_200.status_code == 200, response_get_200.text
    data_get_id = response_get_200.json()
    assert data_get_id["name"] == "Sirius"
    assert data_get_id["email"] == "sirius@sirius.com"

    #testing_get_all
    response_get_all_200 = client.get(
        "/users/",
    )
    assert response_get_all_200.status_code == 200, response_get_all_200.text
    data_get_all = response_get_200.json()
    assert data_get_all["name"] == "Sirius"
    assert data_get_all["email"] == "sirius@sirius.com"

    #testing_delete
    response_delete_200 = client.delete(
        "/users/",
        json={"email": "sirius@sirius.com", "password": "siriususerapi"}
    )
    assert response_delete_200.status_code == 200, response_delete_200.text

