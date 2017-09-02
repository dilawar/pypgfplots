# Examples
## [test_imshow_with_custom_labels.py]({{ site.url }} /tests/test_imshow_with_custom_labels.py)


```python
import sys
import pypgfplots
import numpy as np

np.random.seed( 0 )
# Genearte a random matrix.
mat = np.random.rand( 10, 10 )

pypgfplots.write_standalone_matrix( mat, outfile = '%s.tex' % sys.argv[0] 
        , title = 'Measurement matrix'
        , xlabel = 'Index'
        , ylabel = 'Index'
         # If indices are not given then we compute the tick location.
        , ytick = [ (1,'c1'), (3,'c2'), (6,'c3') ]  
        , label = r'\bf b.'
        )
 
```

![test_imshow_with_custom_labels.py](test_imshow_with_custom_labels.py.png)
## [test_imshow.py]({{ site.url }} /tests/test_imshow.py)


```python
import sys
import pypgfplots
import numpy as np
mat = np.random.rand( 10, 10 )

pypgfplots.write_standalone_matrix( mat, outfile = '%s.tex' % sys.argv[0] 
        , title = 'Measurement matrix'
        , xlabel = 'Index'
        , ylabel = 'Index'
        , label = r'\bf b.'
        )
 
```

![test_imshow.py](test_imshow.py.png)
## [test_2y_1yaxis.py]({{ site.url }} /tests/test_2y_1yaxis.py)


```python
import sys
import pypgfplots 
import numpy as np

np.random.seed( 0 )

x = np.arange( 0, 1, 0.1 )
y1 = np.random.randint( 0, 11, len(x) )
y2 = np.random.randint( 0, 11, len(x) )

# There are two y-series on one y-axis. User should make sure that y1 and y2 can
# be plotted together.
pypgfplots.write_standalone( (None, y1, y2 )
        , outfile = '%s.tex' % sys.argv[0] 
        , xlabel = 'Index', ylabel = '$\frac{a}{b}$'
        , title = "Plot with Index."
        , legends = [ "Series A", "Series B" ]
        , axis_attrib = 'legend pos=outer north east'
        , label = r'\bf a.'
        )
 
```

![test_2y_1yaxis.py](test_2y_1yaxis.py.png)
## [test_2y_2yaxis_left_right.py]({{ site.url }} /tests/test_2y_2yaxis_left_right.py)


```python
import sys
import pypgfplots 
import numpy as np

np.random.seed( 1 )

x = np.arange( 0, 1, 0.1 )
y1 = np.random.randint( 0, 11, len(x) )
y2 = np.random.randint( 11, 101, len(x) )

# There are two y-series on two different y-axis. One will be on left and
# another will be on right.
# be plotted together.
pypgfplots.write_standalone( (x, y1), (x, y2)
        , outfile = '%s.tex' % sys.argv[0] 
        , xlabel = 'Time', ylabel = '$\frac{a}{b}$'
        , title = "Plot with Index."
        , legends = [ "Series A", "Series B" ]
        , axis_attrib = 'legend pos=outer north east'
        , label = r'\bf a.'
        )
 
```

![test_2y_2yaxis_left_right.py](test_2y_2yaxis_left_right.py.png)