import os, sys
import sys
import numpy as np
from prettyplot import PrettyPlot, plotstyle
from prettyplot.qtWrapper import *
from prettyplot.candlestickPlot import CandlestickPlot
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
    fig1 = CandlestickPlot(style='dark')
    fig1.setWindowTitle('Candlestick example')
    fig1.plot(data)
    fig1.grid(False, True)
    sys.exit(app.exec_())
