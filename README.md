# Podcast Vector Database

This project provides a minimal example of building a simple vector database for podcast transcripts using only the Python standard library.

## Ingest transcripts

Place your podcast transcript `.txt` files inside the `transcripts/` directory. Then run:

```bash
python -m vector_db.ingest_transcripts
```

This will create `db.json` containing term-frequency vectors for each transcript.

## Search the database

You can query the database from Python:

```python
from vector_db.vector_db import VectorDatabase

# Load the database

db = VectorDatabase('db.json')

# Search for relevant transcripts
results = db.search('technology and science')
for doc_id, score in results:
    print(doc_id, score)
```
