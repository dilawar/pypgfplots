all : test

test : ./test.py ./pypgfplots.py
	python $<
