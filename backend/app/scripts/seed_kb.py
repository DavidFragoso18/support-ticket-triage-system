import csv
from pathlib import Path
from sqlmodel import Session
from app.db.base import engine, create_db_and_tables
from app.db.models.kb import KBArticle
from app.nlp.embeddings import emb
from app.services.serialize import to_bytes

CSV_PATH = Path(__file__).resolve().parents[3] / "data" / "seeds" / "kb_articles.csv"

def main():
    print(f"[seed] CSV: {CSV_PATH} (exists={CSV_PATH.exists()})")
    create_db_and_tables()
    print("[seed] DB ready. Loading CSV…")

    rows = list(csv.DictReader(open(CSV_PATH, newline="", encoding="utf-8")))
    print(f"[seed] {len(rows)} KB rows found. Computing embeddings…")

    with Session(engine) as session:
        for i, row in enumerate(rows, start=1):
            title = row["title"]
            content = row["content"]
            tags = row.get("tags") or None

            vec = emb.encode_text(content)
            session.add(KBArticle(title=title, content=content, tags=tags, embedding=to_bytes(vec)))

            if i % 2 == 0 or i == len(rows):
                session.commit()
                print(f"[seed] Committed {i}/{len(rows)}")

    print("[seed] KB seeded.")

if __name__ == "__main__":
    main()
