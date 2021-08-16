'''
Attempt to use GraphicsObject to create a custom item.
'''
from .qtWrapper import *
from pyqtgraph.graphicsItems.InfiniteLine import InfiniteLine
from pyqtgraph.Point import Point
from pyqtgraph import GraphicsObject
import pyqtgraph.functions as fn
from pyqtgraph.graphicsItems.GraphicsItem import GraphicsItem

TIP_DY = 0.1
TIP_DX = 0.2


class DebugVector(GraphicsObject):

    def __init__(self, length=1, tail=(0,0), angle=0, *args, **kwargs):
        '''
        :param
        tail - starting position of the vector tail
        '''
        super().__init__(*args, **kwargs)
        self.length = length
        if type(tail) is tuple:
            tail = QPointF(*tail)
        self.tail = tail
        self.head = QPointF(length,0)
        self.length = length
        # self.setAngle(angle)
        # self.setPos(tail)
        self.generatePicture()

    def generatePicture(self):
        self.picture = QPicture()
        p = QPainter(self.picture)
        p.setRenderHint(p.Antialiasing)
        # pen = self.currentPen
        # pen = QPen('#ffffff')
        pen = fn.mkPen({'color': '#FFFFFF', 'width': 1.5}) #outline
        pen.setJoinStyle(Qt.MiterJoin)
        p.setPen(pen)
        p.drawLine(QPointF(0,0), self.head)
        arrowhead = QPolygonF([Point(self.length-TIP_DX, TIP_DY), self.head, Point(self.length-TIP_DX, -TIP_DY)])
        p.drawPolyline(arrowhead)
        p.end()

    def paint(self, p, *args):
        p.drawPicture(0, 0, self.picture)
        # p.setRenderHint(p.Antialiasing)
        # pen = self.currentPen
        # pen.setJoinStyle(Qt.MiterJoin)
        # p.setPen(pen)
        # p.drawLine(QPointF(0,0), self.head)
        # arrowhead = QPolygonF([Point(self.length-TIP_DX, TIP_DY), self.head, Point(self.length-TIP_DX, -TIP_DY)])
        # p.drawPolyline(arrowhead)

    def boundingRect(self):
        ## boundingRect _must_ indicate the entire area that will be drawn on
        ## or else we will get artifacts and possibly crashing.
        ## (in this case, QPicture does all the work of computing the bouning rect for us)
        return QRectF(self.picture.boundingRect())


    def setAngle(self, angle):
        """
        Takes angle argument in degrees.
        0 is horizontal; 90 is vertical.

        Note that the use of value() and setValue() changes if the line is
        not vertical or horizontal.
        """
        self.angle = angle #((angle+45) % 180) - 45   ##  -45 <= angle < 135
        self.resetTransform()
        self.setRotation(self.angle)
        self.update()

    def setPos(self, pos):
        '''
        pos - new tail point
        '''
        if type(pos) is tuple:
            pos = QPointF(*pos)
        if self.tail != pos:
            self.tail = pos
            self.viewTransformChanged()
            GraphicsObject.setPos(self, pos)

    def viewTransformChanged(self):
        """
        Called whenever the transformation matrix of the view has changed.
        (eg, the view range has changed or the view was resized)
        """
        self._boundingRect = None
        GraphicsItem.viewTransformChanged(self)
