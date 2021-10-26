'''
The zoomstack is useful for recalling or restoring zoomed views on multiple prettyplot objects that are within the same QMainWindow.
It can be used with a single plot or multiple plots.

The zoom state is stored as follows:
[0, rect1, 1, rect2...]
where n is the index of the viewbox in self.vbox_list and rectn are the limits of the viewbox.
The viewboxes that are managed by the zoomstack are in self.vbox_list

Usage:
To initialize, pass the plots that the zoomstack should manage to the contructer.
Plot the data on the plot
Call the function initZoomStack.

TODO:
Complete documentation
'''


from .qtWrapper import *
from prettyplot.pplogger import get_logger
logger = get_logger(__name__)


class ZoomStack(QObject):

    sigEnableForward = Signal(bool)
    sigEnableBack = Signal(bool)

    def __init__(self, plot_list):
        super().__init__()
        logger.debug('Initializing zoom stack')
        self.vbox_list = list() #viewboxes managed by the zoom stack
        self.stack = list() #the stack itself, stores each zoom state
        self.zoom_pos = 0
        for plot_widget in plot_list:
            plot_widget.plotItem.vb.sigZoom.connect(self.addToZoomStack)
            self.vbox_list.append(plot_widget.plotItem.vb) #store viewbox of the plot item for recalling zoom
        # self.initZoomStack()


    def initZoomStack(self):
        '''
        Store the initial zoom state of all viewboxes managed by the zoom stack. 
        The data must be plotted in the viewbox first otherwise the default unit rectangle
        will be stored in pozition 0 on the stack.
        '''
        zoom_state = list()

        for i, viewbox in enumerate(self.vbox_list):
            vr = viewbox.viewRange() #note the viewrange does not match the coordinates
            bottom = vr[1][0]
            top = vr[1][1]
            left = vr[0][0]
            right = vr[0][1]
            _p1 = QPointF(left, top)
            _p2 = QPointF(right, bottom)
            rect = QRectF(_p1, _p2)
            logger.debug(rect)
            zoom_state.append(i)
            zoom_state.append(rect)
        
        self.stack.append(zoom_state)
        # logger.debug('Stored initial zoom state: {}'.format(zoom_state))


    def zoom_home(self):
        logger.debug('Restoring home view')
        self.recall_view(self.stack[0])
        

    def recall_view(self, zoom_state):
        '''
        zoom_state is an entry in the self.stack
        '''
        for idx, rect in zip(*[iter(zoom_state)]*2): #first item in stack
            # print(idx, rect)
            logger.debug('Recalling view')
            viewbox = self.vbox_list[idx]
            viewbox.showAxRect(rect, padding=0) #recall view


    def addToZoomStack(self, viewbox, rect):
        
        idx = self.vbox_list.index(viewbox) 
        zoom_state = [idx, rect]
        self.stack.append(zoom_state) #store the view
        self.zoom_pos += 1

        #If an item is added to the stack and self.zoom_pos is not at the stack head
        #discard items after the stack head
        n = len(self.stack) - self.zoom_pos - 1
        if n:
            logger.debug('Pruning zoom stack. n={}'.format(n))
            self.stack = self.stack[:self.zoom_pos+1]


        logger.debug('Adding to zoom stack. Viewbox: {}'.format(idx))
        logger.debug('Number of items in stack: {}'.format(len(self.stack)))
        logger.debug('zoom_pos: {}'.format(self.zoom_pos))
        

        self.sigEnableBack.emit(self.zoom_pos > 0)
        self.sigEnableForward.emit(self.zoom_pos < (len(self.stack) - 1))

    @Slot()
    def zoom_back(self):
        '''
        Slot for the forward button on the toolbar.
        '''
        if self.zoom_pos > 0:
            self.zoom_pos -= 1
            logger.debug(f'Zooming to position: {self.zoom_pos}')    
            self.recall_view(self.stack[self.zoom_pos])
        else:
            logger.debug('Beginning of zoom stack reached')

        logger.debug('Zoom pos: {}'.format(self.zoom_pos))
        self.sigEnableBack.emit(self.zoom_pos > 0)
        self.sigEnableForward.emit(self.zoom_pos < (len(self.stack) - 1))

    @Slot()
    def zoom_forward(self):
        '''
        Slot for the forward button on the toolbar.
        '''
        logger.debug('Zooming forward')
        if self.zoom_pos < (len(self.stack) - 1):
            self.zoom_pos += 1
            self.recall_view(self.stack[self.zoom_pos])
        
        self.sigEnableBack.emit(self.zoom_pos > 0)
        self.sigEnableForward.emit(self.zoom_pos < (len(self.stack) - 1))
    