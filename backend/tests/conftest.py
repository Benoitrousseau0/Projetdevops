import os
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from core.database import Base, get_db
from core.main import app

TEST_DB_PATH = "./test.db"
TEST_DATABASE_URL = f"sqlite:///{TEST_DB_PATH}"
engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="function")
def client():
    # Crée les tables
    Base.metadata.create_all(bind=engine)

    def override_get_db():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db
    client = TestClient(app)

    yield client

    # Drop les tables
    Base.metadata.drop_all(bind=engine)

    # Ferme toutes les connexions à la BDD
    engine.dispose()

    # Supprime le fichier test.db
    if os.path.exists(TEST_DB_PATH):
        os.remove(TEST_DB_PATH)

    app.dependency_overrides.clear()
