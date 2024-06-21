'''
'''
import os, sys
import sys
import numpy as np
from kiwiplot import KiwiPlot, plotstyle
from kiwiplot.qtWrapper import *
import pyqtgraph as pg #must come after importing kiwiplot.qt
# pg.setConfigOptions(useOpenGL=True) #works but anitaliasing stops working
from pyqtgraph.graphicsItems.ViewBox import ViewBox
# from kiwiplot.ViewBox import ViewBox #js
from kiwiplot.zoom_stack import ZoomStack
_this_file = os.path.realpath(sys.argv[0])
BASEDIR = os.path.dirname(_this_file)
IMAGE_DIR = os.path.join(BASEDIR, 'images')

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setWindowTitle('Plot Example')
        self.setStyleSheet('QToolBar{spacing:5px;};') #QStatusBar.item {border: none;}
        
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_height = self.status_bar.minimumSize().height()
        self.status_bar.showMessage('Home view')
        
        # self.plotwidget = PlotWidget(updateLabelfn = self.status_bar.showMessage)
        self.plotwidget1 = KiwiPlot(style='grey')
        # self.plotwidget1.cursorDataSignal.connect(self.process_cursor_data)
        self.plotwidget2 = KiwiPlot(style='white')

        #Set mouse mode to rectangle (zoom) mode rather than the default pan mode
        #TODO: Shift this into the constructor of zoom stack.
        self.plotwidget1.plotItem.vb.setMouseMode(pg.ViewBox.RectMode)
        self.plotwidget2.plotItem.vb.setMouseMode(pg.ViewBox.RectMode)
        self.plotwidget2.link_x(self.plotwidget1) #Link X axes
        

        vbox = QVBoxLayout()
        widget = QWidget()
        vbox.addWidget(self.plotwidget1)
        vbox.addWidget(self.plotwidget2)
        widget.setLayout(vbox)
        self.setCentralWidget(widget)

        self.createActions()
        self.createToolBar()

        #Initialize zoom stack and back/forward icons.
        #TODO: Need modified zoom stack
        # self.zoom_stack = ZoomStack([self.plotwidget1, self.plotwidget2])
        # self.zoom_stack.link_toolbar_actions(
        #     self.backAction,
        #     self.forwardAction,
        #     self.zoomHomeAction,
        #     self.zoomFreeAction,
        #     self.zoomConstrainedAction
        # )
        self.show()
        self.plot_data()
        
        #TODO: Need modified zoom stack
        # self.zoom_stack.save_home_view() #Must be called after creating the plots



    def plot_data(self):
        t = np.linspace(0, 20e-3, 100)
        y1 = 2*np.sin(2*np.pi*50*t)
        y2 = np.sin(2*np.pi*100*t)
        y3 = 0.5*np.sin(2*np.pi*150*t)
        y4 = 0.25*np.sin(2*np.pi*200*t)

        #Legend created using name keyword
        self.plotwidget1.plot(t,y1, name='y1')
        self.plotwidget1.plot(t,y2, name='y2')
        self.plotwidget1.plot(t,y3, name='y3')
        self.plotwidget1.plot(t,y4, name='y4')
        self.plotwidget1.grid()

        self.plotwidget1.set_xlabel('Time (ms)')
        self.plotwidget1.set_ylabel('Magnitude')
        self.plotwidget1.show_legend()
        self.plotwidget1.set_title('Graph 1')
        self.plotwidget1.cursor_on()

        # self.plotwidget2.set_linecolors(plotstyle.palette_2)
        for i in range(1, 6):
            self.plotwidget2.plot(t,y1*i)
        self.plotwidget2.grid()
        self.plotwidget2.show_legend(['y1','y2','y3','y4','y5']) 
        self.plotwidget2.cursor_on()
    
    @Slot(object)
    def process_cursor_data(self, data):
        logger.debug('Cursor data: {}'.format(data))

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
        self.zoomFreeAction = QAction(icon, "Free zoom", self, shortcut="Ctrl+Z")
        self.zoomFreeAction.setCheckable(True)
        icon = QIcon(os.path.join(IMAGE_DIR, 'zoom_constrained.png'))
        self.zoomConstrainedAction = QAction(icon, "Constrained zoom", self, shortcut="Ctrl+X")
        self.zoomConstrainedAction.setCheckable(True)
        self.zoomConstrainedAction.setChecked(True) #default zoom mode
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
        self.plotwidget.viewbox.setZoomMode(pg.ViewBox.freeZoom)
        
    def zoom_constrained(self):
        logger.debug('Setting zoom_constrained')
        self.plotwidget.viewbox.setZoomMode(pg.ViewBox.xZoom)
    
    
    def show_cursor(self):
        show = self.dataCursorAction.isChecked()
        if show:
            logger.debug('Showing cursor')
            self.plotwidget1.cursor_on()
        else:
            logger.debug('Hiding cursor')
            self.plotwidget1.cursor_off ()
            self.status_bar.showMessage('')
            
    def default_action(self):
        print('Default action')
    
    @Slot(object)
    def update_cursor(self, line):
        point = line.pos()
        xpos = point.x()
        logger.debug(f'cursor x: {xpos}')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    sys.exit(app.exec_())