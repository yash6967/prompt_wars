import os
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient

# Enforce database environment configuration for tests
os.environ["DATABASE_URL"] = "sqlite:///./data/test_saathi.db"

from backend.database import Base, get_db
from backend.main import app

# Create test database engine
engine = create_engine("sqlite:///./data/test_saathi.db", connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="session", autouse=True)
def setup_test_db():
    # Build schema
    Base.metadata.create_all(bind=engine)
    yield
    # Destroy schema post test session
    Base.metadata.drop_all(bind=engine)
    if os.path.exists("./data/test_saathi.db"):
        try:
            os.remove("./data/test_saathi.db")
        except PermissionError:
            pass

@pytest.fixture
def db_session():
    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)
    
    yield session
    
    session.close()
    transaction.rollback()
    connection.close()

@pytest.fixture
def client(db_session):
    def override_get_db():
        try:
            yield db_session
        finally:
            pass
            
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    app.dependency_overrides.clear()
