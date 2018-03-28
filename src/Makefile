all: format *.run.md *.md diffs

%.run.md: %.md code/%.py
	env PYTHONPATH=. run_markdown --timeout_seconds=15 $< > $@ 

%.py.run.md: %.py.md code/%.py
	env PYTHONPATH=. run_markdown --timeout_seconds=15 $< > $@ 

format: code/*py
	black -l 72 code/*py || true

diffs: code/*py ../tools/*py ../tools/*html
	../tools/diff2HtmlCompare.py -p code/lesson1.py code/lesson2.py && mv index.html diffs/lesson1_lesson2.html
	../tools/diff2HtmlCompare.py -p code/lesson2.py code/lesson3.py && mv index.html diffs/lesson2_lesson3.html
	../tools/diff2HtmlCompare.py -p code/lesson3.py code/lesson4.py && mv index.html diffs/lesson3_lesson4.html
	../tools/diff2HtmlCompare.py -p code/lesson4.py code/lesson5.py && mv index.html diffs/lesson4_lesson5.html
	../tools/diff2HtmlCompare.py -p code/lesson5.py code/lesson6.py && mv index.html diffs/lesson5_lesson6.html
	../tools/diff2HtmlCompare.py -p code/lesson6.py code/lesson7.py && mv index.html diffs/lesson6_lesson7.html
	../tools/diff2HtmlCompare.py -p code/lesson7.py code/lesson8.py && mv index.html diffs/lesson7_lesson8.html
	../tools/diff2HtmlCompare.py -p code/lesson8.py code/lesson9.py && mv index.html diffs/lesson8_lesson9.html
	../tools/diff2HtmlCompare.py -p code/lesson9.py code/lesson10.py && mv index.html diffs/lesson9_lesson10.html
	../tools/diff2HtmlCompare.py -p code/lesson10.py code/lesson11.py && mv index.html diffs/lesson10_lesson11.html

full:
	rm -f *.svg
	touch code/*.py
	make all
