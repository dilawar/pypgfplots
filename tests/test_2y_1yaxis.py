import sys
import pypgfplots 
import numpy as np

np.random.seed( 0 )

x = np.arange( 0, 1, 0.1 )
y1 = np.random.randint( 0, 11, len(x) )
y2 = np.random.randint( 0, 11, len(x) )

# There are two y-series on one y-axis. User should make sure that y1 and y2 can
# be plotted together.
pypgfplots.standalone( (x, y1, y2 )
        , outfile = '%s.tex' % sys.argv[0] 
        , xlabel = 'Index', ylabel = '$\frac{a}{b}$'
        , title = "Plot with Index."
        , legend = [ "Series A", "Series B" ]
        , axis_attrib = 'legend pos=outer north east'
        , label = r'\bf a.'
        )
