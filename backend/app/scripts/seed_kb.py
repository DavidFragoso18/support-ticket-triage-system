from pathlib import Path

import pandas as pd
from sqlmodel import Session, select

from app.db.base import create_db_and_tables, engine
from app.db.models.kb import KBArticle
from app.nlp.embeddings import emb

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
            title = row.get('title', row.get('question', 'Untitled'))
            body = row.get('body', row.get('answer', ''))
            category = row.get('category', 'general')
            tags = row.get('tags', row.get('keywords', ''))
            
            # Generate embedding
            text_for_embedding = f"{title} {body} {tags}"
            embedding_list = emb.encode_to_list(text_for_embedding)
            
            article = KBArticle(
                title=title,
                body=body,
                category=category,
                tags=tags,
                embedding=embedding_list,
            )
            session.add(article)
        
        session.commit()
        print(f"✅ Seeded {len(df)} KB articles")

if __name__ == "__main__":
    main(CSV_PATH)