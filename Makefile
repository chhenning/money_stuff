.PHONY: setup connect_to_db ingest run_app

setup:
	@. ./scripts/setup.sh && clear

connect_to_db:
	@. ./scripts/connect_to_db.sh

ingest:
	@. ./scripts/setup.sh && clear && python money_stuff/ingest.py

run_app:
	@. ./scripts/setup.sh && clear && streamlit run money_stuff/web_app.py

