all : build test 
	@echo "All done"

build :
	python -m compileall .
	python setup.py build

install :
	python setup.py install

test : ./test.py ./pypgfplots.py
	python $<
	find . -type f -name '*.tex' | xargs -I file pdflatex --shell-escape file
	find . -type f -name '*.pdf' | xargs -I file convert file file.png
