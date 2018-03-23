all:
	cd src; make
	mdbook build .

.PHONY: all
