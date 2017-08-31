from pypgfplots import *

def test( ):
    x = np.arange( 0, 1, 0.1 )
    y = np.random.randint( 0, 11, len(x) )
    standalone( x, y, 'figure_a.tex' 
            , xlabel = 'time', ylabel = '$\frac{a}{b}$'
            )

def main( ):
    test( )

if __name__ == '__main__':
    main()
