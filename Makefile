all : test

build :
	python -m compileall .

test : ./test.py ./pypgfplots.py
	python $<
	python3 $<
	find . -type f -name '*.tex' | xargs -I file pdflatex --shell-escape file
