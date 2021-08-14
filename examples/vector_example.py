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

        nlines = 6
        angles = np.arange(nlines)*360/nlines
        for a in angles:
            grid_color = QColor(self.plotwidget.graphstyle['grid'])
            arrow = SimpleVector(angle=a, pen=grid_color)
            self.plotwidget.plot_item.addItem(arrow)

        self.show()

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    sys.exit(app.exec_())