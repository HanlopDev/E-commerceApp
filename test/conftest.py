from fastapi.testclient import TestClient
import json
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import pytest
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import app
from database import Base, get_db
from config import setting
from models import User
from hashing import Hasher

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)


@pytest.fixture
def client():
    def override_get_db():
        try:
            db = TestSessionLocal()
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db
    client = TestClient(app)
    yield client


@pytest.fixture
def header_token(client: TestClient):
    test_email = setting.TEST_EMAIL
    test_pass = setting.TEST_PASS
    db = TestSessionLocal()
    user = db.query(User).filter(User.email == setting.TEST_EMAIL).first()
    if user is None:
        user = User(email=test_email, password=Hasher.get_hash_password(test_pass))
        db.add(user)
        db.commit()
        db.refresh(user)
    data = {"username": test_email, "password": test_pass}
    response = client.post("/login/token", data=data)
    access_token = response.json()["access_token"]
    return {"Authorization": f"Bearer {access_token}"}
