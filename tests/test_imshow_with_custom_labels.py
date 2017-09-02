import sys
import pypgfplots
import numpy as np

np.random.seed( 0 )
# Genearte a random matrix.
mat = np.random.rand( 10, 10 )

pypgfplots.standalone( matrix = mat
        , outfile = '%s.tex' % sys.argv[0] 
        , title = 'Measurement matrix'
        , xlabel = 'Index'
        , ylabel = 'Index'
         # If indices are not given then we compute the tick location.
        , ytick = [ (1,'c1'), (3,'c2'), (6,'c3') ]  
        , label = r'\bf b.'
        )
