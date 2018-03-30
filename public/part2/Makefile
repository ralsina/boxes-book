all: *.run.md format


%.run.md: %.md
	env PYTHONPATH=. run_markdown --timeout_seconds=15 $< > $@ 

format: code/*/*.py
	black -l 72 code/*/*.py || true

.PHONY: all format
