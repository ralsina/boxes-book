all:
	cd src; make
	mdbook build .

serve:
	mdbook serve . 

.PHONY: all
