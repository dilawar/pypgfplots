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
                val = '%s' % kwargs[ key ]
            default.append( '%s=%s' % (key, clean(val) ) )
        else:
            default.append( clean( a ) )
    return ', '.join( default )

def indent( text, prefix = '  ' ):
    newLines = [ ]
    for l in text.split( '\n' ):
        newLines.append( prefix + l )
    return '\n'.join( newLines )

def addData( x, y, z, **kwargs ):
    data = [ ]
    every = int( kwargs.get( 'every', 1 ))

    # If x is empty or None, use index.
    if x is None or len(x) < 1:
        x = np.arange( 0, len( y ), 1 )

    if not z:
        for a, b in zip( x[::every], y[::every] ):
            data.append( ' ( %g, %g )' % (a, b ) )
    else:
        # Matrix plot, insert a new line every time row index change.
        coords = [ 'x y meta' ]
        for a, b, c in zip( x[::every], y[::every], z[::every] ):
            coords.append('%s %s %s' % (a, b, c) )
        data.append( '\n'.join(coords) )
    dataTxt = indent( '\n'.join( data ), ' '*4 )
    return dataTxt 


def addPlot( x, y, z = [], legend = '', **kwargs ):
    """ Add an axis to picture """

    res = [ ]
    if kwargs.get( 'virgin_axis', False ):
        res += [ '\\addplot [ ' + _m( 'plot_attribs' ) + '] table { ' ]
    else:
        res += [ '\\addplot+ [ ' + _m( 'plot_attribs' ) + '] table { ' ]
    res += [ _m( 'TABLEDATA' ) ]
    res += [ '  };' ]

    # Add legend entry.
    if legend:
        res += [ '\\addlegendentry{ %s };' % legend ]
    text = '\n'.join( res )

    # These are default plot attributes.
    attribs = [ ]
    # if z values are given then we are plotting a matrix plot.

    if z:
        nrows = int(max( x )) + 1
        attribs += [ 'mesh/rows=%d' % nrows, 'matrix plot'
                , 'point meta=\\thisrow{meta}', 'colormap name=hot' ]

    attribsText = get_default_attribs( attribs, **kwargs )
    text = _sub( 'plot_attribs', attribsText + kwargs.get( 'plot_attribs', '' ) , text )

    # Now attach data.
    text = _sub( 'TABLEDATA', addData(x, y, z,**kwargs), text )
    return text

def axis_template( **kwargs ):
    axis = [ '\\begin{axis}[ ' + _m( 'axis_attribs' ) + ' ] ' ]
    axis += [ _m( "AXIS" ) ]
    axis += [ "\\end{axis}\n" ]
    axisText = '\n'.join( axis )

    # Add these default axis attributes.
    defaultAxisAttribs = [ ]
    attribs = [ 'xlabel=', 'ylabel=', 'title='
            , 'legend style={draw=none,font=\footnotesize}' 
            , 'width=5cm', 'height=4cm'
            ] 
    defaultAxisAttribsText = get_default_attribs(  attribs, **kwargs ) 
    axisAttr = defaultAxisAttribsText + ',' + kwargs.get( 'axis_attribs', '' )
    axisText = _sub( 'axis_attribs', axisAttr , axisText )
    return axisText

def addAxis( x, ys, **kwargs ):
    """addAxis An axis can have multiple y-series.
    :param x:
    :param ys:
    :param zs:
    :param **kwargs:
    """
    template = axis_template( **kwargs )
    legends = kwargs.get( 'legends', '' )
    if not isinstance( legends, list ):
        legends = legends.split( ',' )
    series = [ ]
    for i, y in enumerate( ys ):
        l = ''
        if len( legends ) > i:
            l = legends[ i ]
        series.append( indent( addPlot( x, y, legend = l, **kwargs ), '  ' ) )
    template = _sub( 'AXIS', '\n'.join( series ), template )
    return template

def addAxisMatrix( x, ys, zs, **kwargs ):
    kwargs[ 'axis_attribs' ] = kwargs.get( 'axis_attribs', '' ) + ',colorbar'
    template = axis_template( enlargelimits = 'false', **kwargs )
    legends = kwargs.get( 'legends', '' )
    if not isinstance( legends, list ):
        legends = legends.split( ',' )
    series = [ ]
    series.append( indent( addPlot( x, ys, zs, legend = '', **kwargs ), '  ' ) )
    template = _sub( 'AXIS', '\n'.join( series ), template )
    return template

def tikzpicture_template( **kwargs ):
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

    return text


def tikzpicture( xs, ys, zs = [ ], **kwargs ):
    """tikzpicture. Convert given x, ys to  a tikzpicture.

    :param x: value on x-axis. 
    :param ys: single or multiple y-axis values.
    :param **kwargs:
    """
    text = tikzpicture_template( **kwargs )
    if xs is None:
        xs, ys, zs = [ xs ], [ ys ], [ zs ]
    elif not isinstance( xs[0], list ):
        xs, ys, zs = [ xs ], [ ys ], [ zs ]
    else:
        pass

    axises = [ ]
    for i, x in enumerate( xs ):
        if not zs:
            axisText = addAxis( x, ys[i], **kwargs )
        else:
            axisText = addAxisMatrix( x, ys[i], zs[i], **kwargs )
        axises.append( axisText )

    text = _sub( 'AXISES', '\n'.join( axises ), text )
    return text 

def tikzpicture3d( x, y, z, **kwargs ):
    return 'Not supported yet.'

def standalone_template( **kwargs ):
    res = [ '% \RequirePackage{luatex85,shellesc}' ]
    defaultStandaloneAttribText = get_default_attribs( [ 'multi=false' ], **kwargs )
    res += [ '\\documentclass[tikz,preview,multi=false]{standalone}' ]
    res += [ '\\usepackage{pgfplots}' ]
    res += [ '\\usepgfplotslibrary{groupplots}' ]
    res += [ '\\begin{document}' ]
    res += [ _m( 'TIKZPICTURE' ) ]
    res += [ '\\end{document}' ]
    return '\n'.join( res )

def matrixPlot( mat, **kwargs ):
    xs, ys, zs = [ ], [ ], [ ]
    for (x,y), z in np.ndenumerate( mat ):
        xs.append( x )
        ys.append( y )
        zs.append( z )
    return tikzpicture( xs, ys, zs, **kwargs )

def write_standalone( x, y, outfile = '', **kwargs ):
    text = standalone_template( **kwargs )
    # For each x there could be multiple of ys.
    pictureText = tikzpicture( x, y, **kwargs )
    text = _sub( 'TIKZPICTURE', pictureText, text )

    # Write to file or print to stdout.
    if outfile:
        print( 'Writing to %s' % outfile )
        with open( outfile, 'w' ) as f:
            f.write( text ) 
    else:
        print( text )

def write_standalone_matrix( mat, outfile = '', **kwargs ):
    """write_standalone_matrix Given a 2d matrix, generate a pgfplot file.
    Matrix is a special case of 3d surf plot.

    :param mat:
    :param outfile:
    :param **kwargs:
    """
    # Make axis virgin.
    kwargs[ 'virgin_axis' ] = True
    template = standalone_template( **kwargs )
    matrix = matrixPlot( mat, **kwargs )
    text = _sub( 'TIKZPICTURE', matrix, template )
    if outfile:
        with open( outfile, 'w' ) as f:
            f.write( text )
    else:
        print( text )

if __name__ == '__main__':
    main()

