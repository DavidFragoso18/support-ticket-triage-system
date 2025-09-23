import csv
from pathlib import Path
from sqlmodel import Session
from app.db.base import engine, create_db_and_tables
from app.db.models.ticket import Ticket
from uuid import UUID

CSV_PATH = Path(__file__).resolve().parents[3] / "data" / "seeds" / "tickets_seed.csv"

def parse_uuid_or_none(x: str | None):
    x = (x or "").strip()
    if not x:
        return None
    try:
        return UUID(x)
    except ValueError:
        return None  # ignore bad values

def main():
    print(f"[seed] CSV: {CSV_PATH} (exists={CSV_PATH.exists()})")
    create_db_and_tables()

    with Session(engine) as session, open(CSV_PATH, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        count = 0
        for row in reader:
            id = parse_uuid_or_none(row.get("id"))
            subject = (row.get("subject") or "").strip()
            body = (row.get("body") or "").strip()
            channel = (row.get("channel") or "").strip()
            customer_id = (row.get("customer_id") or "").strip()
            language = (row.get("language") or "").strip()
            
            if not subject or not body:
                print(f"[seed] Skipping row with missing subject/body: {row}")
                continue
                
            session.add(Ticket(
                id=id,
                subject=subject,
                body=body,
                channel=channel,
                customer_id=customer_id,
                language=language
            ))
            count += 1
        session.commit()
    print(f"[seed] Tickets seeded: {count}")

if __name__ == "__main__":
    main()