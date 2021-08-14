'''
Useful for drawing simple vectors
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
logger = logging.getLogger('prettyplot.' + __name__) 

TIP_DY = 0.1
TIP_DX = 0.2

#TODO: Change the linewidth
#How to autoscale the view

class SimpleVector(InfiniteLine):

    def __init__(self, length=1, tail=(0,0), angle=0, *args, **kwargs):
        '''
        :param
        tail - starting position of the vector tail
        '''
        super().__init__(*args, **kwargs)
        self.length = length
        if type(tail) is tuple:
            tail = QPointF(*tail)
        self.head = QPointF(length,0)
        self.length = length
        self.setAngle(angle)
        self.setPos(tail)

    def paint(self, p, *args):
        p.setRenderHint(p.Antialiasing)
        pen = self.currentPen
        pen.setJoinStyle(Qt.MiterJoin)
        p.setPen(pen)
        p.drawLine(QPointF(0,0), self.head)
        arrowhead = QPolygonF([Point(self.length-TIP_DX, TIP_DY), self.head, Point(self.length-TIP_DX, -TIP_DY)])
        p.drawPolyline(arrowhead)