.PHONY: test run setup

test:
	@. ./scripts/setup.sh && pytest -q

run:
	@. ./scripts/setup.sh && clear && python app_name/app.py run --param Love
