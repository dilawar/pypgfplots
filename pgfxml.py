"""pgfxml.py: 

"""
    
__author__           = "Dilawar Singh"
__copyright__        = "Copyright 2017-, Dilawar Singh"
__version__          = "1.0.0"
__maintainer__       = "Dilawar Singh"
__email__            = "dilawars@ncbs.res.in"
__status__           = "Development"

import sys
import os
import xml.etree.ElementTree as ET
from helper import *

indent_ = 0

def addSpaces( t, num ):
    return ' ' * num + t

def attribToTikz( attrib ):
    text = [ ]
    for k in attrib:
        kval = ('%s' % k).replace( '_', ' ' )
        if attrib[k]:
            text.append( '%s=%s' % (kval, attrib[k] ) )
        else:
            text.append( kval )
    return ', '.join( text )

class PGFPlot( ):

    def __init__(self, name = ' '):
        self.name = name 
        self.root = ET.Element( "tikzpicture", scale='1', xshift='0', yshift='0' )

    def add_element( self, root, tag, val ):
        self.root.apepnd( tag, val )

    def __str__( self ):
        return ET.tostring( self.root  )

    def toTiKZ( self, elem, indent ):
        lines = [ ]
        attrText = attribToTikz( elem.attrib )
        if attrText:
            attrText = '[ %s ]' % attrText

        if elem.tag in [ 'tikzpicture', 'axis' ]:
            lines += [ '\\begin{%s} %s ' % ( elem.tag, attrText ) ]
        else:
            if elem.tag in [ 'table', 'file', 'coordinates' ]:
                tag = elem.tag
            else:
                tag = r'\%s' % elem.tag 
            lines += [ '%s %s' % (tag, attrText) ]

        # recurse.
        for t in elem:
            lines += self.toTiKZ( t, indent + 2 )

        # Subtext: Text which is to be attached to elem. 
        slines = [ ]
        if elem.text:
            slines += elem.text.strip( ).split('\n' )
        stext = '\n\t'.join( slines )
        # This needs to be attached to just previous line.
        lastLine = lines.pop( )
        lines.append( lastLine + stext )

        # close.
        if elem.tag in [ 'tikzpicture', 'axis' ]:
            lines += [ '\end{%s}' % elem.tag ]
        return map( lambda x: addSpaces(x, indent), lines )

    def tex( self, outfile = None, prefix = '' ):
        lines = self.toTiKZ( self.root, 0 ) 
        if prefix:
            lines = map( lambda x : prefix + x, lines )

        text = '\n'.join( lines )
        return text

