# Examples
## [test_2dplota.py]({{ site.url }} /tests/test_2dplota.py)


```python
import sys
import pypgfplots 
import numpy as np

x = np.arange( 0, 1, 0.1 )
y1 = np.random.randint( 0, 11, len(x) )
y2 = np.random.randint( 0, 11, len(x) )

# For each x, there is only 1-axis. There could be multiple ys.
pypgfplots.write_standalone( None, (y1, y2), '%s.tex' % sys.argv[0] 
        , xlabel = 'Index', ylabel = '$\frac{a}{b}$'
        , title = "Plot with Index."
        , legends = [ "Series A", "Series B" ]
        , label = r'\bf a.'
        )
 
```

![test_2dplota.py](test_2dplota.py.png)
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