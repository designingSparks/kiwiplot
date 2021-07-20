'''
Reference:
https://groups.google.com/g/pyqtgraph/c/U3AsIBvEirM/m/RdSRsZ-MAgAJ
https://stackoverflow.com/questions/29196610/qt-drawing-a-filled-rounded-rectangle-with-border
https://stackoverflow.com/questions/8366600/qt-opacity-color-brush
'''
from pyqtgraph import LegendItem, PlotDataItem, ScatterPlotItem, LabelItem
from pyqtgraph.Qt import QtCore, QtGui
from pyqtgraph.graphicsItems.ScatterPlotItem import drawSymbol
from pyqtgraph.graphicsItems.LegendItem import ItemSample
import pyqtgraph.functions as fn
from .qtWrapper import *


class myLegend(LegendItem):
    def __init__(self, size=None, offset=None):
        LegendItem.__init__(self, size, offset)

    #Can override paint to draw a custom legend rectangle
    def paint(self, p, *args):
        transRed = QColor(0xFF, 0, 0, 0) #the last parameter is the opacity
        pen = fn.mkPen({'color': transRed, 'width': 0})
        p.setPen(pen) # outline
        p.setBrush(fn.mkBrush('#808080'))   # background fill 

        p.setRenderHint(QPainter.Antialiasing)
        path = QPainterPath()
        rect = self.boundingRect()
        left, top, right, bottom = rect.getCoords()
        rect.setLeft(left + 0.5) #top left of bounding rectange is 0,0
        rect.setTop(top + 9.5)
        rect.setBottom(bottom - 9.5)
        rect.setRight(right-4.5)

        path.addRoundedRect(rect, 10, 10)
        # QPen pen(Qt::black, 10);
        # p.setPen(pen);
        # p.fillPath(path, Qt::red);
        # p.drawPath(path);
        p.drawPath(path)
        # p.drawRect(self.boundingRect())

    def addItem(self, item, name):
        """
        Add a new entry to the legend.

        ==============  ========================================================
        **Arguments:**
        item            A PlotDataItem from which the line and point style
                        of the item will be determined or an instance of
                        ItemSample (or a subclass), allowing the item display
                        to be customized.
        title           The title to display for this item. Simple HTML allowed.
        ==============  ========================================================
        """
        label = LabelItem(name, color=(0,0,0))
        if isinstance(item, ItemSample):
            sample = item
        else:
            sample = ItemSample(item)
        row = self.layout.rowCount()
        self.items.append((sample, label))
        self.layout.addItem(sample, row, 0)
        self.layout.addItem(label, row, 1)
        self.updateSize()