PYTHON=python
TEST_SCRIPTS:=$(wildcard ./tests/*.py)

all : build docs test
	@echo "All done"

build :
	$(PYTHON) -m compileall .
	$(PYTHON) -m compileall .
	$(PYTHON) setup.py build

install :
	$(PYTHON) setup.py install --user

test : ./pypgfplots.py $(TEST_SCRIPTS)
	( cd tests && $(MAKE) )
	@echo "All tests are done"

png : ./pypgfplots.py 
	( cd tests && $(MAKE) png )
	@echo "PNG generation done"

%.py.tex : %.py
	PYTHONPATH=. $(PYTHON) $<

%.pdf : %.tex
	pdflatex $<

%.png : %.pdf 
	convert $< $@

docs : $(TEST_SCRIPTS) ./docs/generate_docs.py
	cd docs && $(MAKE)
