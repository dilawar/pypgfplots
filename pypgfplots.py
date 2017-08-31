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
import re

delimiter_ = '@@'
def _m( name ):
    '''Generate macros '''
    global delimiter_
    return '%s%s%s' % (delimiter_, name, delimiter_ )

def _sub( name, value, text ):
    return text.replace(  _m( name ), value )

def clean( s ):
    s = s.replace( "\t", "\\t" )
    s = s.replace( "\f", "\\f" )
    s = s.replace( "\b", "\\b" )
    s = s.replace( "\n", "\\n" )
    return s

def get_default_attribs( listofkeyval, **kwargs ):
    ''' listofkeyval: list 'key=val' or a ;-separated string e.g
    'key1=val1;key2=val2''
    '''
    default = [ ]
    if not isinstance( listofkeyval, list ):
        listofkeyval = listofkeyval.split( ';' )
    for a in listofkeyval:
        if '=' in a:
            key, val = a.split( '=', 1 )
            if kwargs.get( key, '' ):
                val = kwargs[ key ]
            default.append( b'%s=%s' % (key, clean(val) ) )
        else:
            default.append( clean( a ) )
    return ', '.join( default )

def indent( text, prefix = '  ' ):
    newLines = [ ]
    for l in text.split( '\n' ):
        newLines.append( prefix + l )
    return '\n'.join( newLines )

def addPlot( x, y, legend = '', **kwargs ):
    """ Add an axis to picture """

    res = [ ]
    if kwargs.get( 'vergin_axis', False ):
        res += [ '\\addplot [ ' + _m( 'plot_attribs' ) + '] coordinates { ' ]
    else:
        res += [ '\\addplot+ [ ' + _m( 'plot_attribs' ) + '] coordinates { ' ]
    res += [ _m( 'DATA' ) ]
    res += [ '  };' ]

    # Add legend entry.
    if legend:
        res += [ '\\addlegendentry{ %s };' % legend ]
    text = '\n'.join( res )

    # These are default plot attributesi.
    defaultPlotAttribs = [ ]
    defaultPlotAttribsText = ', '.join( defaultPlotAttribs )
    text = _sub( 'plot_attribs'
            , defaultPlotAttribsText + kwargs.get( 'plot_attribs', '' ) 
            , text )

    # Now attach data.
    data = [ ]
    every = int( kwargs.get( 'every', 1 ))

    # If x is empty or None, use index.
    if x is None or len(x) < 1:
        x = np.arange( 0, len( y ), 1 )
    for a, b in zip( x[::every], y[::every] ):
        data.append( ' ( %g, %g )' % (a, b ) )

    dataTxt = indent( '\n'.join( data ), ' '*4 )
    text = _sub( 'DATA', dataTxt, text )

    return text

def addAxis( x, ys, **kwargs ):
    axis = [ '\\begin{axis}[ ' + _m( 'axis_attribs' ) + ' ] ' ]
    # Attach axis.
    legends = kwargs.get( 'legends', '' )
    if not isinstance( legends, list ):
        legends = legends.split( ',' )
    series = [ ]
    for i, y in enumerate( ys ):
        l = ''
        if len( legends ) > i:
            l = legends[ i ]
        axis.append( indent( addPlot( x, y, legend = l, **kwargs ), '  ' ) )
    axis += [ '\\end{axis}' ]
    axisText = '\n'.join( axis )
    # Add these default axis attributes.
    defaultAxisAttribs = [ ]
    attribs = [ 
            'xlabel=', 'ylabel=', 'title=', 'legend style={draw=none,font=\footnotesize}' 
            ] 
    defaultAxisAttribsText = get_default_attribs(  attribs, **kwargs ) 
    axisText = _sub( 'axis_attribs', defaultAxisAttribsText, axisText )
    return axisText


def toPGFPlot( xs, ys, **kwargs ):
    """toPGFPlot Convert given x, ys to  a tikzpicture.

    :param x: value on x-axis. 
    :param ys: single or multiple y-axis values.
    :param **kwargs:
    """
    res = [ '\\begin{tikzpicture}[ %s ] ' % _m( 'tikzpicture_attribs' ) ]
    res += [ _m( 'AXISES' ) ]
    
    # if label is given, then attach a special node.
    label = kwargs.get( 'label', '' )
    if label:
        res += [ '\\node[fill=none] at (rel axis cs:-0.1,1.2) {%s};' % label ]
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

    if not isinstance( xs, list ):
        xs, ys = [ xs ], [ ys ]
    
    axises = [ ]
    for i, x in enumerate( xs ):

        axisText = addAxis( x, ys[i], **kwargs )
        axises.append( axisText )

    text = _sub( 'AXISES', '\n'.join( axises ), text )
    return text 

def standalone( x, y, outfile = '', **kwargs ):
    res = [ '% \RequirePackage{luatex85,shellesc}' ]
    defaultStandaloneAttribText = get_default_attribs( [ 'multi=false' ], **kwargs )
    res += [ '\\documentclass[tikz,preview,multi=false]{standalone}' ]
    res += [ '\\usepackage{pgfplots}' ]
    res += [ '\\usepgfplotslibrary{groupplots}' ]
    res += [ '\\begin{document}' ]
    res += [ _m( 'TIKZPICTURE' ) ]
    res += [ '\\end{document}' ]
    text = '\n'.join( res )
    pictureText = toPGFPlot( x, y, **kwargs )

    text = _sub( 'TIKZPICTURE', pictureText, text )

    # Write to file or print to stdout.
    if outfile:
        print( 'Writing to %s' % outfile )
        with open( outfile, 'w' ) as f:
            f.write( text ) 
    else:
        print( text )

if __name__ == '__main__':
    main()

