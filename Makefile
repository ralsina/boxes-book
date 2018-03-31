all:
	cd src; make
	gitbook build . public

serve:
	gitbook serve . 

.PHONY: all
