all: format *.run.md *.md 

%.run.md: %.md 
	env PYTHONPATH=. run_markdown --timeout_seconds=15 $< > $@ 

format:
	black -l 72 code/*py
