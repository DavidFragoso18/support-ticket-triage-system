# backend/app/scripts/enable_pgvector.py
from sqlalchemy import text

from app.db.base import engine


def main():
    with engine.connect() as conn:
        conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector"))
        conn.commit()
        print("✅ pgvector extension enabled")

if __name__ == "__main__":
    main()