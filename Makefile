
all : build
	@echo "All done"

build :
	python -m compileall .
	python setup.py build

install :
	python setup.py install --user

test : ./pypgfplots.py $(PDFS)
	( cd tests && $(MAKE) )
	@echo "All tests are done"

%.py.tex : %.py
	PYTHONPATH=. python $<

%.pdf : %.tex
	pdflatex $<

%.png : %.pdf 
	convert $< $@
