import sys
sys.path += [ '.', '..' ]
import pypgfplots 
import numpy as np

x = np.arange( 0, 1, 0.1 )
y1 = np.random.randint( 0, 11, len(x) )
y2 = np.random.randint( 0, 11, len(x) )

# For each x, there is only 1-axis. There could be multiple ys.
pypgfplots.write_standalone( None, (y1, y2), '%s.tex' % sys.argv[0] 
        , xlabel = 'Index', ylabel = '$\frac{a}{b}$'
        , title = "Plot with Index."
        , legends = [ "Series A", "Series B" ]
        , label = r'\bf a.'
        )
