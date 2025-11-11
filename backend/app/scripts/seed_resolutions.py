import csv
from pathlib import Path
from sqlmodel import Session
from app.db.base import engine, create_db_and_tables
from app.db.models.resolutions import Resolution
from app.nlp.embeddings import emb
from uuid import UUID

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
            intent = (row.get("intent") or "general_inquiry").strip()
            title = (row.get("title") or row.get("summary") or "").strip()
            body = (row.get("body") or row.get("details") or "").strip()
            
            if not title or not body:
                print(f"[seed] Skipping row with missing title/body: {row}")
                continue
            
            # Generate embedding
            text_for_embedding = f"{intent} {title} {body}"
            embedding_list = emb.encode_to_list(text_for_embedding)
            
            session.add(Resolution(
                intent=intent,
                title=title,
                body=body,
                embedding=embedding_list
            ))
            count += 1
        session.commit()
    print(f"[seed] Resolutions seeded: {count}")

if __name__ == "__main__":
    main()