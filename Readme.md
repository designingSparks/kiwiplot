# Kiwiplot
Kiwiplot is a performant, beautiful plotting library. Due to its speed it is well suited for creating dynamic or interactive plots, for example, plotting a continuous time series of data. Kiwiplot achieves its speed by leveraging the fast pyqtgraph package, which is built directly on Qt. Kiwiplot offers a range of aesthetically pleaseing styling options and additional features such as data cursors, polar plots and constrained x or y zoom modes. The three graph styles are shown below: white, the default style, dark and grey.

Kiwiplot has not yet reached version 1.0. Expect breaking changes.


<img src="documentation/style_default.png" width="400" >
<img src="documentation/style_grey.png" width="400" >
<img src="documentation/style_dark.png" width="400" >


## Motivation
 Kiwiplot was developed to address the visual shortcomings of the pyqtgraph package and to add useful functionality such as data cursors. Although pyqtgraph is fast and robust, it lacks in the area of aesthetics and default styles. Kiwiplot addresses these limitations, allowing fast, interactive and aesthetically pleasing plots to be generated. 

## Why use Kiwiplot

**Compared to Matplotlib**
Matplotlib is a comprehensive plotting package that can generate production-quality graphs. However, for data streaming applications, animations and interactivity, it is far from ideal. Matplotlib is a behemoth and the update rate is slow, resulting in a laggy experience. 


**Compared to PyQtGraph**
PytQtGraph is a performant graphing library. Vanilla PyQt plots are not great looking and visual customization is limited.

## Example Use
Normal usage in a standalone application can be seen below. Further examples can be found in the `examples` directory.

```python
import sys
from kiwiplot import KiwiPlot
from kiwiplot.qtWrapper import QApplication
import numpy as np

if __name__ == '__main__':
    app = QApplication(sys.argv)
    fig = KiwiPlot(style='dark')
    fig.setWindowTitle('Style dark')
    t = np.linspace(0, 20e-3, 100)
    y1 = 2*np.sin(2*np.pi*50*t)
    y2 = 1.5*np.sin(2*np.pi*50*t)
    y3 = 1*np.sin(2*np.pi*50*t)
    fig.plot(t,y1, name='y1')
    fig.plot(t,y2, name='y2')
    fig.plot(t,y3, name='y3')
    fig.grid()
    fig.legend()
    sys.exit(app.exec_())
```

## IPython Support

Kiwiplot can be used from and IPython console or the Jupyter QtConsole as follows:

```python
%gui qt #typically necessary to integrate with the Qt GUI loop
from kiwiplot import KiwiPlot
fig = KiwiPlot()
t = np.linspace(0, 20e-3, 100)
y = 2*np.sin(2*np.pi*50*t)
fig.plot(t,y)
fig.grid()
fig.set_xlabel('Time (s)')
fig.set_ylabel('Amplitude (V)')
fig.set_title('Sine Wave')
fig1.setWindowTitle('Kiwiplot')
```

More information about the IPython (Jupyter) GUI event loop can be found [here](https://ipython.readthedocs.io/en/stable/config/eventloops.html). In general you will need to test your Python installation to see if the command `%gui qt` is necessary.

A discussion about integration of Jupyterlab with PyQtGraph is [here](https://github.com/pyqtgraph/pyqtgraph/issues/1963).


## Requirements
- Python 3.7+
- pyqtgraph 0.12+
- PySide2 or PyQt5
- numpy 1.17+


## Installing

```python
>>cd kiwiplot
>>python setup.py bdist_wheel
>>cd dist
>>pip install kiwiplot-x.y.z-py3-none-any.whl
```