SVGS = lesson1.svg lesson2.svg
RUN_MDS = lesson1.run.md lesson2.run.md lesson3.run.md
DIFFS = code/diffs/lesson1_diff.html code/diffs/lesson2_diff.html code/diffs/lesson3_diff.html

all: *.run.md format $(SVGS) $(RUN_MDS) $(DIFFS)


lesson1.run.md: lesson1.md code/lesson1/*py
	env PYTHONPATH=.:code/lesson1 run_markdown --timeout_seconds=15 lesson1.md > lesson1.run.md 
lesson2.run.md: lesson2.md code/lesson2/*py code/lesson2/boxes.py
	env PYTHONPATH=.:code/lesson2 run_markdown --timeout_seconds=15 lesson2.md > lesson2.run.md 
lesson3.run.md: lesson3.md code/lesson3/*py code/lesson3/boxes.py
	env PYTHONPATH=.:code/lesson3 run_markdown --timeout_seconds=15 lesson3.md > lesson3.run.md 

format: code/*/*.py
	black -l 72 code/*/*.py || true

lesson1.svg: code/lesson1/*py
	python code/lesson1/boxes.py ./pride-and-prejudice.txt lesson1.svg
lesson2.svg: code/lesson2/*py
	python code/lesson2/boxes.py ./pride-and-prejudice.txt lesson2.svg --page-size=10x20

code/diffs/lesson1_diff.html: code/lesson1/boxes.py ../part1/code/lesson11.py
	../../tools/diff2HtmlCompare.py -p ../part1/code/lesson11.py code/lesson1/boxes.py && mv index.html code/diffs/lesson1_diff.html
code/diffs/lesson2_diff.html: code/lesson1/boxes.py code/lesson2/boxes.py
	../../tools/diff2HtmlCompare.py -p code/lesson1/boxes.py code/lesson2/boxes.py && mv index.html code/diffs/lesson2_diff.html
code/diffs/lesson3_diff.html: code/lesson2/boxes.py code/lesson3/boxes.py
	../../tools/diff2HtmlCompare.py -p code/lesson2/boxes.py code/lesson3/boxes.py && mv index.html code/diffs/lesson3_diff.html

.PHONY: all format
