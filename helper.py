"""methods.py: 

"""
    
__author__           = "Dilawar Singh"
__copyright__        = "Copyright 2017-, Dilawar Singh"
__version__          = "1.0.0"
__maintainer__       = "Dilawar Singh"
__email__            = "dilawars@ncbs.res.in"
__status__           = "Development"

import sys
import os

delimiter_ = '@@'

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

def keyvalToDict( listofkeyval, attr = { } ):
    if not listofkeyval:
        return attr

    if not isinstance( listofkeyval, list ):
        listofkeyval = listofkeyval.split( ';' )

    for a in listofkeyval:
        if '=' in a:
            key, val = a.split( '=', 1 )
        else:
            key, val = a,  ''
        attr[ key.strip() ] = clean( val.strip( ) )

    return attr 

def remove_chars( text, chars ):
    for c in chars:
        text = text.replace( c, '' )
    return text

def is_sequence(arg):
    return (not hasattr(arg, "strip") and
            hasattr(arg, "__getitem__") or
            hasattr(arg, "__iter__"))
