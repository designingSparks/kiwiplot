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
        vbox1 = QVBoxLayout()
        vbox1.addWidget(self.plotwidget)
        widget1 = QWidget()
        widget1.setLayout(vbox1)
        self.setCentralWidget(widget1)

        # Random data
        theta = np.linspace(0, 2*np.pi, 100)
        radius = np.random.normal(loc=10, size=100)
        x = radius*np.cos(theta) # Transform to cartesian 
        y = radius*np.sin(theta)
        x[-1] = x[0]
        y[-1] = y[0]
        self.plotwidget.plot(x, y)
        self.show()
        self.add_scatter_dot()

        
    def add_scatter_dot(self):
        '''
        Example of how to add a scatter point.
        '''
        mybrush = pg.mkBrush('#1F77B4') #This makes the dot solid
        scatter = pg.ScatterPlotItem(pen=pg.mkPen(width=1, color='#1F77B4'), symbol='o', brush=mybrush, size=10) #size is the diameter
        self.plotwidget.plotItem.addItem(scatter)
        scatter.setData([0],[0])


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    sys.exit(app.exec_())