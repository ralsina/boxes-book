all: *.run.md *.md

%.run.md: %.md 
	cp $< $@
	env PYTHONPATH=. run_markdown --timeout_seconds=15 --overwrite $@
