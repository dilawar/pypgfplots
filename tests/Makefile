TESTSCRIPTS:=$(wildcard *.py)
TEXS:=$(TESTSCRIPTS:.py=.py.tex)
PDFS:=$(TEXS:.tex=.pdf)
PNGS:=$(PDFS:.pdf=.png)
PYTHON:=python

all : test png

test : $(PDFS) ../pypgfplots.py
	echo "Generated all pdf"

png : $(PNGS)
	echo "Generated PNGs"
	rsync -azv *.png ../docs

%.py.tex : %.py
	PYTHONPATH=$(shell pwd)/.. $(PYTHON) $<

%.pdf : %.tex
	pdflatex -interaction nonstopmode $<

%.png : %.pdf 
	convert -density 300 -quality 90 $< $@
