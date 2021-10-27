'''
Useful for drawing axis lines in polar plots that start from the origin.
Reference:
https://stackoverflow.com/questions/37702642/draw-half-infinite-lines
'''
import sys
from .qtWrapper import *
from pyqtgraph.graphicsItems.InfiniteLine import InfiniteLine
import pyqtgraph as pg
from pyqtgraph.Point import Point
from itertools import cycle
import numpy as np
from . import plotstyle
from .pplogger import *
logger = logging.getLogger('kiwiplot.' + __name__) 

class PolarLine(InfiniteLine):

    def __init__(self, *args, **kwargs):
        '''
        :param
        style - 'white', 'grey', 'dark'
        '''
        super().__init__(*args, **kwargs) 
        
    
    def paint(self, p, *args):
        p.setRenderHint(p.Antialiasing)
        
        left, right = self._endPoints
        pen = self.currentPen
        pen.setJoinStyle(Qt.MiterJoin)
        p.setPen(pen)
        point1 = Point(left, 0)
        point2 = Point(right, 0)
#         print(point1)
#         print(point2)
#         p.drawLine(Point(left, 0), Point(right, 0))
        p.drawLine(Point(0, 0), Point(right, 0))