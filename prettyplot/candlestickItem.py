"""
Demonstrate creation of a custom graphic (a candlestick plot)
"""
from .qtWrapper import *
import pyqtgraph as pg

## Create a subclass of GraphicsObject.
## The only required methods are paint() and boundingRect() 
## (see QGraphicsItem documentation)
class CandlestickItem(pg.GraphicsObject):
    def __init__(self, data, colors):
        pg.GraphicsObject.__init__(self)
        self.data = data  ## data must have fields: time, open, close, min, max
        self.green = colors[0]
        self.red = colors[1]
        self.generatePicture()
    
    def generatePicture(self):
        ## pre-computing a QPicture object allows paint() to run much more quickly, 
        ## rather than re-drawing the shapes every time.
        self.picture = QPicture()
        p = QPainter(self.picture)
        w = (self.data[1][0] - self.data[0][0]) / 3.
        for (t, open, close, min, max) in self.data:
            if open > close:
                p.setPen(pg.mkPen(self.red, width=2))
                p.setBrush(pg.mkBrush(self.red))
            else:
                p.setPen(pg.mkPen(self.green, width=2))
                p.setBrush(pg.mkBrush(self.green))
            p.drawLine(QPointF(t, min), QPointF(t, max))
            p.drawRect(QRectF(t-w, open, w*2, close-open))
        p.end()
    
    def paint(self, p, *args):
        p.drawPicture(0, 0, self.picture)
    
    def boundingRect(self):
        ## boundingRect _must_ indicate the entire area that will be drawn on
        ## or else we will get artifacts and possibly crashing.
        ## (in this case, QPicture does all the work of computing the bouning rect for us)
        return QRectF(self.picture.boundingRect())