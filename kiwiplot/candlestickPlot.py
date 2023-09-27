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
from kiwiplot import KiwiPlot
from .candlestickItem import CandlestickItem
from .klog import *
logger = get_logger(__name__) 


class CandlestickPlot(KiwiPlot):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


    def plot(self, data):
        item = CandlestickItem(data, self.graphstyle['candlecolors'])
        logger.debug('Plotting candlestick')
        self.plotItem.addItem(item)