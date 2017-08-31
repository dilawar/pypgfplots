from pypgfplots import *

def test( ):
    x = np.arange( 0, 1, 0.1 )
    y = np.random.randint( 0, 11, len(x) )
    print( toPGFPlot( x, y, every = 2, vergin_axis = True ) )
    print( '== Now standalone' )
    standalone( x, y )

def main( ):
    test( )

if __name__ == '__main__':
    main()
