For a newsletter corpus like your Money Stuff project, the “best” NER setup is usually hybrid: a strong statistical model for general entities, plus domain rules/gazetteers for finance-y stuff (tickers, instruments, regulators), plus canonicalization/entity linking so the output is actually usable.

What tends to work best in practice

1) Start with a high-quality base model (Transformer NER)
	•	Use a modern transformer NER model as your baseline (spaCy transformer pipeline or a Hugging Face NER model).
	•	This gives you solid PERSON / ORG / GPE / DATE coverage with minimal effort.

2) Add deterministic “finance glue” (rules + dictionaries)
Transformer NER is not reliably great at:
	•	tickers (AAPL, TSLA, BRK.B)
	•	exchange suffixes (RDS.A, SHOP.TO)
	•	product/instrument patterns (5.25% 2034s, “convertible notes”, “CDS”)
	•	shorthand org names (“the Fed”, “DOJ”, “SEC”)
So add:
	•	regex for tickers and percent-coupon patterns
	•	gazetteers (lists) for common regulators, exchanges, big banks, etc.
	•	a phrase matcher for known entities you already have in your DB

In spaCy this is typically EntityRuler + PhraseMatcher before/after the ML component.

3) Normalize + link entities (this is where projects succeed or fail)
Raw spans aren’t enough. You want:
	•	surface_form: “Apple”
	•	canonical: “Apple Inc.”
	•	id: stable key (Wikidata QID, OpenFIGI, LEI, internal UUID)
	•	type: ORG / PERSON / TICKER / INSTRUMENT / REGULATOR / etc.

Do simple normalization first (strip punctuation, unify quotes, collapse whitespace), then:
	•	exact match → alias table → fuzzy match → (optional) external linker.

4) Fine-tune only after you have error stats
Before training anything:
	•	sample 200–500 articles
	•	measure: precision/recall by entity type, plus top error buckets (missed tickers, wrong ORG boundaries, etc.)
If the main pain is domain entities, rules + dictionaries usually beat fine-tuning.
If the pain is lots of consistent misses/label confusion, then fine-tune.

5) Use LLMs strategically (not as your default NER)
LLMs can be excellent for:
	•	bootstrapping labeled data (“silver labels”)
	•	resolving ambiguous mentions
	•	extracting richer finance structures (issuer, instrument, maturity, coupon)
But for high-throughput NER they can be:
	•	slower / more expensive
	•	less consistent across runs
A strong pattern is: model+rules first, then send only “hard” sentences/spans to an LLM as a second pass.

A pragmatic “best” pipeline for your newsletter KB
	1.	Clean text → sentence split
	2.	Run transformer NER
	3.	Apply EntityRuler/PhraseMatcher for tickers/regulators/instruments
	4.	Post-process: merge overlaps, fix boundaries, dedupe
	5.	Canonicalize + link to your entity table
	6.	Store spans + offsets + canonical IDs (so you can re-run later)

If you tell me what entity schema you want (just PERSON/ORG/TICKER? plus INSTRUMENT/LAW/REGULATOR?), I can suggest a concrete spaCy/HF pipeline layout and the exact rule patterns that usually pay off fastest for newsletters.