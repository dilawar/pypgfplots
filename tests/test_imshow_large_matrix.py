import sys
import pypgfplots
import numpy as np

np.random.seed( 10 )

# generate a very large matrix. 
mat = np.random.rand( 1000, 1000 )

pypgfplots.standalone( 
        matrix = mat
        , outfile = '%s.tex' % sys.argv[0] 
        , title = 'A very large matrix'
        , xlabel = 'Index'
        , ylabel = 'Index'
        , every = 10   # Matix is too big, sample every 100 rows/columns
        , label = r'\bf b.'
        )
