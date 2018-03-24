all: format *.run.md *.md diffs

%.run.md: %.md 
	env PYTHONPATH=. run_markdown --timeout_seconds=15 $< > $@ 

format: code/*py
	black -l 72 code/*py || true

diffs: code/*py ../tools/*py ../tools/*html
	../tools/diff2HtmlCompare.py -p code/lesson1.py code/lesson2.py && mv index.html diffs/lesson1_lesson2.html
	../tools/diff2HtmlCompare.py -p code/lesson2.py code/lesson3.py && mv index.html diffs/lesson2_lesson3.html

