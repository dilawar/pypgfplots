"""latex.py: 

"""
    
__author__           = "Dilawar Singh"
__copyright__        = "Copyright 2017-, Dilawar Singh"
__version__          = "1.0.0"
__maintainer__       = "Dilawar Singh"
__email__            = "dilawars@ncbs.res.in"
__status__           = "Development"

import sys
import os
import helper

def standalone_template( **kwargs ):
    res = [ '% \RequirePackage{luatex85,shellesc}' ]
    defaultStandaloneAttribText = helper.get_default_attribs( [ 'multi=false' ], **kwargs )
    res += [ '\\documentclass[tikz,preview,multi=false]{standalone}' ]
    res += [ '\\usepackage{pgfplots}' ]
    #  res += [ '\\usepackage{multirow}' ]
    res += [ '\\usepgfplotslibrary{groupplots}' ]
    res += [ '\\renewcommand{\\familydefault}{\\sfdefault}' ]
    res += [ '\\begin{document}' ]
    res += [ helper._m( 'TIKZPICTURE' ) ]
    res += [ '\\end{document}' ]
    return '\n'.join( res )
