"""
Pytest configuration and fixtures for all tests.
"""
import os
import sys
from pathlib import Path

# Add the backend directory to Python path so 'app' module can be imported
backend_dir = Path(__file__).parent.parent.resolve()
if str(backend_dir) not in sys.path:
    sys.path.insert(0, str(backend_dir))

# Also set PYTHONPATH environment variable
os.environ['PYTHONPATH'] = str(backend_dir) + os.pathsep + os.environ.get('PYTHONPATH', '')

# Imports must come after path manipulation above
import pytest  # noqa: E402
from fastapi.testclient import TestClient  # noqa: E402
from sqlmodel import Session, SQLModel, create_engine  # noqa: E402
from sqlmodel.pool import StaticPool  # noqa: E402

from app.db.base import get_session  # noqa: E402
from app.main import app  # noqa: E402


@pytest.fixture(name="session")
def session_fixture():
    """Create a fresh in-memory SQLite database for each test"""
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session


@pytest.fixture(name="client")
def client_fixture(session: Session):
    """Create a test client with database session override"""
    def get_session_override():
        return session

    app.dependency_overrides[get_session] = get_session_override
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()
