all : build test 
	@echo "All done"

build :
	python -m compileall .
	python setup.py build

install :
	python setup.py install --user

test : ./test.py ./pypgfplots.py
	python3 $<
	find . -type f -name '*.tex' | xargs -I file pdflatex --shell-escape file
	find . -type f -name '*.pdf' | xargs -I file convert file file.png
