import csv
from pathlib import Path
from sqlmodel import Session
from app.db.base import engine, create_db_and_tables
from app.db.models.resolutions import Resolution
from uuid import UUID;

CSV_PATH = Path(__file__).resolve().parents[3] / "data" / "seeds" / "resolutions.csv"

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
            ticket_id = parse_uuid_or_none(row.get("ticket_id"))
            summary = (row.get("summary") or "").strip()
            details = (row.get("details") or "").strip()
            if not summary or not details:
                print(f"[seed] Skipping row with missing summary/details: {row}")
                continue
            session.add(Resolution(ticket_id=ticket_id, summary=summary, details=details))
            count += 1
        session.commit()
    print(f"[seed] Resolutions seeded: {count}")

if __name__ == "__main__":
    main()