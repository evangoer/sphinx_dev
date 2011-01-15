# Makefile for generating sffms

BUILDDIR      = build
DISTDIR       = dist
PROJECT       = sffms

.PHONY: all clean sdist install uninstall

all: clean sdist install

clean:
	rm -rf $(BUILDDIR)/* $(DISTDIR)/*

sdist:
	python setup.py sdist

install:
	pip install dist/$(PROJECT)*tar.gz

uninstall:
	pip uninstall -y $(PROJECT)
