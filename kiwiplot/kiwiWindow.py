'''
'''
import os, sys
import sys
from kiwiplot import KiwiPlot, ZoomStack
from kiwiplot.qtWrapper import *
from kiwiplot.constants import IMAGE_DIR, ZOOM_MODE
from .klog import get_logger
logger = get_logger('kiwiplot.' + __name__)

LAYOUTS = ['vertical', 'v', 'horizontal', 'h']
LINK_CURSORS = True

class KiwiWindow(QMainWindow):

    def __init__(self, layout='vertical', title='Kiwi Window', statusBar=False, show=True):
        super(KiwiWindow, self).__init__()
        self.setWindowTitle(title)
        icon_path = os.path.join(IMAGE_DIR, 'kiwi_small.png')
        self.setWindowIcon(QIcon(icon_path))
        self.setStyleSheet('QToolBar{spacing:5px;};') #QStatusBar.item {border: none;}
        
        if statusBar:
            self.status_bar = QStatusBar()
            self.setStatusBar(self.status_bar)
            self.status_height = self.status_bar.minimumSize().height()
            # self.status_bar.showMessage('Home view')
        
        self.plot_list = list()
        self.cursor_list = list()

        if layout not in LAYOUTS:
            raise Exception('parameter layout unrecognized')
        if layout == 'vertical' or 'v':
            self.layout = QVBoxLayout()

            #TODO: Base this on settings
            self.layout.setContentsMargins(0,0,0,0) #tight layout
        elif layout == 'horizontal' or 'h':
            self.layout = QHBoxLayout()
            self.layout.setContentsMargins(0,0,0,0) #tight layout

        widget = QWidget()
        widget.setLayout(self.layout)
        self.setCentralWidget(widget)
        self.createActions()
        self.createToolBar()
        if show:
            self.show()
        

    def initZoomStack(self):
        #Initialize zoom stack and back/forward icons
        self.zoom_stack = ZoomStack(self.plot_list)
        self.zoom_stack.link_toolbar_actions(
            self.backAction,
            self.forwardAction,
            self.zoomHomeAction,
            self.zoomFreeAction,
            self.zoomConstrainedAction
        )
        self.zoom_stack.save_home_view() #Must be called after creating the plots


    def add_plot(self, style='white'):
        '''Add a new KiwiPlot to self.layout'''
        self.plot = KiwiPlot(style=style)
        self.layout.addWidget(self.plot)
        self.plot_list.append(self.plot) #does this create a new reference?
        return self.plot

    def get_plot(self):
        '''Return the last plot created'''
        return self.plot

    # @Slot(object)
    # def process_cursor_data(self, data):
    #     logger.debug('Cursor data: {}'.format(data))

    def createActions(self):
        '''Toolbar actions'''
        icon = QIcon(os.path.join(IMAGE_DIR, 'back.png'))
        self.backAction = QAction(icon, "Back", self, shortcut=QKeySequence.Back)
        self.backAction.setEnabled(False)
        icon = QIcon(os.path.join(IMAGE_DIR, 'forward.png'))
        self.forwardAction = QAction(icon, "Forward", self, shortcut=QKeySequence.Forward)
        self.forwardAction.setEnabled(False)
        icon = QIcon(os.path.join(IMAGE_DIR, 'zoom_fit.png'))
        self.zoomHomeAction = QAction(icon, "Zoom to fit", self, shortcut=QKeySequence.MoveToStartOfLine)
        icon = QIcon(os.path.join(IMAGE_DIR, 'zoom.png'))
        self.zoomFreeAction = QAction(icon, "Free zoom", self, shortcut="Ctrl+Z", triggered=self.zoom_free)
        self.zoomFreeAction.setCheckable(True)
        icon = QIcon(os.path.join(IMAGE_DIR, 'zoom_constrained.png'))
        self.zoomConstrainedAction = QAction(icon, "Constrained zoom", self, shortcut="Ctrl+X", triggered=self.zoom_constrained)
        self.zoomConstrainedAction.setCheckable(True)
        self.zoomConstrainedAction.setChecked(True) #default zoom mode
        self.zoom_mode = ZOOM_MODE.xZoom
        icon = QIcon(os.path.join(IMAGE_DIR, 'data_cursor.png'))
        self.dataCursorAction = QAction(icon, "Data cursor", self, shortcut="Ctrl+D",
                 triggered=self.show_cursor)
        self.dataCursorAction.setCheckable(True)
        iconfile = QIcon(os.path.join(IMAGE_DIR, 'settings_icon.png'))
        self.settingsAction = QAction(iconfile, "&Settings", self, shortcut="Ctrl+,",
                                    triggered=self.default_action)
        self.zoom_action_group = QActionGroup(self)
        self.zoom_action_group.setExclusive(True)
        self.zoom_action_group.addAction(self.zoomFreeAction)
        self.zoom_action_group.addAction(self.zoomConstrainedAction)
        
        
    def createToolBar(self):
        self.toolBar = self.addToolBar("Card")
        self.toolBar.addAction(self.backAction)
        self.toolBar.addAction(self.forwardAction)
        self.toolBar.addAction(self.zoomHomeAction)
        self.toolBar.addAction(self.zoomFreeAction)
        self.toolBar.addAction(self.zoomConstrainedAction)
        self.toolBar.addAction(self.dataCursorAction)
        self.toolBar.addAction(self.settingsAction) 

    def zoom_free(self):
        logger.debug('Setting zoom_free')
        for plot in self.plot_list:
            plot.viewbox.setZoomMode(ZOOM_MODE.freeZoom)

    def zoom_constrained(self):
        logger.debug('Setting zoom_constrained')
        for plot in self.plot_list:
            plot.viewbox.setZoomMode(ZOOM_MODE.xZoom)
    
    def show_cursor(self):
        show = self.dataCursorAction.isChecked()
        if show:
            logger.debug('Showing cursor')
            for plot in self.plot_list:
                plot.legend() #show legend
                plot.cursor_on()
                plot.cursor.blockSignals(True)
                plot.cursor.show()
                plot.cursor.cursorDataSignal.connect(self.update_cursors) #works for one cursor
                self.cursor_list.append(plot.cursor)
                # plot.cursor.sigPositionChanged.connect(self.update_cursor_pos)
                # plot.cursor.cursorDataSignal.connect(self.update_legend_text) #works for one cursor
            for plot in self.plot_list:
                plot.cursor.blockSignals(False)
                plot.cursor.forceDataSignal()

        else:
            logger.debug('Hiding cursor')
            for plot in self.plot_list:
                plot.cursor_off()
                plot._hide_legend()
            self.cursor_list = list()

            
    def update_cursors(self, data, cursor):
        '''
        Slot that is called when a cursor in self.cursor_list was moved.
        The position of all other cursors is updated.
        '''
        x, y = data
        idx = self.cursor_list.index(cursor) #get the cursor that caused the movement
        # logger.debug('update_cursor_pos: {}'.format(idx))
        x = cursor.getXPos()
        self.update_legend_text(data, cursor)

        #If cursors are linked, update the other cursors
        if LINK_CURSORS:
            cursorsToUpdate = self.cursor_list.copy()
            cursorsToUpdate.pop(idx)
            for c in cursorsToUpdate:
                c.setPos(x) #emits a signal


    # @Slot(object)
    def update_legend_text(self, data, cursor):
        '''
        '''
        x, y = data
        idx = self.cursor_list.index(cursor)
        # text = 'x = {:.3f} ms, idx: {}'.format(x[0]*1000, idx)
        # logger.debug(text)
        plot = self.plot_list[idx] #get kiwiplot to update
        
        legend_labels = list()
        for i, yval in enumerate(y):
            text = '{:.2f}'.format(yval) #text that is shown on the label
            legend_labels.append(text)
        plot.legend_box.update_legend_text(legend_labels)

        
    def default_action(self):
        print('Default action')
    
    @Slot(object)
    def update_cursor(self, line):
        point = line.pos()
        xpos = point.x()
        logger.debug(f'cursor x: {xpos}')
