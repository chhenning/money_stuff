# money-stuff
End-to-end RAG pipeline and analysis engine for financial newsletters using LLMs and semantic search.

# WIP

- [x] Read emails.
- [x] Parse newsletter.
- [x] Add newsletters to sqlite database.
- [x] Populate sqlite db including script for stats.
- [x] Add `streamlit` app.
- [] NER
    - [x] Run Spacy to extract entities
    - [ ] see [ner steps](ner.md)
- [] RAG Pipeline
    - [] Text Chunking for each article


# Stats

```
--- Database Statistics ---

Total Newsletters: 831
Total Articles:    4557
Date Range:        2021-01-01 22:02:30+00:00 to 2026-01-02 17:04:02+00:00
Avg Articles/NL:   5.51
Max Articles/NL:   9
Min Articles/NL:   1

Avg Word Count/Article: 783.50

--- Top 5 Longest Articles ---
5565 words | Ripple
5260 words | Oh Elon
4939 words | Oh Elon
4388 words | Silicon Valley Bank
4286 words | Oh Sam
```

# RAG Pipeline

Using

```sh
llama-server \
  --model ~/.cache/llama.cpp/Qwen3-30B-A3B-Instruct-2507-Q8_0.gguf \
  --n-gpu-layers 999 \
  --port 32000
```



# Troubleshooting

## Spacy

When using `uv` there is no standalone `pip` tool. Below is how to circumvent the issue.

```sh
uv add "spacy[transformers]"

uv pip install \
  https://github.com/explosion/spacy-models/releases/download/en_core_web_trf-3.8.0/en_core_web_trf-3.8.0-py3-none-any.whl

# sanity check
uv run -- python -c "import spacy; spacy.load('en_core_web_trf'); print('ok')"
```
