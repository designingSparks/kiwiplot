from prettyplot.qtWrapper import *
from prettyplot import PrettyPlot
import pyqtgraph as pg
import numpy as np
from prettyplot.simpleVector import SimpleVector
from prettyplot.pplogger import get_logger
logger = get_logger( __name__) 

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.plotwidget = PrettyPlot(style='grey')
        self.plotwidget.setAspectLocked()
        vbox1 = QVBoxLayout()
        vbox1.addWidget(self.plotwidget)
        widget1 = QWidget()
        widget1.setLayout(vbox1)
        self.setCentralWidget(widget1)

        
        grid_color = QColor(self.plotwidget.graphstyle['grid'])

        #Default vector
        vector1 = SimpleVector(pen=grid_color)
        self.plotwidget.plot_item.addItem(vector1)

        #How to shift vector position and angle dynamically
        vector2 = SimpleVector(pen=grid_color)
        vector2.setPos(QPointF(1,1))
        vector2.setAngle(45)
        self.plotwidget.plot_item.addItem(vector2)

        #Initialize vector using all possible parameters
        vector3 = SimpleVector(tail=(0,1), length=0.5, angle=90, pen=grid_color)
        self.plotwidget.plot_item.addItem(vector3)

        self.show()

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    sys.exit(app.exec_())