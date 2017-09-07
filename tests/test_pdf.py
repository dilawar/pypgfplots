# Plot subplot in grid.
import sys
import pypgfplots
import numpy as np

np.random.seed( 10 )

m1 = np.random.rand( 10, 10 )
m2 = np.random.rand( 10, 10 )
y1 = np.random.rand( 100 )
y2 = np.random.rand( 100 )

pypgfplots.standalone( 
        subplots = { 
              (0,0) : dict( matrix = m1, title = 'mat A', label = 'a.' )
            , (0,1) : dict( xy = (np.arange(0, 100,1), y1), label = 'b.' )
            , (1,0) : dict( histogram = y1, label = 'b.'
                , xlabel = 'bins', ylabel = 'Count'
                , plot_attrib='fill=blue!20')
            , (1,1) : dict( matrix = m2, title = 'B', label = 'd.' )
            }
        , outfile = '%s.pdf' % sys.argv[0] 
        , title = 'Measurement matrix'
        , label = r'\bf b.'
        )
