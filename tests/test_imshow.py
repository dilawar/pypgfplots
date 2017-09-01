import sys
import pypgfplots
import numpy as np
mat = np.random.rand( 10, 10 )

pypgfplots.write_standalone_matrix( mat, outfile = '%s.tex' % sys.argv[0] 
        , title = 'Measurement matrix'
        , xlabel = 'Index'
        , ylabel = 'Index'
        , label = r'\bf b.'
        )
