import os

docFile = 'index.md'

files = [ ]
for d, sd, fs in os.walk( '../tests/' ):
    for f in fs:
        print( f )
        if '.py' == f[-3:]:
            files.append( os.path.join( d, f ) )

pytext = [ ]
for f in files:
    with open( f, 'r' ) as _f:
        pytext.append( _f.read( ) ) 

text =  [ '# Examples' ]
text.append( "<table>" )

for f, ftext in zip( files, pytext ):
    fname = os.path.basename( f )
    imgname = fname + '.png'
    url = '{{ site.url }} /tests/%s' % fname 
    text.append( '## [%s](%s)\n\n' % (fname, url) )
    text.append( '<tr><td>\n' )
    text.append( '```python\n%s \n```' % ftext )
    text.append( '</td><td>' )
    text.append( '\n![%s](%s)' % (fname, imgname ) )
    text.append( '</td></tr>' )

text += [ "</table>" ]

txt = '\n'.join( text )
with open( docFile, 'w' ) as f:
    print( txt )
    f.write( txt )

