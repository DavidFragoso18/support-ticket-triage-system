"""
Update existing ticket dates to be recent (for demo/testing purposes)
This spreads tickets across the last 7 days so analytics charts show data
"""
import random
from datetime import datetime, timedelta

from sqlmodel import Session, select

from app.db.base import create_db_and_tables, engine
from app.db.models.ticket import Ticket


def main():
    create_db_and_tables()
    
    with Session(engine) as session:
        # Get all tickets
        tickets = session.exec(select(Ticket)).all()
        
        if not tickets:
            print("[update] No tickets found")
            return
        
        # Spread tickets across last 7 days
        now = datetime.utcnow()
        days_back = 7
        
        print(f"[update] Updating {len(tickets)} tickets to have dates in last {days_back} days")
        
        for i, ticket in enumerate(tickets):
            # Distribute tickets across the time range
            # More recent = more tickets (weighted distribution)
            day_offset = random.choices(
                range(days_back),
                weights=[1, 2, 3, 4, 5, 6, 7],  # More recent days get more tickets
                k=1
            )[0]
            
            # Random time within that day
            hours_offset = random.randint(0, 23)
            minutes_offset = random.randint(0, 59)
            
            new_date = now - timedelta(
                days=day_offset,
                hours=hours_offset,
                minutes=minutes_offset
            )
            
            ticket.created_at = new_date
            ticket.updated_at = new_date
            session.add(ticket)
        
        session.commit()
        print(f"[update] ✅ Updated {len(tickets)} tickets with recent dates")
        print(f"[update] Date range: {now - timedelta(days=days_back)} to {now}")

if __name__ == "__main__":
    main()
