"""
Migration script to create analytics tables for Phase 5.
Run with: python -m app.scripts.migrate_analytics
"""
from sqlalchemy import text

from app.db.base import engine


def migrate():
    """Create analytics tables"""
    
    with engine.begin() as conn:
        # Create agent_activities table
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS agent_activities (
                id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                agent_id VARCHAR(100) NOT NULL,
                ticket_id UUID NOT NULL REFERENCES tickets(id) ON DELETE CASCADE,
                action VARCHAR(50) NOT NULL,
                timestamp TIMESTAMP NOT NULL DEFAULT NOW(),
                duration_seconds INTEGER,
                extra_data TEXT
            );
        """))
        
        # Create indexes for agent_activities
        conn.execute(text("""
            CREATE INDEX IF NOT EXISTS agent_activities_agent_id_idx ON agent_activities(agent_id);
        """))
        conn.execute(text("""
            CREATE INDEX IF NOT EXISTS agent_activities_ticket_id_idx ON agent_activities(ticket_id);
        """))
        conn.execute(text("""
            CREATE INDEX IF NOT EXISTS agent_activities_action_idx ON agent_activities(action);
        """))
        conn.execute(text("""
            CREATE INDEX IF NOT EXISTS agent_activities_timestamp_idx ON agent_activities(timestamp);
        """))
        
        # Create suggestion_feedback table
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS suggestion_feedback (
                id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                ticket_id UUID NOT NULL REFERENCES tickets(id) ON DELETE CASCADE,
                suggestion_type VARCHAR(50) NOT NULL,
                suggestion_id UUID,
                agent_id VARCHAR(100) NOT NULL,
                rating INTEGER NOT NULL CHECK (rating >= 1 AND rating <= 5),
                was_used BOOLEAN NOT NULL DEFAULT FALSE,
                feedback_text TEXT,
                timestamp TIMESTAMP NOT NULL DEFAULT NOW()
            );
        """))
        
        # Create indexes for suggestion_feedback
        conn.execute(text("""
            CREATE INDEX IF NOT EXISTS suggestion_feedback_ticket_id_idx ON suggestion_feedback(ticket_id);
        """))
        conn.execute(text("""
            CREATE INDEX IF NOT EXISTS suggestion_feedback_type_idx ON suggestion_feedback(suggestion_type);
        """))
        conn.execute(text("""
            CREATE INDEX IF NOT EXISTS suggestion_feedback_agent_id_idx ON suggestion_feedback(agent_id);
        """))
        conn.execute(text("""
            CREATE INDEX IF NOT EXISTS suggestion_feedback_timestamp_idx ON suggestion_feedback(timestamp);
        """))
        
        print("✅ Analytics tables created successfully!")


if __name__ == "__main__":
    migrate()
