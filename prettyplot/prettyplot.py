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
from .legend_box import LegendBox
from .pplogger import *
from .cursorLine import CursorLine

logger = logging.getLogger('prettyplot.' + __name__) 

STYLES = ['white', 'grey', 'dark']

# _Q_APP = None # Keep reference to QApplication instance to prevent garbage collection
# qApp = QApplication.instance()
# if qApp is None:
#     _Q_APP = qApp = QApplication([])
    

# def qApplicationSingleton():
#     global _Q_APP
#     qApp = QApplication.instance()
#     if qApp is None:
#         _Q_APP = qApp = QApplication([])
#     return qApp
# qApplicationSingleton()

def find_nearest(array, value):
    array = np.asarray(array)
    idx = (np.abs(array - value)).argmin()
    return array[idx]

class PrettyPlot(pg.PlotWidget):
    
    cursorDataSignal = Signal(object)

    def __init__(self, style=None, *args, **kwargs):
        '''
        :param
        style - 'white', 'grey', 'dark'
        '''
        kwargs['background'] = None
        super().__init__(*args, **kwargs)
        self.plot_item = self.getPlotItem()
        # self.plot_item.showGrid(x=True, y=True, alpha=1)

        self.viewbox = self.plot_item.getViewBox()
        self.viewbox.sigResized.connect(self._resized_view_box)
        # self.viewbox.setMouseMode(pg.ViewBox.RectMode) #one button mode
        # self.viewbox.setZoomMode(pg.ViewBox.xZoom)
        
        #TODO: if style is a text arguement, set the palette to plotstyle.grey and linecolor to ...
        #TODO: change set_palette to set_linecolors, self.palette to self.linecolors
        # self.set_palette(plotstyle.palette_1)

        if style is None:
            self.set_style('white')
        else:
            self.set_style(style)

        self.linewidth = plotstyle.LINEWIDTH
        self.cursor = None
        # self.curves = list() #Not needed. Use self.plot_item.curves()
        self.legend_box = None
        logger.debug('Initializing plot.')
        self.show()
        self.cursor_dots = list() #store dots that show the intersection of the cursor and graph

    # @property
    # def qApplication(self):
    #     """ Returns the QApplication object. Equivalent to QtWidgets.qApp.
    #         :rtype QtWidgets.QApplication:
    #     """
    #     # TODO: replace the lines below by qApplicationSingleton()
    #     global _Q_APP

    #     qApp = QApplication.instance()
    #     if qApp is None:
    #         _Q_APP = qApp = QApplication([])
    #     return qApp


    def set_style(self, style):
        '''
        '''
        if style not in STYLES:
            raise ValueError('style must be in: {}'.format(STYLES))
        if style == 'white':
            self.set_graph_style(plotstyle.style_white)
        elif style == 'grey':
            self.set_graph_style(plotstyle.style_grey)
        elif style == 'dark':
            self.set_graph_style(plotstyle.style_dark)


    def grid(self, *args):
        '''
        Enables/disables the x and y grids.

        :param
        args[0] - bool. Enables or disables both x and y grids
        args[0], args[1] - bool. Separately enable/disable x and y grids
        '''
        xGrid = yGrid = True
        if len(args) == 1:
            xGrid = yGrid = args[0]
        elif len(args) == 2:
            xGrid = args[0]
            yGrid = args[1]
        self.plot_item.showGrid(x=xGrid, y=yGrid, alpha=1)


    def legend(self, legend_list=None, offset=(-20,20)):
        '''
        Show the legend box
        '''
        #Create legend box
        if self.legend_box is None:
            self.legend_box = LegendBox(offset=offset)
            self.legend_box.setParentItem(self.graphicsItem())
            # self.legend.setParentItem(self.viewbox) #also works

        #If no curves exist, use the default palette to define the curves
        #Note that the yaxis width is incorrect until self.plot() has been called
        if len(self.plot_item.curves) == 0:
            linecolor_cycle = cycle(self.palette)
            for name in legend_list:
                pen = pg.functions.mkPen({'color': next(linecolor_cycle), 'width': self.linewidth})
                item = PlotDataItem()
                item.setPen(pen)
                self.legend_box.addItem(item, name)
            return

        if legend_list is not None:
            for i, name in enumerate(legend_list):
                self.legend_box.addItem(self.plot_item.curves[i], name)
            return

        #Curve names were defined during plotting
        if legend_list is None: 
            logger.debug('Creating legend using name property')
            for curve in self.plot_item.curves: #Use default names
                name = curve.name()
                if name is None:
                    name = ''
                self.legend_box.addItem(curve, name)
            return
        


    def set_graph_style(self, graphstyle):
        '''
        Sets the graph background and gridline color
        :param - style must be in STYLES
        '''
        # if style is None:
        #     self.style = plotstyle.style_white
        # else:
        #     self.style = style
        self.graphstyle = graphstyle

        #Background color
        self._background = QGraphicsRectItem(self.viewbox.rect())
        self._background.setParentItem(self.plot_item)
        self._background.setZValue(-1e6)
        self._background.setFlags(QGraphicsItem.ItemNegativeZStacksBehindParent)
        self._background.setPen(QPen())
        background_color = QColor(self.graphstyle['background'])
        self._background.setBrush(background_color)
        self._background.setRect(self.plot_item.mapRectFromItem(self.viewbox, self.viewbox.rect())) #manual resize to show background correctly

        #Needed to ensure y axis are aligned
        self.plot_item.getAxis('left').setWidth(plotstyle.YAXIS_WIDTH) 
        # self.plot_item.getAxis('left').setWidth(50) 

        #Changes the gridline color
        col = QColor(self.graphstyle['grid'])
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
            axis.setTextPen(self.graphstyle['text']) #sets text color

        #Needed to hide the top & right axis border. Otherwise this is rendered in black
        self.showAxis('top')
        self.showAxis('right')
        self.getAxis('top').setStyle(tickLength=0, showValues=False)
        self.getAxis('right').setStyle(tickLength=0, showValues=False)
        self.set_linecolors(graphstyle['linecolors'])


    def set_linecolors(self, palette):
        '''
        :param
        palette - a list of color strings. See plotsyle.py for examples.
        '''
        self.linecolors = palette
        self.linecolor_sequence = cycle(self.linecolors)


    # def _get_pen(self):
    #     '''
    #     Creates a pen based on the next color in the chosen linecolor palette.
    #     '''
    #     color = next(self.linecolor_sequence)
    #     pen = pg.functions.mkPen({'color': color, 'width': self.linewidth})
    #     return pen, color

    @Slot(object)
    def _resized_view_box(self, view_box):
        # plot_item = self.getPlotItem()
        self._background.setRect(self.plot_item.mapRectFromItem(view_box, view_box.rect()))


    def plot(self, x, y, color=None, linewidth=None, **kargs):

        if color is None:
            color = next(self.linecolor_sequence)
        if linewidth is None:
            linewidth = self.linewidth

        #TODO: Add try except
        pen = pg.functions.mkPen({'color': color, 'width': linewidth})
        curve = self.plot_item.plot(x, y, pen=pen, **kargs)
        cursor_dot = pg.ScatterPlotItem(size=plotstyle.CURSORDOTSIZE, pen=pen, brush=color)
        self.cursor_dots.append(cursor_dot)
        # self.curves.append(curve)
        # self.viewbox.initZoomStack() #reset zoom stack
        return curve


    def update_curve(self, index, x, y):
        try:
            self.curves[index].setData(x, y)
        except Exception as ex:
            raise Exception(f'Could not update curve with index {index}')


    def show_cursor(self):

        if len(self.plot_item.curves) == 0:
            return

        if self.cursor is None:
            mypen = pg.functions.mkPen({'color': self.graphstyle['cursor'], 'width': plotstyle.CURSORWIDTH})  #white
            self.cursor = CursorLine(angle=90, movable=True, pen=mypen) #http://www.pyqtgraph.org/downloads/0.10.0/pyqtgraph-0.10.0-deb/pyqtgraph-0.10.0/examples/crosshair.py
            self.cursor.sigPositionChanged.connect(self.update_cursor)
            # self.cursor_x = 0

            #Cursor initial position is midway on the x axis
            #TODO - change this to midway on the viewbox
            curve = self.plot_item.curves[0] #use first line as reference
            # idx = int(len(curve.xData)/2)
            # xval = curve.xData[idx]
            left = self.viewbox.viewRange()[0][0]
            right = self.viewbox.viewRange()[0][1]
            mid = np.average([left, right])
            idx = (np.abs(curve.xData - mid)).argmin()
            xval = curve.xData[idx]
            self.plot_item.addItem(self.cursor, ignoreBounds=True)
            self.cursor.setPos(pg.Point(xval,0))
            self.cursor.setXDataLimit([curve.xData[0], curve.xData[-1]])

            #Show the cursor dots
            for i, cursor_dot in enumerate(self.cursor_dots):
                curve = self.plot_item.curves[i]
                yval = curve.yData[idx] #find_nearest(curve.xData, xval)
                self.plot_item.addItem(cursor_dot, ignoreBounds=True)
                cursor_dot.setData([xval], [yval])
                self.plot_item.curves.pop() #Don't store the cursor dots in the curves list as these are stored in self.cursor_dots

        else:
            logger.debug('Cursor already created')

    @Slot(object)
    def update_cursor(self, line):
        '''
        Called when the cursor was moved
        Params
        line - pyqtgraph InfiniteLine type
        '''
        xpos = line.x()
        # logger.debug('xpos: {}'.format(xpos))

        xlist = list()
        ylist = list()

        #Update cursor dots
        for i, curve in enumerate(self.plot_item.curves):
            idx = (np.abs(curve.xData - xpos)).argmin()
            xval = curve.xData[idx]
            yval = curve.yData[idx]
            xlist.append(xval)
            ylist.append(yval)
            # logger.debug(f'idx{idx}')
            self.cursor_dots[i].setData([xval], [yval])

        self.cursorDataSignal.emit((xlist, ylist))

    # def show_cursor(self):
    #     self.plot_item.addItem(self.cursor, ignoreBounds=True)
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