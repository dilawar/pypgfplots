"""pypgfplots.py: 

"""
    
__author__           = "Dilawar Singh"
__copyright__        = "Copyright 2017-, Dilawar Singh"
__version__          = "1.0.0"
__maintainer__       = "Dilawar Singh"
__email__            = "dilawars@ncbs.res.in"
__status__           = "Development"

import sys
import os
import numpy as np

delimiter_ = '@@'
def _m( name ):
    '''Generate macros '''
    global delimiter_
    return '%s%s%s' % (delimiter_, name, delimiter_ )

def _sub( name, value, text ):
    return text.replace(  _m( name ), value )

def get_default_attribs( listofkeyval, **kwargs ):
    ''' listofkeyval: list 'key=val' or a ;-separated string e.g
    'key1=val1;key2=val2''
    '''
    default = [ ]
    if not isinstance( listofkeyval, list ):
        listofkeyval = listofkeyval.split( ';' )
    for a in listofkeyval:
        key, val = a.split( '=' )
        if kwargs.get( key, '' ):
            val = kwargs[ key ]
        default.append( '%s=%s' % (key, val) )
    return ', '.join( default )

def indent( text, prefix = '  ' ):
    newLines = [ ]
    for l in text.split( '\n' ):
        newLines.append( prefix + l )
    return '\n'.join( newLines )

def add_axis_attribs( text, axis_props_text ):
    return _sub( 'axis_attribs', axis_props_text, text )

def add_plot_attribs( text, plot_props_text ):
    return _sub( 'plot_attribs', plot_props_text, text )

def to_axis( x, y, **kwargs ):
    # Initialize axis and plot.
    res = [ '\\begin{axis}[ %s ]' % _m( 'axis_attribs' ) ]

    if kwargs.get( 'vergin_axis', False ):
        res += [ '  \\addplot [ ' + _m( 'plot_attribs' ) + '] coordinates { ' ]
    else:
        res += [ '  \\addplot+ [ ' + _m( 'plot_attribs' ) + '] coordinates { ' ]

    res.append( _m( 'DATA' ) )
    res += [ '  };' ]
    text = '\n'.join( res )

    # Add these default axis attributes.
    defaultAxisAttribs = [ ]
    defaultAxisAttribsText = get_default_attribs( 
            [ 'xlabel=', 'ylabel=', 'title=' ], **kwargs 
            ) 

    # These are default plot attributesi.
    defaultPlotAttribs = [ ]
    defaultPlotAttribsText = ', '.join( defaultPlotAttribs )
    # And finally replace placeholders keeping axis and plot attributes.
    text = add_axis_attribs( text
            , defaultAxisAttribsText + kwargs.get( 'axis_attribs', '' ) )
    text = add_plot_attribs( text
            , defaultPlotAttribsText + kwargs.get( 'plot_attribs', '' ) )


    # Now attach data.
    data = [ ]
    every = int( kwargs.get( 'every', 1 ))
    for a, b in zip( x[::every], y[::every] ):
        data.append( ' ( %g, %g )' % (a, b ) )

    dataTxt = indent( '\n'.join( data ), ' '*4 )
    text = _sub( 'DATA', dataTxt, text )

    return text

def toPGFPlot( x, y, **kwargs ):
    '''Generate a tikzpicture environment'''
    res = [ '\\begin{tikzpicture}[ %s ] ' % _m( 'tikzpicture_attribs' ) ]
    res += [ _m( 'AXIS' ) ]
    res += [ '\end{tikzpicture}' ]
    text = '\n'.join( res )

    # Default tikzpicture attribs.
    defaultPictureAttribsText = get_default_attribs( 
         [ 'scale=1', 'xshift=0', 'yshift=0' ], **kwargs 
         )

    pictureAttribsText = kwargs.get( 'tikzpicture_attribs', '' )
    text = _sub( 'tikzpicture_attribs'
            , defaultPictureAttribsText + ', ' + pictureAttribsText
            , text )


    # Attach axis.
    axisText = indent( to_axis( x, y, **kwargs ), '  ' )
    text = _sub( 'AXIS', axisText, text )
    return text 

def standalone( x, y, outfile = None, **kwargs ):
    res = [ '\RequirePackage{luatex85,shellesc}' ]
    defaultStandaloneAttribText = get_default_attribs( [ 'multi=false' ], **kwargs )

    res += [ '\documentclass[tikz,preview,multi=false]{standalone}' ]
    res += [ '\usepackage{pgfplots}' ]
    res += [ '\usepgfplotslibrary{groupplots}' ]
    res += [ '\\begin{document}' ]
    res += [ _m( 'TIKZPICTURE' ) ]
    res += [ '\end{document}' ]
    text = '\n'.join( res )

    pictureText = toPGFPlot( x, y, **kwargs )
    text = _sub( 'TIKZPICTURE', pictureText, text )

    # Write to file or print to stdout.
    if outfile:
        with open( outfile, 'w' ) as f:
            f.write( text ) 
    else:
        print( text )

if __name__ == '__main__':
    main()

