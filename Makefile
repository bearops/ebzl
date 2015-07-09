SHELL = /bin/sh

DEFAULT_GOAL := build-wheel

build-wheel:
	python setup.py bdist_wheel

upload-wheel: build-wheel
	twine upload dist/*

clean:
	-rm -rf build dist ebzl.egg-info

all: build-wheel upload-wheel clean
