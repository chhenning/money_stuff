
CREATE TABLE IF NOT EXISTS newsletter (
  id             INTEGER PRIMARY KEY,
  sent_date      DATETIME NOT NULL,
  subject        TEXT NOT NULL,
  UNIQUE(sent_date, subject) ON CONFLICT IGNORE
);

CREATE TABLE IF NOT EXISTS article (
  id              INTEGER PRIMARY KEY,
  newsletter_id   INTEGER REFERENCES newsletter(id) ON DELETE CASCADE,
  title TEXT  NOT NULL, 
  text  TEXT  NOT NULL, -- markdown
  ml_text TEXT NULL
);

CREATE VIRTUAL TABLE IF NOT EXISTS article_fts
USING fts5(
    title,
    text,
    content='article',
    content_rowid='id'
);


CREATE TABLE IF NOT EXISTS article_ner (
    id           INTEGER PRIMARY KEY,
    article_id   INTEGER REFERENCES article(id) ON DELETE CASCADE,
    text         TEXT NOT NULL,
    label        TEXT NOT NULL,
    start_char   INTEGER NOT NULL,
    end_char     INTEGER NOT NULL
);


-- content='article' links the FTS index to your article table.
-- content_rowid='id' tells FTS to sync with the id column.
-- title and text are the searchable fields.
CREATE VIRTUAL TABLE IF NOT EXISTS article_fts
USING fts5(
    title,
    text,
    content='article',
    content_rowid='id'
);


INSERT INTO article_fts(rowid, title, text)
SELECT id, title, text FROM article;

-- Keep FTS in sync automatically (recommended)
CREATE TRIGGER article_ai AFTER INSERT ON article BEGIN
  INSERT INTO article_fts(rowid, title, text)
  VALUES (new.id, new.title, new.text);
END;

CREATE TRIGGER article_au AFTER UPDATE ON article BEGIN
  UPDATE article_fts
    SET title = new.title,
        text  = new.text
    WHERE rowid = new.id;
END;

CREATE TRIGGER article_ad AFTER DELETE ON article BEGIN
  DELETE FROM article_fts WHERE rowid = old.id;
END;
