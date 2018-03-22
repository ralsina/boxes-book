all: lesson1.run.md lesson2.run.md lesson3.run.md
	mdbook build ..

%.run.md: %.md
	cp $< $@
	run_markdown --overwrite $@	