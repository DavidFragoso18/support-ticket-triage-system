from sqlmodel import SQLModel, create_engine, Session
from app.core.config import settings

def _import_models():
    # Import to register tables in SQLModel.metadata
    import app.db.models.ticket    # noqa: F401
    import app.db.models.kb        # noqa: F401
    import app.db.models.resolutions

engine = create_engine(
    settings.database_url,
    echo=False,
    connect_args={"connect_timeout": 5},  # optional, helps fail fast
)

def create_db_and_tables() -> None:
    _import_models()
    SQLModel.metadata.create_all(engine)
    

def get_session():
    with Session(engine) as session:
        yield session
