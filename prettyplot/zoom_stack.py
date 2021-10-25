from .qtWrapper import QObject, Signal
from prettyplot.pplogger import get_logger
logger = get_logger(__name__)


class ZoomStack(QObject):

    sigEnableForward = Signal(bool)
    sigEnableBack = Signal(bool)

    def __init__(self, plot_list):
        super().__init__()
        logger.debug('Initializing zoom stack')
        self.vbox_list = list() 
        self.stack = list() #stores the viewbox index and new zoomed Qrect 
        self.zoom_pos = 0
        for plot_widget in plot_list:
            plot_widget.plotItem.vb.sigZoom.connect(self.addToZoomStack)
            self.vbox_list.append(plot_widget.plotItem.vb) #store viewbox of the plot item for recalling zoom


    def addToZoomStack(self, viewbox, rect):

        idx = self.vbox_list.index(viewbox) 
        self.stack.append((idx, rect)) #store the view
        self.zoom_pos += 1

        logger.debug('Adding to zoom stack. Viewbox: {}'.format(idx))
        # logger.debug('Number of items in stack: {}'.format(len(self.stack)))
        logger.debug('zoom_pos: {}, len zoom_stack: {}'.format(self.zoom_pos, len(self.stack)))
        
        #TODO: What does this do??
        # n = len(self.stack) - self.zoom_pos - 1
        # if n:
        #     logger.debug('Pruning zoom stack. n={}'.format(n))
        #     self.stack = self.stack[:self.zoom_pos+1]

        self.sigEnableBack.emit(self.zoom_pos > 0)
        self.sigEnableForward.emit(self.zoom_pos < (len(self.stack) - 1))


    def zoom_back(self):
        logger.debug('Zooming back')
        if self.zoom_pos > 0:
            self.zoom_pos -= 1
            idx, rect = self.stack[self.zoom_pos]
            logger.debug('Rect: {}'.format(rect))
            viewbox = self.vbox_list[idx]
            viewbox.showAxRect(rect, padding=0) #apply zoom

        logger.debug('Zoom pos: {}'.format(self.zoom_pos))
        self.sigEnableBack.emit(self.zoom_pos > 0)
        self.sigEnableForward.emit(self.zoom_pos < (len(self.stack) - 1))