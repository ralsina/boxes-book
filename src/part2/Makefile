all: *.md


%.py.run.md: %.py.md
	env PYTHONPATH=. run_markdown --timeout_seconds=15 $< > $@ 
