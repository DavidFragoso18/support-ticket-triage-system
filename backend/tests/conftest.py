"""
Pytest configuration and fixtures for all tests.
"""

import os
import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

# Add the backend directory to Python path so 'app' module can be imported
backend_dir = Path(__file__).parent.parent.resolve()
if str(backend_dir) not in sys.path:
    sys.path.insert(0, str(backend_dir))

# Also set PYTHONPATH environment variable
os.environ["PYTHONPATH"] = str(backend_dir) + os.pathsep + os.environ.get("PYTHONPATH", "")

# Imports must come after path manipulation above
import pytest  # noqa: E402
from fastapi.testclient import TestClient  # noqa: E402
from sqlmodel import Session, SQLModel, create_engine  # noqa: E402
from sqlmodel.pool import StaticPool  # noqa: E402

# CRITICAL: Patch the engine BEFORE importing app.db.base to prevent PostgreSQL connection
# Create a mock engine that will be replaced by our test engine
mock_engine = MagicMock()
with patch("app.db.base.engine", mock_engine):
    import app.db.base  # noqa: E402
    from app.db.base import get_session  # noqa: E402
    from app.main import app  # noqa: E402

# Import all models so SQLModel knows about them when creating tables
from app.db.models import (  # noqa: E402, F401
    AgentActivity,
    AIResponse,
    ClassificationFeedback,
    KBArticle,
    Resolution,
    SuggestionFeedback,
    Ticket,
    TicketClassification,
    TicketResolution,
)


@pytest.fixture(name="engine")
def engine_fixture():
    """Create a fresh in-memory SQLite database for each test"""
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(engine)
    return engine


@pytest.fixture(name="session")
def session_fixture(engine):
    """Create a new session for each test"""
    with Session(engine) as session:
        yield session


@pytest.fixture(name="client")
def client_fixture(session: Session, engine):
    """Create a test client with database session override"""

    def get_session_override():
        return session

    # Replace the app's database engine with our test engine
    import app.db.base as db_base_module

    db_base_module.engine = engine

    app.dependency_overrides[get_session] = get_session_override

    # Patch create_db_and_tables in app.main to prevent real DB connection
    with patch("app.main.create_db_and_tables"):
        # Use context manager to trigger startup/shutdown events
        with TestClient(app) as client:
            yield client

    app.dependency_overrides.clear()
