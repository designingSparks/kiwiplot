'''
Useful for setting the background color of the viewbox:
https://github.com/pyqtgraph/pyqtgraph/issues/1190

Example:
self.plotwidget = PlotWidget()
vbox = QVBoxLayout()
widget = QWidget()
vbox.addWidget(self.plotwidget)
widget.setLayout(vbox)
self.setCentralWidget(widget)
self.show()
'''
import sys
# import os
# os.environ['QT_API'] = 'PYQT5'
from .qtWrapper import *
from pyqtgraph.graphicsItems.PlotDataItem import PlotDataItem
from . import plotstyle
import pyqtgraph as pg
pg.setConfigOption('antialias', True) #Plotted curve looks nicer
from itertools import cycle
import numpy as np
from .mylegend import myLegend
from .pplogger import *
logger = logging.getLogger('prettyplot.' + __name__) 

class PrettyPlot(pg.PlotWidget):
    
    def __init__(self, style=None, linecolors=None, *args, **kwargs):
        kwargs['background'] = None
        super().__init__(*args, **kwargs)
        self.plot_item = self.getPlotItem()
        self.plot_item.showGrid(x=True, y=True, alpha=1)

        self.viewbox = self.plot_item.getViewBox()
        self.viewbox.sigResized.connect(self._resized_view_box)
        # self.viewbox.setMouseMode(pg.ViewBox.RectMode) #one button mode
        # self.viewbox.setZoomMode(pg.ViewBox.xZoom)
        
        #TODO: if style is a text arguement, set the palette to plotstyle.grey and linecolor to ...
        #TODO: change set_palette to set_linecolors, self.palette to self.linecolors
        self.linewidth = plotstyle.LINEWIDTH
        self.set_palette(plotstyle.palette_1)
        self.set_graph_style(style)
        self.show()
        self.cursor = None
        # self.curves = list() #Not needed. Use self.plot_item.curves()
        self.legend = None
        logger.debug('Initializing plot.')

    def show_legend(self, legend_list=None, offset=(-20,20)):

        #Create legend box
        if self.legend is None:
            self.legend = myLegend(offset=offset)
            self.legend.setParentItem(self.graphicsItem())
            # self.legend.setParentItem(self.viewbox) #also works

        #If no curves exist, use the default palette to define the curves
        #Note that the yaxis width is incorrect until self.plot() has been called
        if len(self.plot_item.curves) == 0:
            linecolor_cycle = cycle(self.palette)
            for name in legend_list:
                pen = pg.functions.mkPen({'color': next(linecolor_cycle), 'width': self.linewidth})
                item = PlotDataItem()
                item.setPen(pen)
                self.legend.addItem(item, name)
            return

        if legend_list is not None:
            for i, name in enumerate(legend_list):
                self.legend.addItem(self.plot_item.curves[i], name)
            return

        #Curve names were defined during plotting
        if legend_list is None: 
            logger.debug('Creating legend using name property')
            for curve in self.plot_item.curves: #Use default names
                name = curve.name()
                if name is None:
                    name = ''
                self.legend.addItem(curve, name)
            return
        


    def set_graph_style(self, style=None):
        '''
        Sets the graph background and gridline color
        '''
        if style is None:
            self.style = plotstyle.style_white
        else:
            self.style = style

        #Background color
        self._background = QGraphicsRectItem(self.viewbox.rect())
        self._background.setParentItem(self.plot_item)
        self._background.setZValue(-1e6)
        self._background.setFlags(QGraphicsItem.ItemNegativeZStacksBehindParent)
        self._background.setPen(QPen())
        background_color = QColor(self.style['background'])
        self._background.setBrush(background_color)
        self._background.setRect(self.plot_item.mapRectFromItem(self.viewbox, self.viewbox.rect())) #manual resize to show background correctly

        #Needed to ensure y axis are aligned
        self.plot_item.getAxis('left').setWidth(plotstyle.YAXIS_WIDTH) 
        # self.plot_item.getAxis('left').setWidth(50) 

        #Changes the gridline color
        col = QColor(self.style['grid'])
        axis_pen = QPen(col)
        for ax in ('top', 'left', 'right', 'bottom'):
            axis = self.plot_item.getAxis(ax)
            axis.setPen(axis_pen)

        #Sets the font and color of the bottom & left axis units otherwise the text has
        #the same color as the gridlines
        font = QFont("Arial", 9)
        # font = QFont("Helvetica [Cronyx]", 9)
        keys = ['bottom', 'left']
        for k in keys:
            axis = self.plot_item.getAxis(k)
            axis.setTickFont(font)
            axis.setTextPen(self.style['text']) #sets text color

        #Needed to hide the top & right axis border. Otherwise this is rendered in black
        self.showAxis('top')
        self.showAxis('right')
        self.getAxis('top').setStyle(tickLength=0, showValues=False)
        self.getAxis('right').setStyle(tickLength=0, showValues=False)


    def set_palette(self, palette):
        self.palette = palette
        self.linecolor_cycle = cycle(self.palette)


    def _get_pen(self):
        '''
        Creates a pen based on the next color in the chosen linecolor palette.
        '''
        pen = pg.functions.mkPen({'color': next(self.linecolor_cycle), 'width': self.linewidth})
        return pen

    # @pyqtSlot(object)
    def _resized_view_box(self, view_box):
        # plot_item = self.getPlotItem()
        self._background.setRect(self.plot_item.mapRectFromItem(view_box, view_box.rect()))


    def plot(self, x, y, pen=None, **kargs):
        if pen is None:
            pen = self._get_pen()
        curve = self.plot_item.plot(x, y, pen=pen, **kargs)
        # self.curves.append(curve)
        # self.viewbox.initZoomStack() #reset zoom stack
        return curve


    def update_curve(self, index, x, y):
        try:
            self.curves[index].setData(x, y)
        except Exception as ex:
            raise Exception(f'Could not update curve with index {index}')


    def create_cursor(self, callback=None):

        if self.cursor is None:
            mypen = pg.functions.mkPen({'color': self.style['cursor'], 'width': plotstyle.CURSORWIDTH})  #white
            self.cursor = pg.InfiniteLine(angle=90, movable=True, pen=mypen) #http://www.pyqtgraph.org/downloads/0.10.0/pyqtgraph-0.10.0-deb/pyqtgraph-0.10.0/examples/crosshair.py
            if callback is not None:
                self.cursor.sigPositionChanged.connect(callback)
            self.cursor_x = 0
        else:
            logger.debug('Cursor already created')


    def show_cursor(self):
        self.plot_item.addItem(self.cursor, ignoreBounds=True)
        #Get the current viewbox limits
        # left = self.viewbox.viewRange()[0][0]
        # right = self.viewbox.viewRange()[0][1]
        # middle = np.average([left, right])
        # self.plot_item.addItem(self.cursor, ignoreBounds=True)
        # self.myplot.addItem(self.plotHighlight, ignoreBounds=True)
        
        
        # idx = (np.abs(self.xdata - middle)).argmin()
        # xpos = self.xdata[idx]
        # self.cursor.setPos(pg.Point(xpos,0))
        # self.updatePlotHighlight(middle)

    def hide_cursor(self):
        self.plot_item.removeItem(self.cursor)

    def set_xlabel(self, label):
        self.plot_item.setLabel('bottom', label, **plotstyle.label_style)
    
    def set_ylabel(self, label):
        self.plot_item.setLabel('left', label, **plotstyle.label_style)
    
    def set_title(self, text):
        self.plot_item.setTitle(text, **plotstyle.label_style)

    # def enable_legend(self, xpos, ypos, padding=10):
    #     '''
    #     Parameters:
    #     xpos, ypos = 'left', 'right', 'top', 'bottom'
    #     padding - distance in pixels from plot edge
    #     '''
    #     #TODO:
    #     if xpos not in ['left', 'right']:
    #         raise ValueError('xpos incorrect')
    #     if ypos not in ['top', 'bottom']:
    #         raise ValueError('ypos incorrect')

    #     x = padding
    #     y = padding
    #     if xpos == 'right':
    #         x = -x
    #     if ypos == 'bottom':
    #         y = -y
    #     self.plot_item.addLegend(offset=(x,y))


    def update_legend_text(self):
        '''
        '''
        for item in self.plot_item.legend.items:
            for single_item in item:
                if isinstance(single_item, pg.graphicsItems.LabelItem.LabelItem):
                    single_item.setText(single_item.text, **plotstyle.legend_label_style) 


if __name__ == '__main__':
    app = QApplication(sys.argv)
    fig = PrettyPlot()
    import numpy as np
    t = np.linspace(0, 20e-3, 100)
    y1 = 2*np.sin(2*np.pi*50*t)
    fig.plot(t,y1, name='y1')
    sys.exit(app.exec_())