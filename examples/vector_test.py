import pyqtgraph as pg
import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from prettyplot.simpleVector import SimpleVector
from pyqtgraph.graphicsItems.InfiniteLine import InfiniteLine
from pyqtgraph.Point import Point

TIP_DY = 0.1
TIP_DX = 0.2


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

if __name__ == '__main__':
    app = pg.mkQApp("Vanilla pyqtgraph")
    fig = pg.PlotWidget()
    vector1 = SimpleVector(pen='#ffffff')
    vector2 = SimpleVector(pen='#ffffff')
    vector2.setPos(QPointF(1,1))
    vector2.setAngle(45)
    fig.plotItem.addItem(vector1)
    fig.plotItem.addItem(vector2)
    fig.show()
    sys.exit(app.exec_())

