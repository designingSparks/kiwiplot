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

class SimpleVector(InfiniteLine):

    def __init__(self, head=(1,0), tail=(0,0),*args, **kwargs):
        '''
        :param
        style - 'white', 'grey', 'dark'
        '''
        super().__init__(*args, **kwargs)
        self.head = QPointF(*head)
        self.tail = QPointF(*tail)
    

    # def arrowCalc(self, start_point=None, end_point=None):  # calculates the point where the arrow should be drawn

    #     try:
    #         startPoint, endPoint = start_point, end_point

    #         if start_point is None:
    #             startPoint = self._sourcePoint

    #         if endPoint is None:
    #             endPoint = self._destinationPoint

    #         dx, dy = startPoint.x() - endPoint.x(), startPoint.y() - endPoint.y()

    #         leng = np.sqrt(dx ** 2 + dy ** 2)
    #         normX, normY = dx / leng, dy / leng  # normalize

    #         # perpendicular vector
    #         perpX = -normY
    #         perpY = normX
    #         leftX = endPoint.x() + self._arrow_height * normX + self._arrow_width * perpX
    #         leftY = endPoint.y() + self._arrow_height * normY + self._arrow_width * perpY
    #         rightX = endPoint.x() + self._arrow_height * normX - self._arrow_height * perpX
    #         rightY = endPoint.y() + self._arrow_height * normY - self._arrow_width * perpY
    #         point2 = QPointF(leftX, leftY)
    #         point3 = QPointF(rightX, rightY)
    #         return QPolygonF([point2, endPoint, point3])
    #     except (ZeroDivisionError, Exception):
    #         return None

    # def directPath(self, point1, point2):
    #     path = QPainterPath(point1)
    #     path.lineTo(point2)
    #     return path

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
        p.drawLine(self.tail, self.head)
        arrowhead = QPolygonF([Point(0.8, 0.1), Point(1, 0), Point(0.8, -0.1)])
        p.drawPolyline(arrowhead)

        # path = self.directPath(point1, point2)
        # triangle_source = self.arrowCalc(path.pointAtPercent(0.1), Point(1, 0))  # change path.PointAtPercent() value to move arrow on the line
        # if triangle_source is not None:
        #     p.drawPolyline(triangle_source)