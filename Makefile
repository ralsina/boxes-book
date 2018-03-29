all:
	cd src; make
	cd src/part2; make
	mdbook build .

serve:
	mdbook serve . 

.PHONY: all
