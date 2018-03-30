SVGS = lesson1.svg

all: *.run.md format $(SVGS)


%.run.md: %.md
	env PYTHONPATH=. run_markdown --timeout_seconds=15 $< > $@ 

format: code/*/*.py
	black -l 72 code/*/*.py || true

lesson1.svg: code/lesson1/*py
	python code/lesson1/boxes.py ./pride-and-prejudice.txt lesson1.svg

.PHONY: all format
