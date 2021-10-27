'''
Simple animation of a polar plot using the QTimer timeout interrupt to draw the curve.
A scatterplot item, i.e. dot is drawn at the head of the curve.
'''
from kiwiplot.qtWrapper import *
from kiwiplot.polarPlot import PolarPlot
import pyqtgraph as pg
import numpy as np
from kiwiplot.pplogger import get_logger
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

        #Curve to animate
        theta = np.linspace(0, np.pi, 500)
        radius = np.cos(21*theta)
        self.x = radius*np.cos(theta) # Transform to cartesian 
        self.y = radius*np.sin(theta)
        self.plotwidget.plot([self.x[0]], [self.y[0]]) #Plot the first point to create the curve, otherwise update_plot() will not work

        #Scatterplot dot is used at the head of the animation
        color = self.plotwidget.linecolors[0]
        mybrush = pg.mkBrush(color) #fill
        self.scatter_dot = pg.ScatterPlotItem(pen=pg.mkPen(width=1, color=color), symbol='o', brush=mybrush, size=8)
        self.plotwidget.plotItem.addItem(self.scatter_dot)

        self.show()
        self.timer.start(20) #ms

    def on_timer(self):
        x = self.x[0:self.plot_index]
        y = self.y[0:self.plot_index]
        x_head = self.x[self.plot_index]
        y_head = self.y[self.plot_index]
        self.plotwidget.update_plot(0, x, y)
        # self.plotwidget.update_plot(1, [x_head], [y_head]) #also works
        self.scatter_dot.setData([x_head], [y_head])
        self.plot_index += 1
        logger.debug(self.plot_index)

        if self.plot_index == 500:
            self.timer.stop()
            logger.debug('Stopping timer')
            self.plotwidget.removeItem(self.scatter_dot)

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    sys.exit(app.exec_())