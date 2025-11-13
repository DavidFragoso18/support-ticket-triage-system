"""
Migration script to create ai_responses table.
"""
import os
import sys

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from sqlmodel import create_engine, text

from app.core.config import settings


def migrate():
    """Create ai_responses table"""
    engine = create_engine(str(settings.database_url))
    
    with engine.begin() as conn:
        # Create ai_responses table
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS ai_responses (
                id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                ticket_id UUID NOT NULL REFERENCES tickets(id) ON DELETE CASCADE,
                response_text TEXT NOT NULL,
                tone VARCHAR(50) NOT NULL,
                context_used INTEGER DEFAULT 0,
                model VARCHAR(100) NOT NULL,
                agent_id VARCHAR(100),
                was_edited BOOLEAN DEFAULT FALSE,
                was_sent BOOLEAN DEFAULT FALSE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """))
        
        # Create indexes
        conn.execute(text("""
            CREATE INDEX IF NOT EXISTS idx_ai_responses_ticket_id 
            ON ai_responses(ticket_id);
        """))
        
        conn.execute(text("""
            CREATE INDEX IF NOT EXISTS idx_ai_responses_agent_id 
            ON ai_responses(agent_id);
        """))
        
        conn.execute(text("""
            CREATE INDEX IF NOT EXISTS idx_ai_responses_created_at 
            ON ai_responses(created_at DESC);
        """))
        
        print("✅ ai_responses table created successfully")

if __name__ == "__main__":
    migrate()
