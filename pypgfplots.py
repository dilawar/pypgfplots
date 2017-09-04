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
import xml.etree.ElementTree as ET
import pgfxml
import latex
import helper

# Create a dictionary of default options.
default_ = { 
        'axis' : [ 'xlabel=', 'ylabel=', 'title='
            , 'legend style={draw=none,fill=none,font=\footnotesize}'  
            # Equivalent to matplotlib 'interpolation' option. Available options
            # are. No checks are performed.
            # pgfplots/shader=flat|interp|faceted|flat corner|flat mean|faceted
            , 'shader=flat'
            , 'axis y line=box' ]
        , 'tikzpicture' : [ 'scale=1', 'xshift=0', 'yshift=0' ]
        }

def dataToTableText( data_dict, **kwargs ):
    header, cols = [ ], [ ]
    for k in data_dict.keys( ): 
        # Matrix plot, insert a new line every time row index change.
        s = data_dict[ k ]
        if len(s) > 0:
            cols.append( s )
            header.append( k )

    header = ' '.join( header )
    coords = [ header ]

    data = np.vstack( cols ).T

    for s in data:
        s = map( lambda x: '%g' % x, s )
        coords.append( ' '.join( s ) )
    dataTxt = '\n'.join( coords )
    return dataTxt 

def generate_ticks( ticktype, ticks ):
    attribs = [ ]
    tickLocation, tickLabels = zip( *ticks )
    tickLocation = map( lambda x: '%s' % x, tickLocation )
    return tickLocation, tickLabels

def attachTicks( axis, **kwargs ):
    for tick in [ 'xtick', 'ytick', 'ztick' ]:
        if kwargs.get( tick, [ ] ):
            loc, label = generate_ticks( tick, kwargs[ tick ] )
            axis.attrib[ tick ] = '{ %s }' % ','.join( loc )
            axis.attrib['%slabels' % tick ] = '{%s}' % ','.join( label )

def attachData( table, data_dict, **kwargs ):
    dataText = dataToTableText( data_dict, **kwargs )
    table.text = '{\n' + dataText + '\n};\n'

def attachTexLabel( plot, id_ ):
    # add a pgfplot label using \label. It can be use by \ref. This is hardly
    # ever used in my own work.
    assert id_ > -1, 'got %s' % id_
    label = 'pgfplots:label%d' % id_
    le = ET.Element( 'label' )
    le.text = '{'+  label + '}'
    plot.append( le )
    return le

def plotAttr( **kwargs ):
    cl = kwargs.get( 'color', '' )
    attr = dict( )
    if cl:
        attr[ 'color' ] = cl
        attr[ 'mark options' ] = '{fill=%s}' % cl
    return attr

def addPlotXML( x, y, z=[], id_=0, **kwargs ):
    """Add plot to axis.

    :param axis: xml element.
    :param x: x-vector.
    :param y: y-vector.
    :param **kwargs:
    """
    attr = plotAttr( **kwargs )
    plot = ET.Element( 'addplot+', **attr )
    tableElem = ET.Element( 'table', x='x', y='y', z='z' )

    every = kwargs.get( 'every', 1)
    if every > 1:
        x, y, z = x[::every], y[::every], z[::every]

    attachData( tableElem, dict( x=x, y=y, z=z), **kwargs )
    plot.append( tableElem )
    
    # Attach a label; hardly ever used in my work.
    attachTexLabel( plot, id_ )

    return plot

def addImshowXML( mat, **kwargs ):
    # Resample data
    every = kwargs.get( 'every', 1 )
    if hasattr( every, '__iter__' ):
        everyRow, everyCol = every[:2]
    else:
        everyRow, everyCol = every, every

    nrows, ncols = mat.shape

    attr = plotAttr( **kwargs )
    attr[ 'matrix plot'] = ''
    attr[ 'mesh/rows' ] = nrows / everyRow

    # If I set this option, I do not get a square image even though I have same
    # numbers of rows and columns.
    ## attr[ 'mesh/cols' ] = nrows / everyCol

    image = ET.Element( 'addplot', **attr )
    tabAttrib = dict( x='x', y='y', meta = 'meta', point_meta='explicit' )
    tableElem = ET.Element( 'table', **tabAttrib )

    x, y, z = [], [], []

    print( 'Every %d and %d' % (everyRow, everyCol) )
    for (i, j), v in np.ndenumerate( mat ):
        if i % everyRow == 0:
            if j % everyCol == 0:
                x.append( i )
                y.append( j )
                z.append( v )

    attachData( tableElem, dict(x=x, y=y, meta=z), **kwargs )
    image.append( tableElem )

    return image

def getDefaultAxis( **kwargs ):
    global default_ 
    axisDefault = helper.keyvalToDict( default_[ 'axis' ] )

    # Also merge the user specified attributes.
    axisDefault = helper.keyvalToDict( kwargs.get( 'axis_attrib', '' ), axisDefault )

    # Overwrite any default by global.
    for k in axisDefault:
        if kwargs.get( k ):
            axisDefault[k] = helper.clean( kwargs[k] )

    axis = ET.Element( 'axis', **axisDefault )
    return axis

def attachLegends( pic, legends, **kwargs ):
    axises = pic.findall( 'axis' )
    lastAxis = axises[-1]
    # collect the labels from other axies.
    plotLabels = [ ]
    for i, axis in enumerate( axises ):
        # Append addlegendentry 
        for p in axis.findall( 'addplot+' ):
            l = p.find( 'label' )
            if l is not None:
                l = helper.remove_chars( l.text, '{}' )
                plotLabels.append( l )

    for i, pl in enumerate( plotLabels ):
        l = ''
        if len(legends) > i:
            l = legends[i]

        legend = 'addlegendentry{%s}' % l
        tag = 'addlegendimage{/pgfplots/refstyle=%s}\\%s' % (pl, legend )
        e = ET.Element( tag )
        lastAxis.append( e )

def tikz_addplot( pic, data, **kwargs ):
    ylabel = kwargs.get( 'ylabel', '' )
    color = kwargs.get( 'color', '' )
    axis, numPlots = None, 0
    for xys in data:
        if len( xys ) == 2:
            kwargs[ 'axis y line'] = 'left' if numPlots % 2 == 0 else 'right'
            # Here ylabel can be a list.
            if helper.is_sequence( ylabel ):
                kwargs[ 'ylabel' ] = ylabel[ numPlots ]
            else:
                kwargs[ 'ylabel' ] = ylabel

            # Similarly color.
            if helper.is_sequence( color ):
                kwargs[ 'color'] = color[numPlots]
            else:
                kwargs[ 'color' ] = color

            axis = getDefaultAxis( **kwargs )
            plot = addPlotXML(  xys[0], xys[1], id_=numPlots, **kwargs )
            axis.append( plot )
            numPlots += 1

            attachTicks( axis, **kwargs )
            pic.append( axis )

        elif len( xys ) > 2:
            # This plot is of format (x, y1, y2 .. ); all plots are to be drawn
            # on same y-axis.
            axis = getDefaultAxis( **kwargs )
            x = xys[ 0 ]
            for i, y in enumerate( xys[1:] ):
                plot = addPlotXML( x, y, id_=numPlots,  **kwargs )
                axis.append( plot )
                numPlots += 1

            attachTicks( axis, **kwargs )
            # Append axis at the end.
            pic.append( axis )
        else:
            raise UserWarning( 'Invalid data' )
    return axis


def tikz_imshow( pic, mat, **kwargs ):
    nrows, ncols = mat.shape 
    assert ncols > 1, 'Must have more than 1 cols'
    assert nrows > 1, 'Must have more than 1 rows'
    axis = getDefaultAxis( **kwargs )
    axis.attrib[ 'colorbar' ] = ''
    axis.attrib[ 'colormap name' ] = 'viridis'
    axis.attrib[ 'enlargelimits' ] = '{abs=0.5}'
    plot = addImshowXML( mat, **kwargs )
    axis.append( plot )
    attachTicks( axis, **kwargs )
    pic.append( axis )
    return axis


def tikzpicture( data, **kwargs ):
    doc = pgfxml.PGFPlot( )


    # Get tikzpicture and merge attributes.
    pic = doc.root
    defaultPicAttr = helper.keyvalToDict( default_[ 'tikzpicture' ] )
    pic.attrib = helper.merge_dict( defaultPicAttr, pic.attrib )

    axis = None

    # If given data is list of tuples, add 2d plots.
    if type( data) is np.ndarray:
        axis = tikz_imshow( pic, data, **kwargs )
    else:
        axis = tikz_addplot( pic, data, **kwargs )

    # attach legend to the last axis. When multiple axises are used,
    # \addlegendentry overwrites previous entry.
    # Make sure that previous axis has appropriate \addlegendimage 
    if axis is not None:
        if kwargs.get( 'legend', '' ):
            attachLegends( pic, kwargs[ 'legend'], **kwargs )
        

    if axis is not None:
        # Attach label to tikz-picture.
        if kwargs.get( 'label', '' ):
            lE = ET.Element( 'node', xshift='-1cm', yshift='1cm' )
            lE.text = ' (label) at (rel axis cs:0,1) { %s }; ' % kwargs[ 'label' ]
            pic.append( lE )

    return doc.tex( )

def standalone( *plots, **kwargs ):
    """Write a standalone file
    """
    template = latex.standalone_template( **kwargs )
    if len( plots ) > 0:
        picTex = tikzpicture( plots, **kwargs )
    else:
        picTex = tikzpicture( kwargs.get( 'matrix' ), **kwargs )

    # Add plot text to tikzpicture.
    text = helper._sub( 'TIKZPICTURE', picTex, template )

    outfile = kwargs.get( 'outfile', '' )
    if not outfile:
        print( text )
    else:
        with open( outfile, 'w' ) as  f:
            f.write( text )

if __name__ == '__main__':
    main()

