'''
Monkey patching of pyqtgraph.ViewBox to add additional zoom modes.
'''
import numpy as np
from pyqtgraph.graphicsItems.ViewBox import ViewBox
from pyqtgraph import functions as fn
from pyqtgraph import Point
from .qtWrapper import *
from .constants import ZOOM_MODE
from .plotstyle import zoom_blue

from .klog import get_logger
logger = get_logger(__name__)


class ViewBox2(ViewBox):

    sigZoom = Signal()


    # def scaleHistory(self, d):
    #     if len(self.axHistory) == 0:
    #         return
    #     ptr = max(0, min(len(self.axHistory)-1, self.axHistoryPointer+d))
    #     if ptr != self.axHistoryPointer:
    #         self.axHistoryPointer = ptr
    #         self.showAxRect(self.axHistory[ptr])


    def __init__(self, parent=None, border=None, lockAspect=False, enableMouse=True, invertY=False, enableMenu=True, name=None, invertX=False, defaultPadding=0.02):
        super().__init__(parent, border, lockAspect, enableMouse, invertY, enableMenu, name, invertX, defaultPadding)
        self._zoomMode = ZOOM_MODE.xZoom #default zoom mode
        self.setZoomBoxColor(zoom_blue)
        
    def setZoomBoxColor(self, color):
        self.rbScaleBox.setPen(fn.mkPen(color[:3], width=1)) #outer border of zoom box is solid (ignore alpha value)
        brush = fn.mkBrush(color)
        self.rbScaleBox.setBrush(brush) #inner color is transparent

    def setZoomMode(self, mode):
        if mode not in [ZOOM_MODE.freeZoom, ZOOM_MODE.xZoom, ZOOM_MODE.yZoom]:
            raise Exception("Mode must be ZOOM_MODE.freeZoom, ZOOM_MODE.xZoom, or ZOOM_MODE.yZoom")
        self._zoomMode = mode


    def mousePressEvent(self, event):
        '''
        Stores the mouse starting position
        '''
        self.start_pos = event.pos()
        self.start_point = self.mapToView(self.start_pos)
        # logger.debug('Start point xy: {}, {}'.format(self.start_point.x(), self.start_point.y()))
        # logger.debug('Mouse press detected')
        rect = self.viewRect()
        event_valid = rect.contains(self.mapToView(self.start_pos))
        # logger.debug('Pressed in viewbox: {}'.format(event_valid))
        event.ignore()

    
    def mouseDragEvent(self, ev, axis=None):
        ## if axis is specified, event will only affect that axis.
        ev.accept()  ## we accept all buttons
        if self.start_pos is None:
            return

        pos = ev.pos()
        lastPos = ev.lastPos()
        dif = pos - lastPos
        dif = dif * -1

        ## Ignore axes if mouse is disabled
        mouseEnabled = np.array(self.state['mouseEnabled'], dtype=np.float64)
        mask = mouseEnabled.copy()
        if axis is not None:
            mask[1-axis] = 0.0

        ## Scale or translate based on mouse button
        if ev.button() & (Qt.LeftButton | Qt.MiddleButton):
            if self.state['mouseMode'] == ViewBox.RectMode and axis is None:
                if ev.isFinish():  ## This is the final move in the drag; change the view scale now
                    logger.debug('Zoom finish')
                    self.start_pos = None
                    self.rbScaleBox.hide()
                    _p1 = self.start_point
                    _p2 = self.mapToView(pos)

                    if  self._zoomMode == ZOOM_MODE.xZoom:
                        left = self.viewRange()[0][0]
                        right = self.viewRange()[0][1]
                        bottom = self.viewRange()[1][0]
                        top = self.viewRange()[1][1]
                        
                        x_release = _p2.x()
                        if x_release < left:
                            x_release = left
                        elif x_release > right:
                            x_release = right
                        
                        _p1 = QPointF(_p1.x(), top)
                        _p2 = QPointF(x_release, bottom)
            #             print('_p1: {}, {}'.format(_p1.x(), _p1.y()))
            #             print('_p2: {}, {}'.format(_p2.x(), _p2.y()))
                        ax = QRectF(_p1, _p2)
#                         self.setXRange(self.start_point.x(), point.x(), padding=0) #works
                        
                    elif self._zoomMode == ZOOM_MODE.yZoom:
                        left = self.viewRange()[0][0]
                        right = self.viewRange()[0][1]
                        bottom = self.viewRange()[1][0]
                        top = self.viewRange()[1][1]
                        
                        #TODO
                        y_release = _p2.y()
                        if y_release < bottom:
                            y_release = bottom
                        elif y_release > top:
                            y_release = top
                            
                            
                        _p1 = QPointF(left, _p1.y())
                        _p2 = QPointF(right, y_release)
            #             print('_p1: {}, {}'.format(_p1.x(), _p1.y()))
            #             print('_p2: {}, {}'.format(_p2.x(), _p2.y()))
                        ax = QRectF(_p1, _p2)
#                         self.setYRange(self.start_point.y(), point.y(), padding=0) #works
                        
                    elif self._zoomMode == ZOOM_MODE.freeZoom:
                        p1 = Point(ev.buttonDownPos(ev.button()))
                        p2 = Point(pos)
                        ax = QRectF(p1, p2)
                        ax = self.childGroup.mapRectFromParent(ax)
                    
                    logger.debug('ax: {}'.format(ax))
                    self.showAxRect(ax, padding=0) #apply zoom
                    self.axHistoryPointer += 1
                    self.axHistory = self.axHistory[:self.axHistoryPointer] + [ax]
                    self.sigZoom.emit() #zoom stack in zoom_stack.py

                    # ax = QtCore.QRectF(Point(ev.buttonDownPos(ev.button())), Point(pos))
                    # ax = self.childGroup.mapRectFromParent(ax)
                    # self.showAxRect(ax)
                    # self.axHistoryPointer += 1
                    # self.axHistory = self.axHistory[:self.axHistoryPointer] + [ax]
                else: #if dragging
                    ## update shape of scale box
                    # self.updateScaleBox(ev.buttonDownPos(), ev.pos())
                    rect = self.viewRect()
                    event_valid = rect.contains(self.mapToView(pos))
                    # logger.debug('Drag in viewbox: {}'.format(event_valid))
                    
                    #Could simplify this
                    if self._zoomMode == ZOOM_MODE.xZoom or self._zoomMode == ZOOM_MODE.yZoom:
                        delta = pos - self.start_pos
                        dx = delta.x()
                        dy = delta.y()
                        if abs(dx) > abs(dy):
                            if self._zoomMode != ZOOM_MODE.xZoom:
                                self._zoomMode = ZOOM_MODE.xZoom
                                logger.debug('Setting ZOOM_MODE.xZoom')
                        else:
                            if self._zoomMode != ZOOM_MODE.yZoom:
                                self._zoomMode = ZOOM_MODE.yZoom
                                logger.debug('Setting ZOOM_MODE.yZoom')
                            
                    ## update the zoom rectangle
#                     self.updateScaleBox(ev.buttonDownPos(), ev.pos()) #Original

                    self.updateScaleBox(self.start_pos, ev.pos()) 


            else:
                tr = self.childGroup.transform()
                tr = fn.invertQTransform(tr)
                tr = tr.map(dif*mask) - tr.map(Point(0,0))

                x = tr.x() if mask[0] == 1 else None
                y = tr.y() if mask[1] == 1 else None

                self._resetTarget()
                if x is not None or y is not None:
                    self.translateBy(x=x, y=y)
                self.sigRangeChangedManually.emit(self.state['mouseEnabled'])
        elif ev.button() & Qt.RightButton:
            #print "vb.rightDrag"
            if self.state['aspectLocked'] is not False:
                mask[0] = 0

            dif = ev.screenPos() - ev.lastScreenPos()
            dif = np.array([dif.x(), dif.y()])
            dif[0] *= -1
            s = ((mask * 0.02) + 1) ** dif

            tr = self.childGroup.transform()
            tr = fn.invertQTransform(tr)

            x = s[0] if mouseEnabled[0] == 1 else None
            y = s[1] if mouseEnabled[1] == 1 else None

            center = Point(tr.map(ev.buttonDownPos(Qt.RightButton)))
            self._resetTarget()
            self.scaleBy(x=x, y=y, center=center)
            self.sigRangeChangedManually.emit(self.state['mouseEnabled'])


    def updateScaleBox(self, p1, p2):
        # r = QtCore.QRectF(p1, p2)
        # r = self.childGroup.mapRectFromParent(r)
        # self.rbScaleBox.setPos(r.topLeft())
        # tr = QtGui.QTransform.fromScale(r.width(), r.height())
        # self.rbScaleBox.setTransform(tr)
        # self.rbScaleBox.show()
        '''Called during dragging'''
        _p1 = self.mapToView(p1) #works better than mapSceneToView
        _p2 = self.mapToView(p2)
        
        #Calculate QRect r differently base on zoom mode
        if self._zoomMode == ZOOM_MODE.xZoom:

            bottom = self.viewRange()[1][0]
            top = self.viewRange()[1][1]
            _p1 = QPointF(_p1.x(), top)
            _p2 = QPointF(_p2.x(), bottom)
#             print('_p1: {}, {}'.format(_p1.x(), _p1.y()))
#             print('_p2: {}, {}'.format(_p2.x(), _p2.y()))
            r = QRectF(_p1, _p2)
            
        elif self._zoomMode == ZOOM_MODE.yZoom:
            #View coordinates
            left = self.viewRange()[0][0]
            right = self.viewRange()[0][1]
            _p1 = QPointF(left, _p1.y())
            _p2 = QPointF(right, _p2.y())
#             print('_p1: {}, {}'.format(_p1.x(), _p1.y()))
#             print('_p2: {}, {}'.format(_p2.x(), _p2.y()))
            r = QRectF(_p1, _p2)
            
        elif self._zoomMode == ZOOM_MODE.freeZoom:
            r = QRectF(p1, p2)
            r = self.childGroup.mapRectFromParent(r)
        
        #Working
        self.rbScaleBox.setPos(r.topLeft())
        tr = QTransform.fromScale(r.width(), r.height())
        self.rbScaleBox.setTransform(tr)
        self.rbScaleBox.show()
