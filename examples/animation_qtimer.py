'''
Simple animation using the QTimer timeout interrupt.
TODO: Add a round circle at the tip of the curve.
'''
from prettyplot.qtWrapper import *
from prettyplot.polarPlot import PolarPlot
import pyqtgraph as pg
import numpy as np
from prettyplot.pplogger import get_logger
logger = get_logger( __name__) 

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.plotwidget = PolarPlot(style='grey', nlines=8)
        self.plotwidget.linewidth = 2
        self.plotwidget.xlim([-1,1])
        self.plotwidget.ylim([-1,1])
        vbox1 = QVBoxLayout()
        vbox1.addWidget(self.plotwidget)
        widget1 = QWidget()
        widget1.setLayout(vbox1)
        self.setCentralWidget(widget1)

        self.timer = QTimer()
        self.timer.timeout.connect(self.on_timer)
        self.plot_index = 0

        #Data
        theta = np.linspace(0, np.pi, 500)
        radius = np.cos(21*theta)
        self.x = radius*np.cos(theta) # Transform to cartesian 
        self.y = radius*np.sin(theta)
        self.plotwidget.plot([self.x[0]], [self.y[0]]) #Plot the first point to create the curve
        self.show()
        self.timer.start(20) #ms

    def on_timer(self):
        x = self.x[0:self.plot_index]
        y = self.y[0:self.plot_index]
        self.plotwidget.update_plot(0, x, y)
        self.plot_index += 1
        logger.debug(self.plot_index)
        if self.plot_index == 500:
            self.timer.stop()
            logger.debug('Stopping timer')


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    sys.exit(app.exec_())