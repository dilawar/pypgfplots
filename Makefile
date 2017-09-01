
all : build docs
	@echo "All done"

build :
	python -m compileall .
	python setup.py build

install :
	python setup.py install --user

test : ./pypgfplots.py
	( cd tests && $(MAKE) )
	@echo "All tests are done"

png : ./pypgfplots.py
	( cd tests && $(MAKE) png )
	@echo "PNG generation done"

%.py.tex : %.py
	PYTHONPATH=. python $<

%.pdf : %.tex
	pdflatex $<

%.png : %.pdf 
	convert $< $@

docs :
	cd docs && $(MAKE)
