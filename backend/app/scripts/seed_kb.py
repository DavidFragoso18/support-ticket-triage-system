import csv
import pandas as pd
from pathlib import Path
from sqlmodel import Session, select
from app.db.base import engine, create_db_and_tables
from app.db.models.kb import KBArticle
from app.nlp.embeddings import emb
from app.services.serialize import to_bytes

CSV_PATH = Path(__file__).resolve().parents[3] / "data" / "seeds" / "kb_articles.csv"

def main(csv_path: str):
    print(f"[seed] CSV: {csv_path} (exists={Path(csv_path).exists()})")
    create_db_and_tables()
    df = pd.read_csv(csv_path)
    print("[seed] DB ready. Loading CSV…")

    with Session(engine) as session:
        # Clear existing articles (optional)
        session.exec(select(KBArticle)).all()
        session.query(KBArticle).delete()
        
        # Insert new articles
        for _, row in df.iterrows():
            article = KBArticle(
                category=row['category'],
                question=row['question'],
                answer=row['answer'],
                keywords=row['keywords'],
                intent=row.get('intent'),  # Optional
                priority=row.get('priority')  # Optional
            )
            session.add(article)
        
        session.commit()
        print(f"✅ Seeded {len(df)} KB articles")

if __name__ == "__main__":
    main(CSV_PATH)