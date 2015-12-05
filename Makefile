SHELL = /bin/sh

DEFAULT_GOAL := build-wheel

build-wheel:
	python setup.py bdist_wheel

upload-wheel: build-wheel
	twine upload dist/*

install:
	sudo pip install -e .

clean:
	-sudo rm -rf build dist ebzl.egg-info

all: build-wheel upload-wheel clean
