# -*- coding: utf-8 -*-
'''
This is a patched version of pyqtgraph.InfiniteLine
'''
from .qtWrapper import *
from pyqtgraph.Point import Point
from pyqtgraph.graphicsItems.GraphicsObject import GraphicsObject
from pyqtgraph.graphicsItems.GraphicsItem import GraphicsItem
from pyqtgraph.graphicsItems.TextItem import TextItem
from pyqtgraph.graphicsItems.ViewBox import ViewBox
from pyqtgraph import functions as fn
from pyqtgraph import ScatterPlotItem
import numpy as np
import weakref
from . import plotstyle
from .klog import *
logger = logging.getLogger('kiwiplot.' + __name__)

__all__ = ['CursorLine', 'InfLineLabel']


class CursorLine(GraphicsObject):
    """
    **Bases:** :class:`GraphicsObject <pyqtgraph.GraphicsObject>`

    Displays a line of infinite length.
    This line may be dragged to indicate a position in data coordinates.

    =============================== ===================================================
    **Signals:**
    sigDragged(self)
    sigPositionChangeFinished(self)
    sigPositionChanged(self)
    sigclicked(self, ev)
    =============================== ===================================================
    """

    sigDragged = Signal(object)
    sigPositionChangeFinished = Signal(object)
    sigPositionChanged = Signal(object)
    sigClicked =  Signal(object, object)
    cursorDataSignal = Signal(object, object)

    def __init__(self, pos=None, angle=90, pen=None, movable=False, bounds=None,
                 hoverPen=None, span=(0, 1), markers=None, 
                 name=None, parentWidget=None):
        """
        =============== ==================================================================
        **Arguments:**
        pos             Position of the line. This can be a QPointF or a single value for
                        vertical/horizontal lines.
        angle           Angle of line in degrees. 0 is horizontal, 90 is vertical.
        pen             Pen to use when drawing line. Can be any arguments that are valid
                        for :func:`mkPen <pyqtgraph.mkPen>`. Default pen is transparent
                        yellow.
        hoverPen        Pen to use when the mouse cursor hovers over the line. 
                        Only used when movable=True.
        movable         If True, the line can be dragged to a new position by the user.
        bounds          Optional [min, max] bounding values. Bounds are only valid if the
                        line is vertical or horizontal.
        hoverPen        Pen to use when drawing line when hovering over it. Can be any
                        arguments that are valid for :func:`mkPen <pyqtgraph.mkPen>`.
                        Default pen is red.
        span            Optional tuple (min, max) giving the range over the view to draw
                        the line. For example, with a vertical line, use span=(0.5, 1)
                        to draw only on the top half of the view.
        markers         List of (marker, position, size) tuples, one per marker to display
                        on the line. See the addMarker method.
        name            Name of the item
        =============== ==================================================================
        """
        self._boundingRect = None

        self._name = name

        GraphicsObject.__init__(self)

        if bounds is None:              ## allowed value boundaries for orthogonal lines
            self.maxRange = [None, None]
        else:
            self.maxRange = bounds
        self.moving = False
        self.setMovable(movable)
        self.mouseHovering = False
        self.p = [0, 0]
        self.setAngle(angle)

        if pos is None:
            pos = Point(0,0)
        self.setPos(pos)

        if pen is None:
            pen = (200, 200, 100)
        self.setPen(pen)
        
        if hoverPen is None:
            self.setHoverPen(color=(255,0,0), width=self.pen.width())
        else:
            self.setHoverPen(hoverPen)
        
        self.span = span
        self.currentPen = self.pen

        self.markers = []
        self._maxMarkerSize = 0
        if markers is not None:
            for m in markers:
                self.addMarker(*m)
                
        # Cache variables for managing bounds
        self._endPoints = [0, 1] # 
        self._bounds = None
        self._lastViewSize = None

        # if label is not None:
        #     labelOpts = {} if labelOpts is None else labelOpts
        #     self.label = InfLineLabel(self, text=label, **labelOpts)

        self.parentWidget = parentWidget

        self.xDataLimit = list()  
        self.interpolateData = True
        # self.isVisible = False #this causes a bug as there is already a fn called this.
        self.isDisplayed = False 
        self.isPressed = False
        self.cursor_dots = list() #store dots that show the intersection of the cursor and graph
        # self.sigPositionChanged.connect(self.update_cursor)


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


    def hide(self):
        '''
        Remove cursorLine and dots from parent plot item.
        '''
        self.parentWidget.plot_item.removeItem(self)
        for cursor_dot in self.cursor_dots:
            self.parentWidget.removeItem(cursor_dot)
            self.cursor_dots = list()


    # @Slot(object)
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

        # self.cursorDataSignal.emit((xlist, ylist), self)


    def setXDataLimit(self, xlim):
        '''
        xlim a list of [xmin, xmax]
        Used to prevent the cursor from being dragged beyond the first or last data points.
        '''
        self.xDataLimit = xlim

    def setMovable(self, m):
        """Set whether the line is movable by the user."""
        self.movable = m
        self.setAcceptHoverEvents(m)

    def setBounds(self, bounds):
        """Set the (minimum, maximum) allowable values when dragging."""
        self.maxRange = bounds
        self.setValue(self.value())
        
    def bounds(self):
        """Return the (minimum, maximum) values allowed when dragging.
        """
        return self.maxRange[:]
        
    def setPen(self, *args, **kwargs):
        """Set the pen for drawing the line. Allowable arguments are any that are valid
        for :func:`mkPen <pyqtgraph.mkPen>`."""
        self.pen = fn.mkPen(*args, **kwargs)
        if not self.mouseHovering:
            self.currentPen = self.pen
            self.update()

    def setHoverPen(self, *args, **kwargs):
        """Set the pen for drawing the line while the mouse hovers over it.
        Allowable arguments are any that are valid
        for :func:`mkPen <pyqtgraph.mkPen>`.

        If the line is not movable, then hovering is also disabled.

        Added in version 0.9.9."""
        # If user did not supply a width, then copy it from pen
        widthSpecified = ((len(args) == 1 and 
                           (isinstance(args[0], QPen) or
                           (isinstance(args[0], dict) and 'width' in args[0]))
                          ) or 'width' in kwargs)
        self.hoverPen = fn.mkPen(*args, **kwargs)
        if not widthSpecified:
            self.hoverPen.setWidth(self.pen.width())
            
        if self.mouseHovering:
            self.currentPen = self.hoverPen
            self.update()
        
    def addMarker(self, marker, position=0.5, size=10.0):
        """Add a marker to be displayed on the line. 
        
        ============= =========================================================
        **Arguments**
        marker        String indicating the style of marker to add:
                      ``'<|'``, ``'|>'``, ``'>|'``, ``'|<'``, ``'<|>'``,
                      ``'>|<'``, ``'^'``, ``'v'``, ``'o'``
        position      Position (0.0-1.0) along the visible extent of the line
                      to place the marker. Default is 0.5.
        size          Size of the marker in pixels. Default is 10.0.
        ============= =========================================================
        """
        path = QPainterPath()
        if marker == 'o': 
            path.addEllipse( QRectF(-0.5, -0.5, 1, 1))
        if '<|' in marker:
            p = QPolygonF([Point(0.5, 0), Point(0, -0.5), Point(-0.5, 0)])
            path.addPolygon(p)
            path.closeSubpath()
        if '|>' in marker:
            p = QPolygonF([Point(0.5, 0), Point(0, 0.5), Point(-0.5, 0)])
            path.addPolygon(p)
            path.closeSubpath()
        if '>|' in marker:
            p = QPolygonF([Point(0.5, -0.5), Point(0, 0), Point(-0.5, -0.5)])
            path.addPolygon(p)
            path.closeSubpath()
        if '|<' in marker:
            p = QPolygonF([Point(0.5, 0.5), Point(0, 0), Point(-0.5, 0.5)])
            path.addPolygon(p)
            path.closeSubpath()
        if '^' in marker:
            p = QPolygonF([Point(0, -0.5), Point(0.5, 0), Point(0, 0.5)])
            path.addPolygon(p)
            path.closeSubpath()
        if 'v' in marker:
            p = QPolygonF([Point(0, -0.5), Point(-0.5, 0), Point(0, 0.5)])
            path.addPolygon(p)
            path.closeSubpath()
        
        self.markers.append((path, position, size))
        self._maxMarkerSize = max([m[2] / 2. for m in self.markers])
        self.update()

    def clearMarkers(self):
        """ Remove all markers from this line.
        """
        self.markers = []
        self._maxMarkerSize = 0
        self.update()
        
    def setAngle(self, angle):
        """
        Takes angle argument in degrees.
        0 is horizontal; 90 is vertical.

        Note that the use of value() and setValue() changes if the line is
        not vertical or horizontal.
        """
        self.angle = angle #((angle+45) % 180) - 45   ##  -45 <= angle < 135
        self.resetTransform()
        self.setRotation(self.angle)
        self.update()


    def forceDataSignal(self):
        '''
        Hack to ensure the legend box is initialized correctly
        '''
        xlist, ylist = self.update_cursor_dots()
        self.cursorDataSignal.emit((xlist, ylist), self)

    def setPos(self, pos, emitSignal=True):

        if isinstance(pos, (list, tuple, np.ndarray)) and not np.ndim(pos) == 0:
            newPos = list(pos)
        elif isinstance(pos,  QPointF):
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
            xlist, ylist = self.update_cursor_dots()
            self.viewTransformChanged()
            GraphicsObject.setPos(self, Point(self.p))

            # if emitSignal:
            self.sigPositionChanged.emit(self)  
            self.cursorDataSignal.emit((xlist, ylist), self)

    def getXPos(self):
        return self.p[0]

    def getYPos(self):
        return self.p[1]

    def getPos(self):
        return self.p

    def value(self):
        """Return the value of the line. Will be a single number for horizontal and
        vertical lines, and a list of [x,y] values for diagonal lines."""
        if self.angle%180 == 0:
            return self.getYPos()
        elif self.angle%180 == 90:
            return self.getXPos()
        else:
            return self.getPos()

    def setValue(self, v):
        """Set the position of the line. If line is horizontal or vertical, v can be
        a single value. Otherwise, a 2D coordinate must be specified (list, tuple and
        QPointF are all acceptable)."""
        self.setPos(v)

    ## broken in 4.7
    #def itemChange(self, change, val):
        #if change in [self.ItemScenePositionHasChanged, self.ItemSceneHasChanged]:
            #self.updateLine()
            #print "update", change
            #print self.getBoundingParents()
        #else:
            #print "ignore", change
        #return GraphicsObject.itemChange(self, change, val)
    
    def setSpan(self, mn, mx):
        if self.span != (mn, mx):
            self.span = (mn, mx)
            self.update()

    def _computeBoundingRect(self):
        #br = UIGraphicsItem.boundingRect(self)
        vr = self.viewRect()  # bounds of containing ViewBox mapped to local coords.
        if vr is None:
            return  QRectF()
        
        ## add a 4-pixel radius around the line for mouse interaction.
        
        px = self.pixelLength(direction=Point(1,0), ortho=True)  ## get pixel length orthogonal to the line
        if px is None:
            px = 0
        pw = max(self.pen.width() / 2, self.hoverPen.width() / 2)
        w = max(4, self._maxMarkerSize + pw) + 1
        w = w * px
        br =  QRectF(vr)
        br.setBottom(-w)
        br.setTop(w)

        length = br.width()
        left = br.left() + length * self.span[0]
        right = br.left() + length * self.span[1]
        br.setLeft(left)
        br.setRight(right)
        br = br.normalized()
        
        vs = self.getViewBox().size()
        
        if self._bounds != br or self._lastViewSize != vs:
            self._bounds = br
            self._lastViewSize = vs
            self.prepareGeometryChange()
        
        self._endPoints = (left, right)
        self._lastViewRect = vr
        
        return self._bounds

    def boundingRect(self):
        if self._boundingRect is None:
            self._boundingRect = self._computeBoundingRect()
        return self._boundingRect

    def paint(self, p, *args):
        p.setRenderHint(p.Antialiasing)
        
        left, right = self._endPoints
        pen = self.currentPen
        pen.setJoinStyle( Qt.MiterJoin)
        p.setPen(pen)
        p.drawLine(Point(left, 0), Point(right, 0))
        
        
        if len(self.markers) == 0:
            return
        
        # paint markers in native coordinate system
        tr = p.transform()
        p.resetTransform()
        
        start = tr.map(Point(left, 0))
        end = tr.map(Point(right, 0))
        up = tr.map(Point(left, 1))
        dif = end - start
        length = Point(dif).length()
        angle = np.arctan2(dif.y(), dif.x()) * 180 / np.pi
        
        p.translate(start)
        p.rotate(angle)
        
        up = up - start
        det = up.x() * dif.y() - dif.x() * up.y()
        p.scale(1, 1 if det > 0 else -1)
        
        p.setBrush(fn.mkBrush(self.currentPen.color()))
        #p.setPen(fn.mkPen(None))
        tr = p.transform()
        for path, pos, size in self.markers:
            p.setTransform(tr)
            x = length * pos
            p.translate(x, 0)
            p.scale(size, size)
            p.drawPath(path)
        
    def dataBounds(self, axis, frac=1.0, orthoRange=None):
        if axis == 0:
            return None   ## x axis should never be auto-scaled
        else:
            return (0,0)

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

    def mousePressEvent(self, ev):
        logger.debug('press')
        self.parentWidget.setCursor(QCursor(Qt.SizeHorCursor))
        self.isPressed = True
        ev.ignore()
    
    def mouseClickEvent(self, ev):
        self.sigClicked.emit(self, ev)
        if self.moving and ev.button() == Qt.RightButton:
            ev.accept()
            self.setPos(self.startPosition)
            self.moving = False
            self.sigDragged.emit(self)
            self.sigPositionChangeFinished.emit(self)

    def hoverEvent(self, ev):
        if (not ev.isExit()) and self.movable and ev.acceptDrags(Qt.LeftButton):
            self.setMouseHover(True)
            self.parentWidget.setCursor(QCursor(Qt.SizeHorCursor))
        else:
            self.setMouseHover(False)
            if not self.isPressed:
                self.parentWidget.setCursor(QCursor(Qt.ArrowCursor))

    def setMouseHover(self, hover):
        ## Inform the item that the mouse is (not) hovering over it
        if self.mouseHovering == hover:
            return
        self.mouseHovering = hover
        if hover:
            self.currentPen = self.hoverPen
        else:
            self.currentPen = self.pen
        self.update()

    def viewTransformChanged(self):
        """
        Called whenever the transformation matrix of the view has changed.
        (eg, the view range has changed or the view was resized)
        """
        self._boundingRect = None
        GraphicsItem.viewTransformChanged(self)
        
    def setName(self, name):
        self._name = name

    def name(self):
        return self._name


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
    =============== ==================================================================
    
    All extra keyword arguments are passed to TextItem. A particularly useful
    option here is to use `rotateAxis=(1, 0)`, which will cause the text to
    be automatically rotated parallel to the line.
    """
    def __init__(self, line, text="", movable=False, position=0.5, anchors=None, **kwds):
        self.line = line
        self.movable = movable
        self.moving = False
        self.orthoPos = position  # text will always be placed on the line at a position relative to view bounds
        self.format = text
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
        self.valueChanged()
        self.setAnchor(self.anchors[1]) #set to left of line
        # self.setAnchor(self.anchors[0]) #set to right of line

    def valueChanged(self):
        if not self.isVisible():
            return
        value = self.line.value()
        self.setText(self.format.format(value=value))
        self.updatePosition()

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
            
    def setMovable(self, m):
        """Set whether this label is movable by dragging along the line.
        """
        self.movable = m
        self.setAcceptHoverEvents(m)
        
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
