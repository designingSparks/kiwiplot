# -*- coding: utf-8 -*-
'''
This is a patched version of pyqtgraph.InfiniteLine
'''
from .qtWrapper import *
from pyqtgraph.Point import Point
from pyqtgraph.graphicsItems.InfiniteLine import InfiniteLine
import numpy as np
from pyqtgraph.graphicsItems.GraphicsObject import GraphicsObject
# from pyqtgraph.graphicsItems.GraphicsItem import GraphicsItem
# from pyqtgraph.graphicsItems.TextItem import TextItem
# from pyqtgraph.graphicsItems.ViewBox import ViewBox
# from pyqtgraph import functions as fn
from pyqtgraph import ScatterPlotItem
# import weakref
from . import plotstyle
# from .klog import *
# logger = logging.getLogger('kiwiplot.' + __name__)

# __all__ = ['CursorLine', 'InfLineLabel']


class CursorLine2(InfiniteLine):
    
    cursorDataSignal = Signal(object, object)

    def __init__(self, *args, parentWidget=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.parentWidget = parentWidget
        self.xDataLimit = list()  
        self.interpolateData = True
        # self.isVisible = False #this causes a bug as there is already a fn called this.
        self.isDisplayed = False 
        self.isPressed = False
        self.cursor_dots = list() #store dots that show the intersection of the cursor and graph


    def show(self):
        '''
        Display cursor and cursor dots on parent plot item. Set the x position of the cursor automatically.
        Note: If curves are added to the plot after the cursor is shown, these will be unrecognized by the cursor.
        '''
        if self.isDisplayed: #prevent multiple calls to this function from creating many cursor dots
            return

        pw = self.parentWidget
        curve = pw.plot_item.curves[0] #use first line as reference
        # idx = int(len(curve.xData)/2)
        # xval = curve.xData[idx]
        left = pw.viewbox.viewRange()[0][0]
        right = pw.viewbox.viewRange()[0][1]
        xmid = np.average([left, right])
        # idx = (np.abs(curve.xData - mid)).argmin()
        # xval = curve.xData[idx]
        self.isDisplayed = True

        self.setXDataLimit([curve.xData[0], curve.xData[-1]])
        pw.plot_item.addItem(self, ignoreBounds=True)

        #Create and show the cursor dots
        for curve in pw.plot_item.curves:
            pen = curve.opts['pen']
            cursor_dot = ScatterPlotItem(size=plotstyle.CURSORDOTSIZE, pen=pen, brush=pen.color())
            self.cursor_dots.append(cursor_dot)
            pw.plot_item.addItem(cursor_dot, ignoreBounds=True)
            pw.plot_item.curves.pop() #Don't store the cursor dots in the curves list as these are stored in self.cursor_dots

            #Show the cursor dots
            # yval = curve.yData[idx] #find_nearest(curve.xData, xval)
            # cursor_dot.setData([xval], [yval])

        self.setPos(Point(xmid,0))


    def setXDataLimit(self, xlim):
        '''
        xlim a list of [xmin, xmax]
        Used to prevent the cursor from being dragged beyond the first or last data points.
        '''
        self.xDataLimit = xlim


    def forceDataSignal(self):
        '''
        Hack to ensure the legend box is initialized correctly
        '''
        xlist, ylist = self.update_cursor_dots()
        self.cursorDataSignal.emit((xlist, ylist), self)
    

    def update_cursor_dots(self):
        '''
        Called when the cursor was moved. It updates the cursor dot to the intersection point of the cursor and the curve.
        It also emits the cursorDataSignal signal, which contains the x, y coordinates of the new intersection points.
        Params
        line - pyqtgraph InfiniteLine type
        '''
        pw = self.parentWidget
        # xpos = line.x()
        xpos = self.p[0]
        xlist = list() #Data to emit
        ylist = list()
        # logger.debug('Updating cursor dots')

        #Update cursor dots
        for i, curve in enumerate(pw.plot_item.curves):
            if self.interpolateData is True: #linear interpolation
                y = np.interp(xpos, curve.xData, curve.yData)
                xlist.append(xpos)
                ylist.append(y)
                self.cursor_dots[i].setData([xpos], [y])
            else:
                #Render dots on actual data points, i.e. no interpolation
                idx = (np.abs(curve.xData - xpos)).argmin()
                xval = curve.xData[idx]
                yval = curve.yData[idx]
                xlist.append(xval)
                ylist.append(yval)
                self.cursor_dots[i].setData([xval], [yval])
        return xlist, ylist
    

    def hoverEvent(self, ev):
        if (not ev.isExit()) and self.movable and ev.acceptDrags(Qt.LeftButton):
            self.setMouseHover(True)
            self.parentWidget.setCursor(QCursor(Qt.SizeHorCursor))
        else:
            self.setMouseHover(False)
            if not self.isPressed:
                self.parentWidget.setCursor(QCursor(Qt.ArrowCursor))


    def mouseDragEvent(self, ev):
        if self.movable and ev.button() == Qt.LeftButton:
            if ev.isStart():
                self.moving = True
                #Mouse may not be pressed exactly on the cursorline. Maintain the original offset
                self.cursorOffset = self.pos() - self.mapToParent(ev.buttonDownPos()) 
                self.startPosition = self.pos()
            ev.accept()

            if not self.moving:
                return

            view = self.getViewBox()
            range = view.viewRange() #[[-0.000865195885804833, 0.020865195885804832], [-2.2279788573127783, 2.2279788573127783]]
            xrange = range[0] #x view extents in axis coordinates

            # Cursor drag limits
            newpos = self.cursorOffset + self.mapToParent(ev.pos())
            xmin = max(xrange[0], self.xDataLimit[0]) #prevent dragging to left of viewbox or min x value
            xmax = min(xrange[1], self.xDataLimit[1])
            if newpos.x() < xmin:
                newpos.setX(xmin)
            if newpos.x() > xmax:
                newpos.setX(xmax)
            self.setPos(newpos)
            # self.setPos(self.cursorOffset + self.mapToParent(ev.pos())) #original

            self.sigDragged.emit(self)
            if ev.isFinish():
                self.moving = False
                self.sigPositionChangeFinished.emit(self)
                self.parentWidget.setCursor(QCursor(Qt.ArrowCursor))
                self.isPressed = False

    def setPos(self, pos):
        '''
        Same as the parent function except for emitting the cursorDataSignal signal and calculating xlist, ylist.
        '''
        if isinstance(pos, (list, tuple, np.ndarray)) and not np.ndim(pos) == 0:
            newPos = list(pos)
        elif isinstance(pos, QPointF):
            newPos = [pos.x(), pos.y()]
        else:
            if self.angle == 90:
                newPos = [pos, 0]
            elif self.angle == 0:
                newPos = [0, pos]
            else:
                raise Exception("Must specify 2D coordinate for non-orthogonal lines.")

        ## check bounds (only works for orthogonal lines)
        if self.angle == 90:
            if self.maxRange[0] is not None:
                newPos[0] = max(newPos[0], self.maxRange[0])
            if self.maxRange[1] is not None:
                newPos[0] = min(newPos[0], self.maxRange[1])
        elif self.angle == 0:
            if self.maxRange[0] is not None:
                newPos[1] = max(newPos[1], self.maxRange[0])
            if self.maxRange[1] is not None:
                newPos[1] = min(newPos[1], self.maxRange[1])

        if self.p != newPos:
            self.p = newPos
            xlist, ylist = self.update_cursor_dots() #not in parent function
            self.viewTransformChanged()
            GraphicsObject.setPos(self, Point(self.p))
            self.sigPositionChanged.emit(self)
            self.cursorDataSignal.emit((xlist, ylist), self) #not in parent function