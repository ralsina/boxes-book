RUN_MDS = lesson0.run.md   lesson11.run.md  lesson2.run.md  lesson4.run.md  lesson6.run.md  lesson8.run.md lesson10.run.md  lesson1.run.md   lesson3.run.md  lesson5.run.md  lesson7.run.md  lesson9.run.md

SVGS = lesson10_lots_of_a.svg  lesson11.svg  lesson3.svg lesson4_side_by_side.svg  lesson6.svg  lesson7_different_letters.svg lesson8.svg lesson10_one_break.svg  lesson1.svg   lesson4_random_box_sizes.svg  lesson4.svg lesson7_adjusted_letters_no_boxes.svg  lesson7_pride_and_prejudice.svg  lesson9.svg lesson10.svg lesson2.svg lesson4_random_sizes.svg lesson5.svg lesson7_adjusted_letters.svg lesson7.svg

all: $(SVGS) $(RUN_MDS) diffs

%.py.run.md: %.py.md code/%.py
	env PYTHONPATH=. run_markdown --timeout_seconds=15 $< > $@ 

%.run.md: %.md
	env PYTHONPATH=. run_markdown --timeout_seconds=15 $< > $@ 

lesson1.svg: lesson1.run.md

lesson2.svg: lesson1.run.md

lesson3.svg: lesson3.run.md

lesson4_random_box_sizes.svg: lesson4.run.md
lesson4_random_sizes.svg: lesson4.run.md
lesson4_side_by_side.svg: lesson4.run.md
lesson4.svg: lesson4.run.md
lesson5.svg: lesson5.run.md
lesson6.svg: lesson6.run.md
lesson7_adjusted_letters_no_boxes.svg: lesson7.run.md
lesson7_adjusted_letters.svg: lesson7.run.md
lesson7_different_letters.svg: lesson7.run.md
lesson7_pride_and_prejudice.svg: lesson7.run.md
lesson7.svg: lesson7.run.md
lesson8.svg: lesson8.run.md
lesson9.svg: lesson9.run.md
lesson10_lots_of_a.svg: lesson10.run.md
lesson10_one_break.svg: lesson10.run.md
lesson10.svg: lesson10.run.md
lesson11.svg: lesson11.run.md

diffs: code/*py ../../tools/*py ../../tools/*html
	../../tools/diff2HtmlCompare.py -p code/lesson1.py code/lesson2.py && mv index.html diffs/lesson1_lesson2.html
	../../tools/diff2HtmlCompare.py -p code/lesson2.py code/lesson3.py && mv index.html diffs/lesson2_lesson3.html
	../../tools/diff2HtmlCompare.py -p code/lesson3.py code/lesson4.py && mv index.html diffs/lesson3_lesson4.html
	../../tools/diff2HtmlCompare.py -p code/lesson4.py code/lesson5.py && mv index.html diffs/lesson4_lesson5.html
	../../tools/diff2HtmlCompare.py -p code/lesson5.py code/lesson6.py && mv index.html diffs/lesson5_lesson6.html
	../../tools/diff2HtmlCompare.py -p code/lesson6.py code/lesson7.py && mv index.html diffs/lesson6_lesson7.html
	../../tools/diff2HtmlCompare.py -p code/lesson7.py code/lesson8.py && mv index.html diffs/lesson7_lesson8.html
	../../tools/diff2HtmlCompare.py -p code/lesson8.py code/lesson9.py && mv index.html diffs/lesson8_lesson9.html
	../../tools/diff2HtmlCompare.py -p code/lesson9.py code/lesson10.py && mv index.html diffs/lesson9_lesson10.html
	../../tools/diff2HtmlCompare.py -p code/lesson10.py code/lesson11.py && mv index.html diffs/lesson10_lesson11.html


.PHONY: diffs