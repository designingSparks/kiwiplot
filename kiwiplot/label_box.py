'''
Derived from legend_box.py
'''
from pyqtgraph import LegendItem, PlotDataItem, ScatterPlotItem, LabelItem, graphicsItems
from pyqtgraph.Qt import QtCore, QtGui
from pyqtgraph import Point
from pyqtgraph.graphicsItems.ScatterPlotItem import drawSymbol
from pyqtgraph.graphicsItems.LegendItem import ItemSample
import pyqtgraph.functions as fn
from .qtWrapper import *

BACKGROUND_DEFAULT = '#808080'

class LabelBox(LegendItem):
    def __init__(self, size=None, offset=None, background=BACKGROUND_DEFAULT, isTight=True, fixed=True):
        # if isTight:
        #     offset -= 5
        LegendItem.__init__(self, size, offset)
        self.background = background
        self.fixed = fixed
        self.layoutTight = isTight


    #Can override paint to draw a custom legend rectangle
    def paint(self, p, *args):
        # transRed = QColor(0xFF, 0, 0, 0) #the last parameter is the opacity. 0 = opaque, 255 = solid
        # pen = fn.mkPen({'color': transRed, 'width': 0}) #outline
        midGrey = QColor(0xCC, 0xCC, 0xCC, 127)
        pen = fn.mkPen({'color': midGrey, 'width': 1.5}) #outline
        p.setPen(pen) # outline
        background_color = QColor(0xFF, 0xFF, 0xFF, 170) #Last value is transparency. 170 = 2/3
        # p.setBrush(fn.mkBrush('#808080'))   # background fill 
        p.setBrush(background_color)   # background fill 

        p.setRenderHint(QPainter.Antialiasing)
        path = QPainterPath()
        rect = self.boundingRect()

        if self.layoutTight: #Tightens the bounding box of the text
            left, top, right, bottom = rect.getCoords()
            rect.setLeft(left + 5) #top left of bounding rectange is 0,0
            rect.setTop(top + 5)
            rect.setBottom(bottom - 5)
            rect.setRight(right-5)
            # self.shift(5, 5)

        path.addRoundedRect(rect, 8, 8)
        # QPen pen(Qt::black, 10);
        # p.setPen(pen);
        # p.fillPath(path, Qt::red);
        # p.drawPath(path);
        p.drawPath(path)
        # p.drawRect(self.boundingRect())


    def hoverEvent(self, ev):
        '''Only need to accept if you want to drag the label box'''
        pass


    def mouseDragEvent(self, ev):
        '''Prevent the label box from being dragged'''
        ev.ignore()

    def shift(self, dx, dy):
        '''
        Shifts the label box by dx, dy
        '''
        self.setPos(self.pos() + Point(dx, dy))


    def addText(self, text):
        label = LabelItem(text, color=(0,0,0), justify='center', bold=True)
        row = 0
        self.layout.addItem(label, row, 0)
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
        '''
        n = len(self.items[0])
        if pos >= (n - 1):
            raise ValueError('pos must be less than %d' % (n-2))

        for i, items in enumerate(self.items): #each item is a tuple of len 2
            single_item = items[pos+1] #add 
            if isinstance(single_item, graphicsItems.LabelItem.LabelItem):
                single_item.setText(labels[i]) #**plotstyle.legend_label_style) 
        self.updateSize()
    

    def remove_all_items(self):
        '''
        Removes all items from the legend.
        '''
        while self.items:
            item = self.items.pop()
            for subitem in item:
                self.layout.removeItem(subitem)
                subitem.deleteLater()
        
        self.updateSize()