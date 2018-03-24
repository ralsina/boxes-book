all: format *.run.md *.md diffs

%.run.md: %.md code/%.py
	env PYTHONPATH=. run_markdown --timeout_seconds=15 $< > $@ 

format: code/*py
	black -l 72 code/*py || true

diffs: code/*py ../tools/*py ../tools/*html
	../tools/diff2HtmlCompare.py -p code/lesson1.py code/lesson2.py && mv index.html diffs/lesson1_lesson2.html
	../tools/diff2HtmlCompare.py -p code/lesson2.py code/lesson3.py && mv index.html diffs/lesson2_lesson3.html
	../tools/diff2HtmlCompare.py -p code/lesson3.py code/lesson4.py && mv index.html diffs/lesson3_lesson4.html
	../tools/diff2HtmlCompare.py -p code/lesson4.py code/lesson5.py && mv index.html diffs/lesson4_lesson5.html

