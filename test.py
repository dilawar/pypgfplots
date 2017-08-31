import pypgfplots 
import numpy as np

def test( ):
    x = np.arange( 0, 1, 0.1 )
    y1 = np.random.randint( 0, 11, len(x) )
    y2 = np.random.randint( 0, 11, len(x) )
    # For each x, there is only 1-axis. There could be multiple ys.
    pypgfplots.write_standalone( None, [y1, y2], 'figure_b.tex' 
            , xlabel = 'Index', ylabel = '$\frac{a}{b}$'
            , title = "Plot with Index."
            , legends = [ "Series A", "Series B" ]
            , label = r'\bf a.'
            )
    pypgfplots.write_standalone( x, [y1, y2], 'figure_a.tex' 
            , xlabel = 'Time (sec)', ylabel = '$\frac{a}{b}$'
            , title = "Plot t vs $\frac{a}{b}$"
            , legends = [ "Series A", "Series B" ]
            , label = r'\bf b.'
            )

def main( ):
    test( )

if __name__ == '__main__':
    main()
