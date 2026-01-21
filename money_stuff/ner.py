import os

# 1. Enable fallback for ops not yet implemented in MPS (Critical for stability)
os.environ["PYTORCH_ENABLE_MPS_FALLBACK"] = "1"

import spacy
import torch
import time

from loguru import logger

from money_stuff import get_all_ml_articles
from money_stuff.db import save_entities


def extract_ents(doc, doc_id):
    return [
        {
            "article_id": doc_id,
            "text": ent.text,
            "label": ent.label_,
            "start_char": ent.start_char,
            "end_char": ent.end_char,
        }
        for ent in doc.ents
    ]


if __name__ == "__main__":

    articles = get_all_ml_articles()
    len(articles)
    logger.info(f"Found {len(articles)} articles")

    cpu: bool = True

    # Force spaCy to use the GPU (MPS)
    if torch.backends.mps.is_available():
        print("🚀 Using Apple MPS (GPU) acceleration")
        spacy.require_gpu()

        cpu = False
    else:
        print("⚠️ MPS not detected, falling back to CPU")
        cpu = True

    # Load the transformer model
    nlp = spacy.load(
        "en_core_web_trf", disable=["tagger", "parser", "attribute_ruler", "lemmatizer"]
    )

    ids = [a["id"] for a in articles]
    texts = [article["ml_text"] for article in articles]

    # Processing
    # Note: On GPU, n_process (multiprocessing) usually crashes or adds overhead.
    # Keep batch_size moderate (50-100) to keep the GPU fed without OOM.
    start = time.time()

    if cpu:
        docs = list(nlp.pipe(texts, batch_size=100, n_process=6))
    else:
        docs = list(nlp.pipe(texts, batch_size=100))

    print(f"Time: {time.time() - start:.2f}s")

    all_entities = []
    for i, doc in enumerate(docs):
        all_entities.extend(extract_ents(doc, ids[i]))

    save_entities(all_entities)
    logger.info(f"Successfully saved {len(all_entities)} entities to the database")
