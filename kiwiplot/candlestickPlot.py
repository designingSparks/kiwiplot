import sys
from .qtWrapper import *
from pyqtgraph.graphicsItems.PlotDataItem import PlotDataItem
from . import plotstyle
import pyqtgraph as pg
from kiwiplot import cursorLine
from itertools import cycle
import numpy as np
from .legend_box import LegendBox
from .cursorLine import CursorLine
from .ViewBox import ViewBox 
from kiwiplot.kiwiplot import kiwiplot
from .candlestickItem import CandlestickItem
from .pplogger import *
logger = get_logger(__name__) 


class CandlestickPlot(kiwiplot):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


    def plot(self, data):
        item = CandlestickItem(data, self.graphstyle['candlecolors'])
        self.plotItem.addItem(item)