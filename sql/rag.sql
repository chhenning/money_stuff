-- new a few more tables

CREATE TABLE IF NOT EXISTS text_chunk(
    id INTEGER PRIMARY KEY,
    article_id INTEGER REFERENCES article(id) ON DELETE CASCADE,
    chunk_id INTEGER NOT NULL,
    text TEXT NOT NULL
);

-- get all articles that don't have a chunk
SELECT id, title, text FROM article WHERE id NOT IN (SELECT article_id FROM text_chunk);