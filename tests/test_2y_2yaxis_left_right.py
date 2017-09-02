# Having multiple y-axis with 1 x-axis not very well tested. This is a corner
# case and should be avoided.
import sys
import pypgfplots 
import numpy as np

np.random.seed( 1 )

x = np.arange( 0, 1, 0.1 )
y1 = np.random.randint( 0, 11, len(x) )
y2 = np.random.randint( 11, 101, len(x) )

# There are two y-series on two different y-axis. One will be on left and
# another will be on right.
# be plotted together.
pypgfplots.standalone( (x, y1), (x, y2)
        , outfile = '%s.tex' % sys.argv[0] 
        , xlabel = 'Time'
        , color = [ 'red', 'blue' ]
        # Don't using ylabel when multiple series are plotted. Use ylabels.
        , ylabel = [ 'conc', 'N' ]
        , title = "Plot with Index."
        , legends = [ "Series A", "Series B" ]
        , axis_attrib = 'legend pos=outer north east'
        , label = r'\bf a.'
        )
