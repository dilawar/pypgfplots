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
import subprocess
import tempfile

delimiter_ = '@@'


def which(file):
    for path in os.environ["PATH"].split(os.pathsep):
        if os.path.exists(os.path.join(path, file)):
                return os.path.join(path, file)
    return None

latexFound_ = True
LATEX = which( 'lualatex' ) or which( 'pdflatex' ) 
if LATEX is None:
    latexFound_ = False


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
    try:
        s = s.replace( "\t", "\\t" )
        s = s.replace( "\f", "\\f" )
        s = s.replace( "\b", "\\b" )
        s = s.replace( "\n", "\\n" )
    except Exception as e:
        print( 'WARN: Failed to cleanup %s of type %s' % (s, type(s)) )
        raise e
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

def attachExtraAttrib( listofkeyval, attr ):
    keyvalToDict( listofkeyval, attr )

def remove_chars( text, chars ):
    for c in chars:
        text = text.replace( c, '' )
    return text

def is_sequence(arg):
    if type( arg ) == str:
        return False
    return hasattr(arg, "__getitem__") or hasattr(arg, "__iter__")


def merge_dict( dict1, dict2 ):
    '''Merge two dictionaries.
    '''
    combined = dict( )
    for k in dict1:
        combined[k] = dict1[k]
    for k in dict2:
        combined[k] = dict2[k]

    return combined


def savefile( text, filename ):
    # definately save a tex file.
    global LATEX
    assert filename, "Empty filename"
    assert filename, "Empty filename"

    dirname = os.path.dirname( filename )
    if not dirname:
        dirname = '.'

    assert dirname, "Could not determine directory of %s" % filename 
    auxD = tempfile.gettempdir( )
    outD = dirname
    basename = os.path.basename( filename )
    nameWe = '.'.join( basename.split( '.' )[:-1] )            # drop extention.
    texfile = os.path.join( dirname, nameWe + '.tex' )
    with open( texfile, 'w' ) as f:
        f.write( text )

    ext = filename.split( '.' )[-1].strip( ).lower( )
    # texargs = '-aux-directory=%s -output-directory=%s ' % ( auxD, outD )
    # NOTE: Luatex does not have -aux-directory option.
    texargs = '-output-directory=%s ' % outD
    if ext in [ 'pdf' ]:
        if latexFound_:
            cmd =  "%s -shell-escape %s %s" % (LATEX, texargs, texfile)
            print( 'Executing %s' % cmd )
            subprocess.call( cmd.split( ) )
        else:
            print( '[WARN] No lualatex/pdflatex found' )
    elif ext in [ 'ps' ]:
        if latexFound_:
            cmd =  "latex --shell-escape %s %s" % (texargs, texfile)
            print( 'Executing %s' % cmd )
            subprocess.call( cmd.split( ) )
        else:
            print( '[WARN] No latex found' )
    else:
        with open( filename, 'w' ) as  f:
            f.write( text )

    ## Remove tex-file if user specified name is different.
    #if filename != texfile:
    #    os.unlink( texfile )
