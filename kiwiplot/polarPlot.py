from .qtWrapper import *
from pyqtgraph.graphicsItems.PlotDataItem import PlotDataItem
from . import plotstyle
import pyqtgraph as pg
pg.setConfigOption('antialias', True) #Plotted curve looks nicer
from itertools import cycle
import numpy as np
from .polarLine import PolarLine
from .pplogger import get_logger
logger = get_logger( __name__) 

STYLES = ['white', 'grey', 'dark']


class PolarPlot(pg.PlotWidget):

    def __init__(self, style=None, nlines=None, *args, **kwargs):
        '''
        :param
        style - 'white', 'grey', 'dark'
        nlines - number of polar axis lines emanating from origin
        '''
        kwargs['background'] = None
        super().__init__(*args, **kwargs) #use custom viewbox
        self.plot_item = self.getPlotItem() #could use self.plotItem instead
        self.viewbox = self.plot_item.getViewBox()
        self.viewbox.sigResized.connect(self._resized_view_box)
        self.setAspectLocked() #important for polar plot to keep x:y ratio constant

        # self.viewbox.setMouseMode(pg.ViewBox.RectMode) #one button mode
        if style is None:
            self.set_style('white')
        else:
            self.set_style(style)

        #Draw axis lines, which emanate from the origin
        if nlines is not None:
            angles = np.arange(nlines)*360/nlines
            for a in angles:
                grid_color = QColor(self.graphstyle['grid'])
                axisline = PolarLine(angle=a, pen=grid_color)
                self.plot_item.addItem(axisline)
        
        self.linewidth = plotstyle.LINEWIDTH
        self.legend_box = None
        logger.debug('Initializing plot.')
        self.show()


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


    def set_graph_style(self, graphstyle):
        '''
        Sets the graph background and gridline color
        :param - style must be in STYLES
        '''
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


    @Slot(object)
    def _resized_view_box(self, view_box):
        self._background.setRect(self.plot_item.mapRectFromItem(view_box, view_box.rect()))


    def plot(self, x, y, color=None, linewidth=None, **kargs):

        if color is None:
            color = next(self.linecolor_sequence)
        if linewidth is None:
            linewidth = self.linewidth

        pen = pg.functions.mkPen({'color': color, 'width': linewidth})
        curve = self.plot_item.plot(x, y, pen=pen, **kargs)
        return curve


    def update_plot(self, index, x, y):
        try:
            self.plot_item.curves[index].setData(x, y)
        except Exception as ex:
            raise Exception(f'Could not update curve with index {index}')

    def xlim(self, xlim):
        '''
        Set the x limits of the plot.
        Parameters:
        xlim - a list with two values, e.g. [-1,1]
        '''
        self.viewbox.setXRange(*xlim) 

    def ylim(self, ylim):
        '''
        Set the y limits of the plot.
        Parameters:
        ylim - a list with two values, e.g. [-1,1]
        '''
        self.viewbox.setYRange(*ylim) 