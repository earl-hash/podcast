import os
from vector_db.vector_db import VectorDatabase


def ingest(transcript_dir: str, db_path: str) -> None:
    db = VectorDatabase(db_path)
    for filename in os.listdir(transcript_dir):
        if filename.endswith('.txt'):
            path = os.path.join(transcript_dir, filename)
            with open(path, 'r', encoding='utf-8') as f:
                text = f.read()
            doc_id = os.path.splitext(filename)[0]
            db.add_document(doc_id, text)
    db.save()


if __name__ == '__main__':
    transcript_dir = os.path.join(os.path.dirname(__file__), '..', 'transcripts')
    db_path = os.path.join(os.path.dirname(__file__), '..', 'db.json')
    ingest(transcript_dir, db_path)
    print(f"Ingested transcripts from {transcript_dir} into {db_path}")
