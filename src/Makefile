all: *.run.md

%.run.md: %.md 
	cp $< $@
	env PYTHONPATH=. run_markdown --timeout_seconds=15 --overwrite $@
