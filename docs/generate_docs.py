import os

docFile = 'index.html'

files = [ ]
for d, sd, fs in os.walk( '../tests/' ):
    for f in fs:
        if '.py' == f[-3:]:
            files.append( os.path.join( d, f ) )

pytext = [ ]
for f in files:
    with open( f, 'r' ) as _f:
        pytext.append( _f.read( ) ) 

text =  [ '<h1>Examples </h1>' ]

text.append( "<table>" )
for f, ftext in zip( files, pytext ):
    fname = os.path.basename( f )
    imgname = fname + '.png'
    url = '{{ site.url }} /tests/%s' % fname 
    text.append( '<tr>' )
    text.append( '</td><td>' )
    text.append( '<pre>\n %s \n</pre>' % ftext )
    text.append( '</td><td>' )
    text.append( '<img src="%s">' % imgname )
    text.append( '</td>' )
    text.append( '</tr>' )

text += [ "</table>" ]

txt = '\n'.join( text )
with open( docFile, 'w' ) as f:
    print( txt )
    f.write( txt )

