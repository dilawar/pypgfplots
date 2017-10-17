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
        , 'tikzpicture' : [ 'scale=1', 'xshift=0', 'yshift=0', 'baseline' ]
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
    helper.attachExtraAttrib( kwargs.get( 'plot_attrib', '' ), attr )
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

    #  xExpr = kwargs.get( 'x', 'x' )
    #  yExpr = kwargs.get( 'y', 'y' )
    #  yExpr = kwargs.get( 'y', 'y' )
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
    attr[ 'mesh/rows' ] = int( nrows / everyRow)

    # If I set this option, I do not get a square image even though I have same
    # numbers of rows and columns.
    ## attr[ 'mesh/cols' ] = int( nrows / everyCol)

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
            axisDefault[k] = '%s' % helper.clean( kwargs[k] )
            if k in [ 'title', 'xlabel', 'ylabel' ]:
                axisDefault[k] = '{%s}' % helper.clean( kwargs[k] )
    
    axis = ET.Element( 'axis', **axisDefault )

    # Some user defined attributes are sure to be part of axis e.g. xmin, ymax
    # etc. Attach them to axis.
    # Do not modify kwargs. It might modify all global kwargs.
    for k in kwargs:
        if 'min' in k or 'max' in k:
            axis.attrib[k] = '%s' % helper.clean( kwargs[k] )

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
            #  kwargs[ 'axis y line'] = 'left' if numPlots % 2 == 0 else 'right'
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

def tikz_addhist( pic, vec, **kwargs ):
    """Plot histogram.
    """
    ylabel = kwargs.get( 'ylabel', '' )
    color = kwargs.get( 'color', '' )
    axis, numPlots = None, 0

    binsize = kwargs.get( 'binsize', 0 )
    if binsize < 1:
        numBins = 10
    else:
        numBins = max( vec ) + 1

    axis = getDefaultAxis( **kwargs )
    kwargs[ 'plot_attrib'] = 'hist={data=y, bins=%d,%s}' % (
            kwargs.get( 'bins', numBins ), kwargs.get( 'hist_attrib', '' )
            ) + ',%s' % kwargs.get( 'plot_attrib', '' )
    kwargs[ 'plot_attrib' ] += ',no marks'

    plot = addPlotXML(  np.arange(0, len(vec),1), vec, id_=0, **kwargs )
    axis.append( plot )

    attachTicks( axis, **kwargs )

    # Append axis at the end.
    pic.append( axis )
    return axis

def tikz_addboxplots( pic, vec, **kwargs ):
    """Plot boxplot.
    """

    ylabel = kwargs.get( 'ylabel', '' )
    color = kwargs.get( 'color', '' )
    axis, numPlots = None, 0
    axis = getDefaultAxis( **kwargs )

    helper.updateDefaultAttribs(axis, [ 'boxplot/draw direction=y' ], **kwargs)

    if type( vec ) != tuple:
        vec = (vec, )
    
    for v in vec:
        kwargs[ 'plot_attrib'] = 'boxplot'
        kwargs[ 'plot_attrib' ] += ',no marks'
        plot = addPlotXML(  np.arange(0, len(v),1), v, id_=0, **kwargs )
        axis.append( plot )

    attachTicks( axis, **kwargs )
    # Append axis at the end.
    pic.append( axis )
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

def tikzpicture_template( doc, **kwargs ):
    # Get tikzpicture and merge attributes.
    pic = doc.root
    # These are default.
    helper.attachExtraAttrib( default_[ 'tikzpicture' ], pic.attrib )
    # These are given by users.
    helper.attachExtraAttrib( kwargs.get( 'picture_attrib', ''), pic.attrib )
    return pic

def tikzpicture( data, **kwargs ):
    doc = pgfxml.PGFPlot( )
    pic = tikzpicture_template( doc,  **kwargs )
    axis = None

    if kwargs[ 'pictype' ] == 'matrix':
        axis = tikz_imshow( pic, data, **kwargs )
    elif kwargs[ 'pictype' ] == 'xy':
        axis = tikz_addplot( pic, data, **kwargs )
    elif kwargs[ 'pictype' ] == 'histogram':
        axis = tikz_addhist( pic, data, **kwargs )
    elif kwargs[ 'pictype' ] == 'boxplot':
        axis = tikz_addboxplots( pic, data, **kwargs )

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

def tabular( grid_dict, **kwargs ):
    """Plot subplot using tabular environment
    """
    tabular = { }
    grid = grid_dict.keys( )
    for k in grid:
        plot = grid_dict[ k ]
        plotTex = standalone_helper( **plot )
        tabular[k] = plotTex

    # Currently we make subplots using tabular environment.
    r, c = map(max, zip( *grid ))
    tabTex = [ '\\begin{tabular}{%s}' % ' '.join( [ 'l' for i in range(c+1)] ) ]
    allRows = [ ]
    for ri in range( r+1 ):
        colspan = int( kwargs.get( 'colspan', 1 ) )
        rowTex = [ ]
        for ci in range( c+1 ):
            entryTex = tabular.get( (ri, ci), ' ' )
            #rowTex.append( ' \\multicolumn{%d}{r}{%s} ' % (colspan, entryTex ))
            rowTex.append( ' %s ' % (entryTex ))
        allRows.append( ' & '.join( rowTex )  )

    tabTex.append( ' \\\\ \n'.join( allRows ) )

    tabTex.append( '\\end{tabular}' )
    tex = '\n'.join( tabTex )
    return tex


def standalone_helper( *plots, **kwargs ):
    """Write a standalone file
    """
    picTex = ''
    if len( plots ) > 0:
        kwargs[ 'pictype' ] = 'xy'
        picTex = tikzpicture( plots, **kwargs )
    else:
        # Either matrix of subplots.
        if 'matrix' in kwargs:
            kwargs[ 'pictype' ] = 'matrix'
            picTex = tikzpicture( kwargs['matrix'], **kwargs )
        elif 'xy' in kwargs:
            kwargs[ 'pictype' ] = 'xy'
            picTex = tikzpicture( [ kwargs['xy'] ], **kwargs )
        elif 'subplots' in kwargs:
            picTex = tabular( kwargs['subplots'], **kwargs ) 
        elif 'histogram' in kwargs:
            kwargs[ 'pictype' ] = 'histogram'
            picTex = tikzpicture( kwargs['histogram'], **kwargs ) 
        elif 'boxplot' in kwargs:
            kwargs[ 'pictype' ] = 'boxplot'
            picTex = tikzpicture( kwargs['boxplot'], **kwargs ) 
        else:
            print( '[Warning] Un-supported function call.' )

    return picTex 


def standalone( *plots, **kwargs ):
    template = latex.standalone_template( **kwargs )

    tex = standalone_helper( *plots, **kwargs )

    # Add plot text to tikzpicture.
    text = helper._sub( 'TIKZPICTURE', tex, template )
    outfile = kwargs.get( 'outfile', '' )
    if outfile:
        helper.savefile( text, outfile )
    else:
        print( text )


if __name__ == '__main__':
    main()

