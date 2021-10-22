from prettyplot.pplogger import get_logger
logger = get_logger(__name__)

class ZoomStack():

    def __init__(self, vbox_list):
        logger.debug('Initializing zoom stack')
        self.vbox_list = vbox_list
        self.stack = list() #list of tuples: 'xMin', 'xMax', 'yMin', 'yMax'
        self.zoom_pos = 0


    def addToZoomStack(self, viewbox, ax):
        idx = self.vbox_list.index(viewbox) 
        logger.debug('Adding to zoom stack. Viewbox: {}'.format(idx))
        self.stack.append((idx, ax))
        logger.debug('Number of items in stack: {}'.format(len(self.stack)))
        
        # n = len(self.zoom_stack) - self.zoom_pos - 1
        # if n:
        #     logger.debug('Pruning zoom stack. n={}'.format(n))
        #     self.zoom_stack = self.zoom_stack[:self.zoom_pos+1]

        # self.stack.append(ax)
        # self.zoom_pos += 1
        # logger.debug('Updated zoom stack: {}'.format(ax))
        # logger.debug('zoom_pos: {}, len zoom_stack: {}'.format(self.zoom_pos, len(self.zoom_stack)))
        # self.sigZoomStackStart.emit(self.zoom_pos > 0)
        # self.sigZoomStackEnd.emit(self.zoom_pos < (len(self.zoom_stack) - 1))