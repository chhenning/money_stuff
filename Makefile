.PHONY: setup read_emails parse_newsletters populate_db stats

setup:
	@. ./scripts/setup.sh && clear

read_emails:
	@. ./scripts/setup.sh && clear && python money_stuff/read_emails.py

parse_newsletters:
	@. ./scripts/setup.sh && clear && python money_stuff/newsletter_parser.py

populate_db:
	@. ./scripts/setup.sh && clear && python money_stuff/populate_db.py

stats:
	@. ./scripts/setup.sh && clear && python money_stuff/db_stats.py