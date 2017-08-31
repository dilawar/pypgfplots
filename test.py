from pypgfplots import *

def test( ):
    x = np.arange( 0, 1, 0.1 )
    y1 = np.random.randint( 0, 11, len(x) )
    y2 = np.random.randint( 0, 11, len(x) )
    # For each x, there is only 1-axis. There could be multiple ys.
    standalone( x, [y1, y2], 'figure_a.tex' 
            , xlabel = 'time', ylabel = '$\frac{a}{b}$'
            , title = "Figure 1"
            , legends = [ "Series A", "Series B" ]
            )

def main( ):
    test( )

if __name__ == '__main__':
    main()
