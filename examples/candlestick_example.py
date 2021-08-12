import os, sys
import sys
import numpy as np
from prettyplot import PrettyPlot, plotstyle
from prettyplot.qtWrapper import *
from prettyplot.candlestickItem import CandlestickItem
import pyqtgraph as pg #must come after importing prettyplot.qt


data = [  ## fields are (time, open, close, min, max).
    (1., 10, 13, 5, 15),
    (2., 13, 17, 9, 20),
    (3., 17, 14, 11, 23),
    (4., 14, 15, 5, 19),
    (5., 15, 9, 8, 22),
    (6., 9, 15, 8, 16),
]


if __name__ == '__main__':
    app = QApplication(sys.argv)
    fig1 = PrettyPlot(style='dark')
    fig1.setWindowTitle('Candlestick example')
    item = CandlestickItem(data)
    fig1.plotItem.addItem(item)
    sys.exit(app.exec_())
