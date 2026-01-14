# Project Ideas & Next Steps

This document outlines potential enhancements for the Money Stuff Explorer project.

## 1. Named Entity Recognition (NER) & Timeline Analysis
**Goal**: Identify companies, people, and organizations mentioned in articles to visualize their frequency over time.
-   **Implementation**: Use `spaCy` or a lightweight LLM to extract entities from article text.
-   **Entity Resolution (Merging Aliases)**: Solve the "Elon" vs "Elon Musk" problem:
    -   **Canonical Mapping**: Maintain a dictionary of aliases (e.g., `{"Musk": "Elon Musk", "SBF": "Sam Bankman-Fried"}`).
    -   **Fuzzy Matching**: Use libraries like `thefuzz` to group similar names (e.g., "J.P. Morgan" vs "JP Morgan").
    -   **Longest Substring**: In a single article, map short names (e.g., "Levine") to the longest widely used name found in that text (e.g., "Matt Levine").
    -   **Knowledge Base Linking**: Link entities to Wikidata/DBpedia IDs to unify synonyms natively.
-   **Storage**: Create a new table `entity_mentions` linking `article_id` to entities.
-   **Visualization**: Add a Streamlit chart showing the "History of [Entity]" (e.g., plot mentions of "FTX" or "Elon Musk" over time).

## 2. Topic Modeling & Clustering
**Goal**: Automatically group articles into themes (e.g., "Crypto", "Banking", "Regulation") without manual tagging.
-   **Implementation**: Use TF-IDF or Embedding-based clustering (e.g., K-Means on OpenAI/HuggingFace embeddings).
-   **Feature**: "Similar Articles" recommendation in the Streamlit app.

## 3. Semantic Search (Vector Search)
**Goal**: Allow users to search by *concept* rather than just keywords.
-   **Implementation**: Generate embeddings for all articles using a local model (like `sentence-transformers`). Store in a vector store (or simple local array/SQLite with extensions).
-   **Benefit**: Searching for "fraud" returns articles about "scams" even if the word "fraud" isn't used.

## 4. Q&A Chatbot (RAG)
**Goal**: Let users ask questions like "What is Matt's opinion on crypto regulations?"
-   **Implementation**: Use the parsed database as a context retriever for an LLM (Retrieval Augmented Generation).
-   **UI**: specific "Ask Matt" chat interface in Streamlit.

## 5. Automated Updates
**Goal**: Keep the database fresh without manual scripts.
-   **Implementation**: A script using `imaplib` to fetch the latest email from the server, parse it, and append it to the DB if it doesn't exist.

## 6. Sentiment Analysis
**Goal**: Track the "mood" of different topics.
-   **Implementation**: Analyze text sentiment per article. Visualize if coverage of a topic (e.g., "Tech") is becoming more positive or negative over time.
