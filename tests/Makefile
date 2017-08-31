TESTSCRIPTS:=$(wildcard *.py)
TEXS:=$(TESTSCRIPTS:.py=.py.tex)
PDFS:=$(TEXS:.tex=.pdf)
PNGS:=$(PDFS:.pdf=.png)

all : test


test : $(PDFS)
	echo "Generated all pdf"

png : $(PNGS)
	echo "Generated PNGs"

%.py.tex : %.py
	PYTHONPATH=.. python $<

%.pdf : %.tex
	pdflatex $<

%.png : %.pdf 
	convert -density 300 -quality 90 $< $@
