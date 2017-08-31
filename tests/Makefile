TESTSCRIPTS:=$(wildcard *.py)
TEXS:=$(TESTSCRIPTS:.py=.py.tex)
PDFS:=$(TEXS:.tex=.pdf)
PNGS:=$(PDFS:.pdf=.png)

all : $(PDFS)
	echo "Generated all pdf"

%.py.tex : %.py
	PYTHONPATH=.. python $<

%.pdf : %.tex
	pdflatex $<

%.png : %.pdf 
	convert $< $@
