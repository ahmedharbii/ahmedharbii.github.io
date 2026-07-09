.PHONY: help install fetch fetch-apply build serve clean test

help:
	@echo "Targets:"
	@echo "  make install      Install Ruby (Jekyll) and Python (fetch) dependencies"
	@echo "  make fetch        Check Google Scholar; write new pubs to _data/publications.draft.yml"
	@echo "  make fetch-apply  Check Google Scholar; append new pubs straight into publications.yml"
	@echo "  make build        Build the site into _site/ with Jekyll"
	@echo "  make serve        Serve the site locally with live reload"
	@echo "  make test         Build the site and run the website test suite against _site/"
	@echo "  make clean        Remove the built site"

install:
	bundle install
	pip install -r scripts/requirements.txt

# Fetch from Google Scholar. Runs locally where Scholar does not block you.
# Review _data/publications.draft.yml, then move validated entries into
# _data/publications.yml and delete the draft.
fetch:
	python scripts/fetch_publications.py

fetch-apply:
	python scripts/fetch_publications.py --apply

build:
	bundle exec jekyll build

serve:
	bundle exec jekyll serve --livereload

test: build
	SITE_DIR=_site python tests/test_website.py

clean:
	rm -rf _site
