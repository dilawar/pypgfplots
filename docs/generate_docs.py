#!/usr/bin/env python

import os
import pygments
from pygments.lexers import get_lexer_by_name
from pygments.formatters import HtmlFormatter

docFile = 'index.html'
css = HtmlFormatter().get_style_defs('.highlight')

with open( 'highlight.css', 'w' ) as f:
    f.write( css )

lexer = get_lexer_by_name("python", stripall=True)
formatter = HtmlFormatter(linenos=True, cssclass="source")

files = [ ]
for d, sd, fs in os.walk( '../tests/' ):
    for f in fs:
        if '.py' == f[-3:]:
            files.append( os.path.join( d, f ) )

pytext = [ ]
for f in files:
    with open( f, 'r' ) as _f:
        pytext.append( _f.read( ) ) 

headHtml = '<link rel="stylesheet" type="text/css" href="highlight.css" >'

text = [ '<!DOCTYPE html> <meta charset="utf-8"> ' ]
text += [ '<html> <head>%s</head> <body>' % headHtml ]
text += [ '<h1>Examples</h1>' ]

text.append( "<table>" )
for f, ftext in zip( files, pytext ):
    fname = os.path.basename( f )
    imgname = fname + '.png'
    url = '{{ site.url }} /tests/%s' % fname 
    text.append( '<tr>' )
    text.append( '</td><td>' )
    code = pygments.highlight( ftext, lexer, formatter )
    text.append( '<div class="highlight">%s </div>' % code )
    text.append( '</td><td>' )
    text.append( '<img src="%s" width="500px">' % imgname )
    text.append( '</td>' )
    text.append( '</tr>' )

text += [ "</table>" ]

text += [ '</body> </html>' ]

txt = '\n'.join( text )
with open( docFile, 'w' ) as f:
    print( txt )
    f.write( txt )

