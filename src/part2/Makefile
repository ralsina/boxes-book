SVGS = lesson1.svg
RUN_MDS = lesson1.run.md lesson2.run.md
DIFFS = code/diffs/*html

all: *.run.md format $(SVGS) $(RUN_MDS) $(DIFFS)


lesson1.run.md: lesson1.md code/lesson1/*py
	env PYTHONPATH=.:code/lesson1 run_markdown --timeout_seconds=15 lesson1.md > lesson1.run.md 
lesson2.run.md: lesson2.md code/lesson2/*py
	env PYTHONPATH=.:code/lesson2 run_markdown --timeout_seconds=15 lesson2.md > lesson2.run.md 

format: code/*/*.py
	black -l 72 code/*/*.py || true

lesson1.svg: code/lesson1/*py
	python code/lesson1/boxes.py ./pride-and-prejudice.txt lesson1.svg

code/diffs/lesson1_diff.html: code/lesson1/boxes.py ../part1/code/lesson11.py
	../../tools/diff2HtmlCompare.py -p ../part1/code/lesson11.py code/lesson1/boxes.py && mv index.html code/diffs/lesson1_diff.html

.PHONY: all format
