import sys
import pyqtgraph as pg
import numpy as np
from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *

if __name__ == '__main__':
    app = pg.mkQApp("Vanilla pyqtgraph")
    fig = pg.PlotWidget()
    t = np.linspace(0, 20e-3, 100)
    y1 = 2*np.sin(2*np.pi*50*t)
    y2 = np.sin(2*np.pi*50*t)
    fig.addLegend() 
    fig.plot(t,y1, name='y1')
    fig.plot(t,y2, name='y2')
    fig.showGrid(True, True) #show x and y grids
    fig.show()
    sys.exit(app.exec_())