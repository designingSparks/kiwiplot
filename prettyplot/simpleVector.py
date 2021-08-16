'''
Attempt to use GraphicsObject to create a custom item.
'''
from .qtWrapper import *
from pyqtgraph import GraphicsObject
from pyqtgraph.graphicsItems.GraphicsItem import GraphicsItem

TIP_DY = 0.1
TIP_DX = 0.2


class SimpleVector(GraphicsObject):

    def __init__(self, pen, length=1, tail=(0,0), angle=0, *args, **kwargs):
        '''
        :param
        tail - starting position of the vector tail
        '''
        super().__init__(*args, **kwargs)
        self.length = length
        self.tail = QPointF(0,0)
        if type(tail) is tuple:
            tail = QPointF(*tail)
        self.head = QPointF(length,0)
        self.length = length
        self.pen = pen
        self.pen.setJoinStyle(Qt.MiterJoin)
        self.generatePicture()
        self.setAngle(angle)
        self.setPos(tail)

    def generatePicture(self):
        self.picture = QPicture()
        p = QPainter(self.picture)
        p.setRenderHint(p.Antialiasing) #Is this necessary?
        p.setPen(self.pen)
        p.drawLine(self.tail, self.head)
        arrowhead = QPolygonF([QPointF(self.length-TIP_DX, TIP_DY), self.head, QPointF(self.length-TIP_DX, -TIP_DY)])
        p.drawPolyline(arrowhead)
        p.end()

    def paint(self, p, *args):
        p.drawPicture(0, 0, self.picture)

    def boundingRect(self):
        ## boundingRect _must_ indicate the entire area that will be drawn on
        ## or else we will get artifacts and possibly crashing.
        ## (in this case, QPicture does all the work of computing the bouning rect for us)
        return QRectF(self.picture.boundingRect())


    def setAngle(self, angle):
        """
        Takes angle argument in degrees.
        0 is horizontal; 90 is vertical.
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
