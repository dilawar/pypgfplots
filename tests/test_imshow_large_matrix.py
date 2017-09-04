import sys
import pypgfplots
import numpy as np

np.random.seed( 10 )

# generate a very large matrix. 
mat = np.random.rand( 1000, 1000 )

pypgfplots.standalone( 
        matrix = mat
        , outfile = '%s.tex' % sys.argv[0] 
        , title = 'A very large matrix for pdflatex'
        , shader = 'interp'
        , xlabel = 'A(i)'
        , ylabel = 'f(A(i))'
        , every = (10,20) # Plot every 10th row and 20th column.
        , label = r'\bf b.'
        )
