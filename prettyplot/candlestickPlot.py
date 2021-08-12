import sys
from .qtWrapper import *
from pyqtgraph.graphicsItems.PlotDataItem import PlotDataItem
from . import plotstyle
import pyqtgraph as pg
from prettyplot import cursorLine
from itertools import cycle
import numpy as np
from .legend_box import LegendBox
from .cursorLine import CursorLine
from .ViewBox import ViewBox 
from prettyplot.prettyplot import PrettyPlot
from .candlestickItem import CandlestickItem
from .pplogger import *
logger = get_logger(__name__) 


class CandlestickPlot(PrettyPlot):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


    def plot(self, data):
        item = CandlestickItem(data, self.graphstyle['candlecolors'])
        self.plotItem.addItem(item)