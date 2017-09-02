TEST_SCRIPTS:=$(wildcard ./tests/*.py)

all : build docs test
	@echo "All done"

build :
	python -m compileall .
	python setup.py build

install :
	python setup.py install --user

test : ./pypgfplots.py $(TEST_SCRIPTS)
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

docs : $(TEST_SCRIPTS)
	cd docs && $(MAKE)
