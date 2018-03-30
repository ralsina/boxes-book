SVGS = lesson1.svg
RUN_MDS = lesson1.run.md

all: *.run.md format $(SVGS) $(RUN_MDS)


lesson1.run.md: lesson1.md
	env PYTHONPATH=.:code/lesson1 run_markdown --timeout_seconds=15 lesson1.md > lesson1.run.md 

format: code/*/*.py
	black -l 72 code/*/*.py || true

lesson1.svg: code/lesson1/*py
	python code/lesson1/boxes.py ./pride-and-prejudice.txt lesson1.svg

.PHONY: all format
