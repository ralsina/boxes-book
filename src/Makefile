all: format *.run.md *.md diffs

%.run.md: %.md 
	env PYTHONPATH=. run_markdown --timeout_seconds=15 $< > $@ 

format: code/*py
	black -l 72 code/*py

diffs: code/*py
	../tools/diff2HtmlCompare.py code/lesson1.py code/lesson2.py && mv index.html diffs/lesson1_lesson2.html

