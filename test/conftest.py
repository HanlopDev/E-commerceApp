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
 
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread":False})
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

