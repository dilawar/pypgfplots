all : build test install
	@echo "All done"

build :
	python -m compileall .
	python setup.py build

install :
	python setup.py install

test : ./test.py ./pypgfplots.py
	python $<
	python3 $<
	find . -type f -name '*.tex' | xargs -I file pdflatex --shell-escape file
