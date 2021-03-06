'''
Reference:
https://groups.google.com/g/pyqtgraph/c/U3AsIBvEirM/m/RdSRsZ-MAgAJ
https://stackoverflow.com/questions/29196610/qt-drawing-a-filled-rounded-rectangle-with-border
https://stackoverflow.com/questions/8366600/qt-opacity-color-brush
'''
from pyqtgraph import LegendItem, PlotDataItem, ScatterPlotItem, LabelItem, graphicsItems
from pyqtgraph.Qt import QtCore, QtGui
from pyqtgraph.graphicsItems.ScatterPlotItem import drawSymbol
from pyqtgraph.graphicsItems.LegendItem import ItemSample
import pyqtgraph.functions as fn
from .qtWrapper import *

BACKGROUND_DEFAULT = '#808080'

class LegendBox(LegendItem):
    def __init__(self, size=None, offset=None, background=BACKGROUND_DEFAULT):
        LegendItem.__init__(self, size, offset)
        self.background = background


    #Can override paint to draw a custom legend rectangle
    def paint(self, p, *args):
        # transRed = QColor(0xFF, 0, 0, 0) #the last parameter is the opacity. 0 = opaque, 255 = solid
        # pen = fn.mkPen({'color': transRed, 'width': 0}) #outline
        midGrey = QColor(0xCC, 0xCC, 0xCC, 127)
        pen = fn.mkPen({'color': midGrey, 'width': 1.5}) #outline
        p.setPen(pen) # outline
        background_color = QColor(0xFF, 0xFF, 0xFF, 64)
        # p.setBrush(fn.mkBrush('#808080'))   # background fill 
        p.setBrush(background_color)   # background fill 

        p.setRenderHint(QPainter.Antialiasing)
        path = QPainterPath()
        rect = self.boundingRect()
        left, top, right, bottom = rect.getCoords()
        rect.setLeft(left + 0.5) #top left of bounding rectange is 0,0
        rect.setTop(top + 9.5)
        rect.setBottom(bottom - 9.5)
        rect.setRight(right-4.5)

        path.addRoundedRect(rect, 8, 8)
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
        label = LabelItem(name, color=(0,0,0), justify='left')
        if isinstance(item, ItemSample):
            sample = item
        else:
            sample = ItemSample(item)
        row = self.layout.rowCount()
        self.items.append((sample, label))
        self.layout.addItem(sample, row, 0)
        self.layout.addItem(label, row, 1)
        self.updateSize()

    
    def update_legend_text(self, labels: list):
        '''
        TODO: If labels[n] is None, don't update the label
        labels: list of the new text labels. It must have the same length as the number of legend box items.
        '''
        for i, item in enumerate(self.items): #each item is a tuple of len 2
            for single_item in item:
                if isinstance(single_item, graphicsItems.LabelItem.LabelItem):
                    single_item.setText(labels[i]) #, **plotstyle.legend_label_style) 