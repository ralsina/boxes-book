all: lesson1.run.md lesson2.run.md lesson3.run.md lesson4.run.md lesson5.run.md lesson6.run.md lesson7.run.md
	mdbook build ..

%.run.md: %.md
	cp $< $@
	run_markdown --overwrite $@	
