"""
Migration script to add full-text search indexes for Phase 5 semantic search.
Run with: python -m app.scripts.migrate_search_indexes
"""
from sqlalchemy import text
from app.db.base import engine


def migrate():
    """Create full-text search indexes"""
    
    with engine.begin() as conn:
        # Add tsvector column for full-text search on tickets
        print("📝 Adding tsvector column...")
        conn.execute(text("""
            ALTER TABLE tickets 
            ADD COLUMN IF NOT EXISTS search_vector tsvector
            GENERATED ALWAYS AS (
                setweight(to_tsvector('english', coalesce(subject, '')), 'A') ||
                setweight(to_tsvector('english', coalesce(body, '')), 'B')
            ) STORED;
        """))
        
        # Create GIN index on tsvector for fast full-text search
        print("🔍 Creating GIN index for full-text search...")
        conn.execute(text("""
            CREATE INDEX IF NOT EXISTS tickets_search_vector_idx 
            ON tickets USING GIN (search_vector);
        """))
        
        # Create index on embedding for vector similarity search (if not exists)
        print("📊 Creating index on embedding vector...")
        conn.execute(text("""
            CREATE INDEX IF NOT EXISTS tickets_embedding_idx 
            ON tickets USING ivfflat (embedding vector_cosine_ops)
            WITH (lists = 100);
        """))
        
        print("✅ Search indexes created successfully!")


if __name__ == "__main__":
    migrate()
