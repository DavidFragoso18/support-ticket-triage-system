"""
Migration script to add status and assigned_agent_id columns to tickets table.
Run this script to update the database schema for Phase 5 WebSocket features.
"""

import sys

sys.path.insert(0, "/app")

from sqlalchemy import text

from app.db.base import engine


def migrate():
    """Add status and assigned_agent_id columns to tickets table"""

    with engine.connect() as conn:
        print("🔄 Adding status column...")
        try:
            conn.execute(
                text(
                    """
                ALTER TABLE tickets 
                ADD COLUMN IF NOT EXISTS status VARCHAR(50) DEFAULT 'open'
            """
                )
            )
            conn.execute(
                text(
                    """
                CREATE INDEX IF NOT EXISTS idx_tickets_status ON tickets(status)
            """
                )
            )
            print("✅ Status column added")
        except Exception as e:
            print(f"⚠️  Status column: {e}")

        print("🔄 Adding assigned_agent_id column...")
        try:
            conn.execute(
                text(
                    """
                ALTER TABLE tickets 
                ADD COLUMN IF NOT EXISTS assigned_agent_id VARCHAR(100)
            """
                )
            )
            conn.execute(
                text(
                    """
                CREATE INDEX IF NOT EXISTS idx_tickets_assigned_agent ON tickets(assigned_agent_id)
            """
                )
            )
            print("✅ Assigned_agent_id column added")
        except Exception as e:
            print(f"⚠️  Assigned_agent_id column: {e}")

        # Commit the changes
        conn.commit()
        print("✅ Migration completed successfully!")


if __name__ == "__main__":
    migrate()
