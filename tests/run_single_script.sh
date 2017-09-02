#!/usr/bin/env bash
python $1
pdflatex $1.tex
convert -density 300 -quality 90 $1.pdf $1.png
