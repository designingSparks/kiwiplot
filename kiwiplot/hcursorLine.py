# -*- coding: utf-8 -*-
'''
This horizontal cursor line is stationary and is designed to be used in conjunction with a vertical cursor line, which is moveable.
Used with the vertical cursor, it becomes a crosshair cursor.
Its position is set by the cursorDataSignal of the vertical cursor.
It doesn't emit any signals, it just consumes the signal from the vertical cursor.

TODO:
Test the log scale functionality
'''
from .qtWrapper import *
from pyqtgraph.Point import Point
from pyqtgraph.graphicsItems.GraphicsObject import GraphicsObject
from pyqtgraph.graphicsItems.GraphicsItem import GraphicsItem
from pyqtgraph.graphicsItems.TextItem import TextItem
from pyqtgraph.graphicsItems.InfiniteLine import InfiniteLine
import numpy as np
from pyqtgraph.graphicsItems.GraphicsObject import GraphicsObject
# from pyqtgraph.graphicsItems.GraphicsItem import GraphicsItem
# from pyqtgraph.graphicsItems.TextItem import TextItem
# from pyqtgraph.graphicsItems.ViewBox import ViewBox
# from pyqtgraph import functions as fn
from pyqtgraph import ScatterPlotItem
from pyqtgraph.functions import mkBrush
# import weakref
from . import plotstyle
# from .klog import *
# logger = logging.getLogger('kiwiplot.' + __name__)

# __all__ = ['CursorLine', 'InfLineLabel']


class HCursorLine(InfiniteLine):
    
    def __init__(self, *args, parentWidget=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.parentWidget = parentWidget
        self.yDataLimit = list()  
        self.interpolateData = True
        # self.isVisible = False #this causes a bug as there is already a fn called this.
        self.isDisplayed = False 
        self.isPressed = False
        # self.cursor_dots = list() #store dots that show the intersection of the cursor and graph
        self.labels = list()
        self.isLog = self.parentWidget.plot_item.ctrl.logXCheck.isChecked() #True or False

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

        #TODO: With log scale, the cursor is not placed at the correct position
        # left = pw.viewbox.viewRange()[0][0]
        # right = pw.viewbox.viewRange()[0][1]
        # xmid = np.average([left, right])

        
        # if isLog:
        #     self.isLog
        #     self.xlog = 10**xmid #Use xlog to get the y value
            
        # idx = (np.abs(curve.xData - mid)).argmin()
        # xval = curve.xData[idx]
        self.isDisplayed = True

        # self.setXDataLimit([curve.xData[0], curve.xData[-1]])
        self.setYDataLimit([curve.yData[0], curve.yData[-1]])

        pw.plot_item.addItem(self, ignoreBounds=True) #add cursor to plot item

        #Create and show the cursor dots
        # for curve in pw.plot_item.curves:
        #     pen = curve.opts['pen']
        #     cursor_dot = ScatterPlotItem(size=plotstyle.CURSORDOTSIZE, pen=pen, brush=pen.color())
        #     self.cursor_dots.append(cursor_dot)
        #     pw.plot_item.addItem(cursor_dot, ignoreBounds=True)
        #     pw.plot_item.curves.pop() #Don't store the cursor dots in the curves list as these are stored in self.cursor_dots

            #Show the cursor dots
            # yval = curve.yData[idx] #find_nearest(curve.xData, xval)
            # cursor_dot.setData([xval], [yval])

        # self.setPos(Point(0,0)) #x,y position of the cursor


    def hide(self):
        '''
        Remove cursorLine and dots from parent plot item.
        '''
        self.parentWidget.plot_item.removeItem(self)
        # for cursor_dot in self.cursor_dots:
        #     self.parentWidget.removeItem(cursor_dot)
        #     self.cursor_dots = list()

            
    # def setXDataLimit(self, xlim):
    #     '''
    #     xlim a list of [xmin, xmax]
    #     Used to prevent the cursor from being dragged beyond the first or last data points.
    #     '''
    #     if self.isLog:
    #         self.xDataLimit = [np.log10(x) for x in xlim]
    #     else:
    #         self.xDataLimit = xlim


    def setYDataLimit(self, ylim):
        '''
        xlim a list of [xmin, xmax]
        Used to prevent the cursor from being dragged beyond the first or last data points.
        '''
        if self.isLog:
            self.yDataLimit = [np.log10(y) for y in ylim]
        else:
            self.yDataLimit = ylim

    # def forceDataSignal(self):
    #     '''
    #     Hack to ensure the legend box is initialized correctly
    #     '''
    #     xlist, ylist = self.update_cursor_dots()
    #     self.cursorDataSignal.emit((xlist, ylist), self)
    


    def hoverEvent(self, ev):
        if (not ev.isExit()) and self.movable and ev.acceptDrags(Qt.LeftButton):
            self.setMouseHover(True)
        else:
            self.setMouseHover(False)


    def mouseDragEvent(self, ev):
        if self.movable and ev.button() == Qt.LeftButton:
            if ev.isStart(): #drag start
                self.moving = True
                #Mouse may not be pressed exactly on the cursorline. Maintain the original offset
                self.cursorOffset = self.pos() - self.mapToParent(ev.buttonDownPos()) 
                self.startPosition = self.pos()
                # self.parentWidget.setCursor(QCursor(Qt.SizeVerCursor))
            ev.accept()

            if not self.moving:
                return
            

            # Limits for the cursor
            # view = self.getViewBox()
            # range = view.viewRange() #[[-0.000865195885804833, 0.020865195885804832], [-2.2279788573127783, 2.2279788573127783]]
            # xrange = range[0] #x view extents in axis coordinates

            # # Cursor drag limits
            # newpos = self.cursorOffset + self.mapToParent(ev.pos())
        
            # xmin = max(xrange[0], self.xDataLimit[0]) #prevent dragging to left of viewbox or min x value
            # xmax = min(xrange[1], self.xDataLimit[1])

            # if newpos.x() < xmin:
            #     newpos.setX(xmin)
            # if newpos.x() > xmax:
            #     newpos.setX(xmax)
            # self.setPos(newpos)
            self.setPos(self.cursorOffset + self.mapToParent(ev.pos())) #original

            self.sigDragged.emit(self)
            if ev.isFinish(): #drag end
                self.moving = False
                self.sigPositionChangeFinished.emit(self)
                self.parentWidget.setCursor(QCursor(Qt.ArrowCursor))
                self.isPressed = False

    def setPos(self, pos):
        '''
        Derived from the parent function. 
        It sets the position of the cursor and emits the cursorDataSignal signal and calculating xlist, ylist.
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
        if self.angle == 0:
            if self.maxRange[0] is not None:
                newPos[1] = max(newPos[1], self.maxRange[0])
            if self.maxRange[1] is not None:
                newPos[1] = min(newPos[1], self.maxRange[1])

        if self.p != newPos:

            self.p = newPos

            #Hack because of how the data signal is emitted from the vertical cursor
            x = self.p[0][0]
            y = self.p[1][0]
            # xlist, ylist = self.update_cursor_dots() #not in parent function
            self.viewTransformChanged()
            # print('New position: {}'.format(self.p))
            GraphicsObject.setPos(self, Point(x,y))
            self.sigPositionChanged.emit(self) #Needed to update the cursor label

            if self.isLog:
                xlist = [10**x for x in xlist]


    def set_label(self, label, labelOpts):
        '''
        ParamsL
        label           Text to be displayed in a label attached to the line, or
                        None to show no label (default is None). May optionally
                        include formatting strings to display the line value.
        labelOpts       A dict of keyword arguments to use when constructing the
                        text label. See :class:`InfLineLabel`.
        '''
        self.label = InfLineLabel(self, text=label, **labelOpts)


    def add_label(self, label_name, format, labelOpts):
        ''' 
        Add a label to the cursor line. This is different from set_label() as it allows multiple labels to be added.
        '''
        label = InfLineLabel(self, text=label_name, format=format, **labelOpts)
        self.labels.append(label)
        return label



class InfLineLabel(TextItem):
    """
    A TextItem that attaches itself to an InfiniteLine.
    
    This class extends TextItem with the following features:
    
    * Automatically positions adjacent to the line at a fixed position along
      the line and within the view box.
    * Automatically reformats text when the line value has changed.
    * Can optionally be dragged to change its location along the line.
    * Optionally aligns to its parent line.

    =============== ==================================================================
    **Arguments:**
    line            The InfiniteLine to which this label will be attached.
    text            String to display in the label. May contain a {value} formatting
                    string to display the current value of the line.
    movable         Bool; if True, then the label can be dragged along the line.
    position        Relative position (0.0-1.0) within the view to position the label
                    along the line.
    anchors         List of (x,y) pairs giving the text anchor positions that should
                    be used when the line is moved to one side of the view or the
                    other. This allows text to switch to the opposite side of the line
                    as it approaches the edge of the view. These are automatically
                    selected for some common cases, but may be specified if the 
                    default values give unexpected results.

    zero_val        Needed to calculate the percentage change wrt. a zero value.

    calc_pc         If True, the label will display the percentage change wrt. a zero value.

    =============== ==================================================================
    
    All extra keyword arguments are passed to TextItem. A particularly useful
    option here is to use `rotateAxis=(1, 0)`, which will cause the text to
    be automatically rotated parallel to the line.
    """
    def __init__(self, line, text="", format=None, zero_val=None, calc_pc=False, movable=False, position=0.5, anchors=None, **kwds):
        self.line = line
        self.movable = movable
        self.moving = False
        self.orthoPos = position  # text will always be placed on the line at a position relative to view bounds
        self.format = format
        self.zero_val = zero_val 
        self.calc_pc = calc_pc
        self.line.sigPositionChanged.connect(self.valueChanged)
        self._endpoints = (None, None)
        if anchors is None:
            # automatically pick sensible anchors
            rax = kwds.get('rotateAxis', None)
            if rax is not None:
                if tuple(rax) == (1,0):
                    anchors = [(0.5, 0), (0.5, 1)]
                else:
                    anchors = [(0, 0.5), (1, 0.5)]
            else:
                if line.angle % 180 == 0:
                    anchors = [(0.5, 0), (0.5, 1)]
                else:
                    anchors = [(0, 0.5), (1, 0.5)]
            
        self.anchors = anchors
        TextItem.__init__(self, **kwds)
        self.setParentItem(line)
        self.setAnchor(self.anchors[1])
        self.value_prev = 0
        self.valueChanged()
        value = self.line.value()[0]  #Make sure the initial position is set above or below
        self.update_anchor(value)


    def set_below(self, isBelow):
        '''
        Set the label below or above the horizontal cursor
        :param
        isBelow - bool
        '''
        if isBelow:
            self.setAnchor(self.anchors[0]) #underneath horizontal cursor
            self.fill = mkBrush((0xCC, 0, 0, 200))
        else:
            self.setAnchor(self.anchors[1]) #on top of horizontal cursor
            self.fill = mkBrush((0x1F, 0x77, 0xB4, 200))


    def update_anchor(self, value):
        '''Update the position to above or below the horizontal cursor. Called from valueChanged().
        '''
        if value > 0:
            self.set_below(False)
        else:
            self.set_below(True)


    def config_percentage_calc(self, zero_val):
        '''
        Call this function to configure the label to calculate the percentage change wrt. a zero value rather
        than displaying the absolute value.
        '''
        self.calc_pc = True
        self.zero_val = zero_val
        self.valueChanged()


    def valueChanged(self):
        if not self.isVisible():
            return
        value = self.line.value()[0] #why is this a list?

        if (self.value_prev > 0) != (value > 0): #Changes the position of the label if the cursor crosses zero
            self.update_anchor(value)
        
        new_text = self.format(value)
        self.setText(new_text)
        self.updatePosition()
        self.value_prev = value

    def getEndpoints(self):
        # calculate points where line intersects view box
        # (in line coordinates)
        if self._endpoints[0] is None:
            lr = self.line.boundingRect()
            pt1 = Point(lr.left(), 0)
            pt2 = Point(lr.right(), 0)
            
            if self.line.angle % 90 != 0:
                # more expensive to find text position for oblique lines.
                view = self.getViewBox()
                if not self.isVisible() or not isinstance(view, ViewBox):
                    # not in a viewbox, skip update
                    return (None, None)
                p = QPainterPath()
                p.moveTo(pt1)
                p.lineTo(pt2)
                p = self.line.itemTransform(view)[0].map(p)
                vr = QPainterPath()
                vr.addRect(view.boundingRect())
                paths = vr.intersected(p).toSubpathPolygons(QTransform())
                if len(paths) > 0:
                    l = list(paths[0])
                    pt1 = self.line.mapFromItem(view, l[0])
                    pt2 = self.line.mapFromItem(view, l[1])
            self._endpoints = (pt1, pt2)
        return self._endpoints
    
    def updatePosition(self):
        # update text position to relative view location along line
        self._endpoints = (None, None)
        pt1, pt2 = self.getEndpoints()
        if pt1 is None:
            return
        pt = pt2 * self.orthoPos + pt1 * (1-self.orthoPos)
        self.setPos(pt)
        
        #This flips the text label automatically to the left or right of the line when the 
        #line transverses the middle of the viewbox
        # update anchor to keep text visible as it nears the view box edge
        # vr = self.line.viewRect()
        # if vr is not None:
        #     logger.debug(vr.center().y())
        #     self.setAnchor(self.anchors[0 if vr.center().y() < 0 else 1])
        
    def setVisible(self, v):
        TextItem.setVisible(self, v)
        if v:
            self.valueChanged()
            
    # def setMovable(self, m):
    #     """Set whether this label is movable by dragging along the line.
    #     """
    #     self.movable = m
    #     self.setAcceptHoverEvents(m)
        
    def setPosition(self, p):
        """Set the relative position (0.0-1.0) of this label within the view box
        and along the line. 
        
        For horizontal (angle=0) and vertical (angle=90) lines, a value of 0.0
        places the text at the bottom or left of the view, respectively. 
        """
        self.orthoPos = p
        self.updatePosition()
        
    def setFormat(self, text):
        """Set the text format string for this label.
        
        May optionally contain "{value}" to include the lines current value
        (the text will be reformatted whenever the line is moved).
        """
        self.format = text
        self.valueChanged()
        
    def mouseDragEvent(self, ev):
        if self.movable and ev.button() == Qt.LeftButton:
            if ev.isStart():
                self._moving = True
                self._cursorOffset = self._posToRel(ev.buttonDownPos())
                self._startPosition = self.orthoPos
            ev.accept()

            if not self._moving:
                return

            rel = self._posToRel(ev.pos())
            self.orthoPos = np.clip(self._startPosition + rel - self._cursorOffset, 0, 1)
            self.updatePosition()
            if ev.isFinish():
                self._moving = False

    def mouseClickEvent(self, ev):
        if self.moving and ev.button() == Qt.RightButton:
            ev.accept()
            self.orthoPos = self._startPosition
            self.moving = False

    def hoverEvent(self, ev):
        if not ev.isExit() and self.movable:
            ev.acceptDrags(Qt.LeftButton)

    def viewTransformChanged(self):
        GraphicsItem.viewTransformChanged(self)
        self.updatePosition()
        TextItem.viewTransformChanged(self)

    def _posToRel(self, pos):
        # convert local position to relative position along line between view bounds
        pt1, pt2 = self.getEndpoints()
        if pt1 is None:
            return 0
        view = self.getViewBox()
        pos = self.mapToParent(pos)
        return (pos.x() - pt1.x()) / (pt2.x()-pt1.x())
