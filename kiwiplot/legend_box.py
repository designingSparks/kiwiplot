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

    def addItem(self, item, text1):
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
        label = LabelItem(text1, color=(0,0,0), justify='right')
        # label2 = LabelItem(text2, color=(0,0,0), justify='right')
        if isinstance(item, ItemSample):
            sample = item
        else:
            sample = ItemSample(item)
        row = self.layout.rowCount()
        self.items.append((sample, label))
        self.layout.addItem(sample, row, 0)
        self.layout.addItem(label, row, 1)
        # self.layout.addItem(label2, row, 2)
        self.updateSize()


    def extend_label(self):
        '''
        Appends a label to each row of the legend box. Useful for displaying values that change with the cursor.
        '''
        for i, item_tuple in enumerate(self.items):
            label = LabelItem('', color=(0,0,0), justify='right')
            self.layout.addItem(label, i, 2)
            # item_tuple =  #extend the tuple
            self.items[i] = item_tuple + (label,)
        self.updateSize()


    def reduce_label(self):
        '''
        Removes the last label from each row of the legend box.
        '''
        for i, item_tuple in enumerate(self.items):
            item = item_tuple[-1]
            self.layout.removeItem(item)
            item.deleteLater()
            self.items[i] = item_tuple[:-1]

        self.updateSize()

    
    def update_legend_text(self, labels: list, pos=0):
        '''
        TODO: If labels[n] is None, don't update the label
        labels: list of the new text labels. It must have the same length as the number of legend box items.
        pos: label position. 0 = first label, 1 = second label
        TODO: Check that if pos > 0, then the legend box must have at least 2 labels
        '''
        n = len(self.items[0])
        # logger.debug('Number of text labels: %d', n-1)

        if pos >= (n - 1):
            raise ValueError('pos must be less than %d' % (n-2))

        for i, items in enumerate(self.items): #each item is a tuple of len 2
            single_item = items[pos+1] #add 
            if isinstance(single_item, graphicsItems.LabelItem.LabelItem):
                single_item.setText(labels[i]) #**plotstyle.legend_label_style) 
        self.updateSize()