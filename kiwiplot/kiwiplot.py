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
from os import times
import sys
# import os
# os.environ['QT_API'] = 'PYQT5'
from .qtWrapper import *
from pyqtgraph.graphicsItems.PlotDataItem import PlotDataItem
from pyqtgraph.graphicsItems.GridItem import GridItem
from . import plotstyle
import pyqtgraph as pg

from kiwiplot import cursorLine
from kiwiplot.plotstyle import *
pg.setConfigOption('antialias', True) #Plotted curve looks nicer
from itertools import cycle
import numpy as np
from .legend_box import LegendBox
from .label_box import LabelBox
# from .cursorLine import CursorLine
from .cursorLine2 import CursorLine2 as CursorLine
# from pyqtgraph.graphicsItems.ViewBox import ViewBox
from .ViewBox2 import ViewBox2 #js
from .klog import get_logger
logger = get_logger('kiwiplot.' + __name__)
STYLES = ['white', 'grey', 'dark']

from .constants import IMAGE_DIR

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


class KiwiPlot(pg.PlotWidget):
    
    # cursorDataSignal = Signal(object)

    def __init__(self, style=None, *args, **kwargs):
        '''
        :param
        style - 'white', 'grey', 'dark'
        '''
        kwargs['background'] = None
        super().__init__(viewBox = ViewBox2(), *args, **kwargs) #use custom viewbox
        self.plot_item = self.getPlotItem()
        self.viewbox = self.plot_item.getViewBox()
        self.viewbox.sigResized.connect(self._resized_view_box)
        self.viewbox.setMouseMode(pg.ViewBox.RectMode) #one button mode
        # self.viewbox.setZoomMode(pg.ViewBox.xZoom)
        
        #TODO: if style is a text arguement, set the palette to plotstyle.grey and linecolor to ...
        #TODO: change set_palette to set_linecolors, self.palette to self.linecolors
        # self.set_palette(plotstyle.palette_1)

        if style is None:
            self.set_style('white')
        else:
            self.set_style(style)

        self.linewidth = plotstyle.LINEWIDTH
        self.cursor = None #reference to last cursor
        # self.cursor_list = list() #can have multiple cursors
        # self.curves = list() #Not needed. Use self.plot_item.curves()
        self.legend_box = None
        logger.debug('Initializing plot.')
        # self.viewbox.cursor_list = self.cursor_list #hack for menu management of
        self.menu = None

        icon_path = os.path.join(IMAGE_DIR, 'kiwi_small.png')
        self.setWindowIcon(QIcon(icon_path))

        self.show()
        self.hasTitle = False

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


    def reset(self):
        '''
        Clears all curves and dots from the plot, clears legend
        ''' 
        self.plot_item.clearPlots()
        self.linecolor_sequence = cycle(self.linecolors)

        if self.legend_box is not None:
            self.legend_box.remove_all_items()


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
        # self.grid = GridItem()
        # self.plot_item.addItem(self.grid)

        # self.grid.setParentItem(self.viewbox)
        xGrid = yGrid = True
        if len(args) == 1:
            xGrid = yGrid = args[0]
        elif len(args) == 2:
            xGrid = args[0]
            yGrid = args[1]
        self.plot_item.showGrid(x=xGrid, y=yGrid, alpha=1)

        # Solves the issue of gridllines being rendered on top of the curves: https://groups.google.com/g/pyqtgraph/c/plhxNt5Yp4o
        for ax in self.plot_item.axes:
            self.getAxis(ax).setZValue(-1) 


    def show_legend(self, legend_list=None, offset=None):
        '''
        Shows the legend box
        '''
        #offset[0], distance from right hand side of plot. 0=flush, -ve=distance from right
        # offset[1] - offset from top of plot, +ve = distance from top
        if offset is None:
            offset=[-LEGEND_OFFSET, LEGEND_OFFSET]
        else:
            offset = [-offset, offset]
            
        if self.hasTitle:
            offset[1] += TITLE_HEIGHT
    
        #Create legend box
        if self.legend_box is None:
            self.legend_box = LegendBox(offset=offset) 
            # self.legend_box.setParentItem(self.graphicsItem()) 
            self.legend_box.setParentItem(self.viewbox) #also works.  implicitly adds this graphics item to the scene of the parent

        #If no curves exist, use the default palette to define the curves
        #Note that the yaxis width is incorrect until self.plot() has been called
        if len(self.plot_item.curves) == 0:
            # linecolor_cycle = cycle(self.palette)
            for name in legend_list:
                pen = pg.functions.mkPen({'color': next(self.linecolor_sequence), 'width': self.linewidth})
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
        
    def hide_legend(self):
        '''
        Hide the legend box
        Ref: legend.scene().removeItem(legend)
        '''
        scene = self.legend_box.scene()
        scene.removeItem(self.legend_box)
        self.legend_box = None


    def show_label(self, text, isTight=True, offset=10):
        '''
        Shows a custom label in the top left corner of the plot. Can be used to display a title or a description.
        :param
        text - text to display
        offset - offset from the top left corner of the plot.
        '''
        self.label_box = LabelBox(isTight=isTight) #can also supply an offset arguement
        self.label_box.setParentItem(self.viewbox)
        self.label_box.addText(text)

        if isTight:
            offset -= 5
            self.label_box.shift(offset, offset) 



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

        #Zoombox
        self.viewbox.setZoomBoxColor(self.graphstyle['zoombox'])

        #Needed to ensure y axis are aligned
        # self.plot_item.getAxis('left').setWidth(plotstyle.YAXIS_WIDTH) 
        # self.plot_item.getAxis('left').setWidth(50) 

        #Changes the gridline color
        col = QColor(self.graphstyle['grid'])
        axis_pen = QPen(col)

        #TODO: Set the gridLine color for dark to light grey, not black.
        for ax in ('top', 'left', 'right', 'bottom'):
            axis = self.plot_item.getAxis(ax)
            axis.setPen(axis_pen)

        #Sets the font and color of the bottom & left axis units otherwise the text has
        #the same color as the gridlines
        # font = QFont("Source Sans Pro", 9) #tick font
        keys = ['bottom', 'left', 'top', 'right']
        # keys = ['bottom', 'left', 'top']
        for k in keys:
            axis = self.plot_item.getAxis(k)
            axis.setTickFont(AXIS_FONT)
            axis.setTextPen(self.graphstyle['text']) #sets text color

        #Needed to hide the top & right axis border. Otherwise this is rendered in black
        # self.showAxis('top')
        # self.showAxis('right')
        # self.getAxis('top').setStyle(tickLength=0, showValues=False)
        # self.getAxis('right').setStyle(tickLength=0, showValues=False)
        self.set_linecolors(graphstyle['linecolors'])


    def update_axis_style(self):
        '''
        This is called to apply the graphstyle presets to the axis in case the user adds custom axis after instantiating a plot
        The changes are only visible on the displayed axes.
        '''
        axis_keys = ['bottom', 'left', 'top', 'right']

              
        #Set the gridline color
        col = QColor(self.graphstyle['grid'])
        axis_pen = QPen(col)
        for k in axis_keys: # in ('top', 'left', 'right', 'bottom'):
            axis = self.plot_item.getAxis(k)
            axis.setPen(axis_pen)

        #Sets the axis tick font and color
        for k in axis_keys:
            axis = self.plot_item.getAxis(k)
            axis.setTickFont(AXIS_FONT)
            axis.setTextPen(self.graphstyle['text']) #sets text color
        


    def set_linecolors(self, palette):
        '''
        :param
        palette - a list of color strings. See plotsyle.py for examples.
        '''
        self.linecolors = palette
        self.linecolor_sequence = cycle(self.linecolors)


    # def _get_pen(self):
    #     '''
    #     Creates a pen based on the next color in the chosen linecolor sequence.
    #     '''
    #     color = next(self.linecolor_sequence)
    #     pen = pg.functions.mkPen({'color': color, 'width': self.linewidth})
    #     return pen, color

    @Slot(object)
    def _resized_view_box(self, view_box):
        '''
        Ensures the background color resizes with the plot.
        '''
        # print('Resized view box: {}'.format(self))

        #How to set the distance of all plots based on the largest width?
        # plot_item = self.getPlotItem()
        # d = plot_item.getAxis('left').width()
        # print(d)
        self._background.setRect(self.plot_item.mapRectFromItem(view_box, view_box.rect()))


    def plot(self, *args, color=None, linewidth=None, **kargs):
        '''
        Parameters:
        linewidth - set the width of the particular curve. If unspecified, the default linewidth is used.
        e.g. color='r'
        *args - x,y values for plotting
        '''
        if linewidth is None:
            linewidth = self.linewidth

        if len(args)%2:
            raise Exception('Number of arguments for plot() incorrect')
        for x, y in zip(*[iter(args)]*2): #iterate two items at a time
            if color is None: #automatically get next color in sequence
                color = next(self.linecolor_sequence)
                pen = pg.functions.mkPen({'color': color, 'width': linewidth})
                color = None
            else:
                pen = pg.functions.mkPen({'color': color, 'width': linewidth})
            curve = self.plot_item.plot(x, y, pen=pen, **kargs)
            # print(curve)
            curve.setZValue(1e6) 
        #TODO: Add try except
        # curve = self.plot_item.plot(x, y, pen=pen, **kargs)
        # return curve


    def update_curve(self, index, x, y):
        try:
            self.plotItem.curves[index].setData(x, y)
        except Exception as ex:
            raise Exception(f'Could not update curve with index {index}')


    def cursor_on(self, name=None, show_label=False):
        '''
        Adds a cursor. A new cursor is created every time this is called. 
        TODO: Check if deleteLater() is needed
        '''
        mypen = pg.functions.mkPen({'color': self.graphstyle['cursor'], 'width': plotstyle.CURSORWIDTH})  #white
        cursor = CursorLine(angle=90, movable=True, pen=mypen, hoverPen=mypen, name=name, parentWidget=self) #http://www.pyqtgraph.org/downloads/0.10.0/pyqtgraph-0.10.0-deb/pyqtgraph-0.10.0/examples/crosshair.py
        
        # if show_label:
        #     # labelOpts={'position':0.97, 'color': 'k', 'fill': (0xFF, 0xFF, 0xFF, 64), 'movable': True} #top
        #     labelOpts={'position':0.03, 'color': 'k', 'fill': (0xFF, 0xFF, 0xFF, 64), 'movable': True} #bottom
        #     cursor.set_label('1', labelOpts) #cursor label is in bottom left

        # self.cursor_list.append(cursor)
        cursor.show() #add cursor and cursor dots to self.plot_item
        logger.debug('Cursor added')
        self.cursor = cursor 

        #This works - The label itself is a TextItem
        # inf1 = pg.InfiniteLine(movable=True, angle=90, pen=mypen, label='x={value:0.2f}', 
        #                labelOpts={'position':0.1, 'color': 'k', 'fill': (0xFF, 0xFF, 0xFF, 64), 'movable': True})
        # self.plot_item.addItem(inf1)
    
        
    def cursor_off(self):
        self.cursor.hide()
        self.cursor = None
    
    def isCursorOff(self):
        return self.cursor is None
    
    def isCursorOn(self):
        return self.cursor is not None

    # @Slot(object)
    # def update_cursor(self, line):
    #     '''
    #     Called when the cursor was moved
    #     Params
    #     line - pyqtgraph InfiniteLine type
    #     '''
    #     xpos = line.x()
    #     # logger.debug('xpos: {}'.format(xpos))

    #     xlist = list()
    #     ylist = list()

    #     #Update cursor dots
    #     for i, curve in enumerate(self.plot_item.curves):
        
    #         if self.cursor.interpolateData is True: #linear interpolation
    #             y = np.interp(xpos, curve.xData, curve.yData)
    #             xlist.append(xpos)
    #             ylist.append(y)
    #             self.cursor_dots[i].setData([xpos], [y])
    #         else:
    #             #Render dots on actual data points, i.e. no interpolation
    #             idx = (np.abs(curve.xData - xpos)).argmin()
    #             xval = curve.xData[idx]
    #             yval = curve.yData[idx]
    #             xlist.append(xval)
    #             ylist.append(yval)
    #             self.cursor_dots[i].setData([xval], [yval])

    #     # self.cursorDataSignal.emit((xlist, ylist))

    def set_label(self, axis_key, label, unit=None):

        if axis_key not in ['bottom', 'left', 'top', 'right']:
            raise Exception('axis_key must be in: {}'.format(['bottom', 'left', 'top', 'right']))
        
        axis = self.plot_item.getAxis(axis_key)
        # axis.label.setFont(QFont('Source Sans Pro'))
        axis.label.setFont(QFont('Source Sans Pro'))
        axis.setLabel(label, unit, **plotstyle.axis_label_style)

    def set_xlabel(self, label, unit=None):
        #Workaround that allows the font to be set
        axis = self.plot_item.getAxis('bottom')
        axis.label.setFont(QFont('Source Sans Pro'))
        axis.setLabel(label, unit, **plotstyle.axis_label_style)
        # self.plot_item.setLabel('bottom', label, **plotstyle.label_style)
    
    def set_ylabel(self, label, unit=None):
        axis = self.plot_item.getAxis('left')
        axis.label.setFont(QFont('Source Sans Pro')) #axis.label = QGraphicsTextItem
        axis.setLabel(label, unit, **plotstyle.axis_label_style)
        # self.plot_item.setLabel('left', label, **plotstyle.label_style)
    
    def set_title(self, text):

        #Working but can't set the font-weight to bold. This is inconsistent with the axis label styles, which take CSS parameters
        # title_label = self.plot_item.titleLabel
        # title_label.item.setFont(QFont('Source Sans Pro'))
        # self.plot_item.setTitle(text, **plotstyle.title_style)

        #Nasty hack to allow proper CSS styling of the title
        #This is adapted from pyqtgraph.PlotItem.setTitle() and  pyqtgraph.LabelItem.setText()
        self.plot_item.titleLabel.setMaximumHeight(TITLE_HEIGHT) # self.plot_item.titleLabel is a LabelItem
        self.plot_item.layout.setRowFixedHeight(0, TITLE_HEIGHT) #row in which title label is placed
        self.plot_item.titleLabel.setVisible(True)
        self.plot_item.titleLabel.item.setFont(QFont('Source Sans Pro'))
        style = ';'.join(['%s: %s' % (k, plotstyle.title_style[k]) for k in plotstyle.title_style]) #This part is from pg.AxistItem.labelString()
        full = "<span style='{}'>{}</span>".format(style, text)
        self.plot_item.titleLabel.item.setHtml(full)
        # self.plot_item.titleLabel.item.setPlainText(text)
        self.plot_item.titleLabel.updateMin()
        self.plot_item.titleLabel.resizeEvent(None)
        self.plot_item.titleLabel.updateGeometry()
        self.hasTitle = True
        
        if self.legend_box is not None:
            logger.debug('Adjusting legend offset')
            self.legend_box.setOffset([-LEGEND_OFFSET, LEGEND_OFFSET+TITLE_HEIGHT])


    def set_linewidth(self, width):
        '''
        Set the default linewidth for all curves drawn on the plot.
        '''
        self.linewidth = width

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

    def link_x(self, plot):
        '''
        Link the x axis so that panning or zooming on plot causes the x axis on this kiwiplot to be updated.
        Parameters:
        plot - an instance of kiwiplot
        '''
        self.plotItem.setXLink(plot.plotItem)

    def autoYRange(self, x_range_start, x_range_end):
        self.enableAutoRange(axis='y')
        self.setAutoVisible(y=True)




if __name__ == '__main__':
    app = QApplication(sys.argv)
    fig = KiwiPlot()
    import numpy as np
    t = np.linspace(0, 20e-3, 100)
    y1 = 2*np.sin(2*np.pi*50*t)
    fig.plot(t,y1, name='y1')
    sys.exit(app.exec_())