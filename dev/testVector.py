#Test debugVector, which inherits pg.GraphicsObject 

import sys
from prettyplot.qtWrapper import *
from prettyplot.simpleVector import SimpleVector
from pyqtgraph.graphicsItems.InfiniteLine import InfiniteLine
from pyqtgraph.Point import Point
from prettyplot.debugVector import DebugVector
from prettyplot import PrettyPlot


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
        self.show()

        vector1 = DebugVector()
        vector2 = DebugVector()
        vector2.setAngle(45)
        vector3 = DebugVector()
        vector3.setAngle(90)
        vector3.setPos((0,2))
        self.plotwidget.plotItem.addItem(vector1)
        self.plotwidget.plotItem.addItem(vector2)
        self.plotwidget.plotItem.addItem(vector3)

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    sys.exit(app.exec_())
