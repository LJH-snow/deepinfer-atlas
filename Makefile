.PHONY: build serve verify upstream diagrams
build:
	python3 scripts/build.py
serve:
	python3 -m http.server 4173 --bind 127.0.0.1 --directory site
verify:
	python3 scripts/verify.py
upstream:
	python3 scripts/fetch_upstream.py
diagrams:
	python3 scripts/diagrams.py
