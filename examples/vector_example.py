from kiwiplot.qtWrapper import *
from kiwiplot import KiwiPlot
import pyqtgraph.functions as fn
from kiwiplot.simpleVector import SimpleVector


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.plotwidget = KiwiPlot(style='grey')
        self.plotwidget.setAspectLocked()
        vbox1 = QVBoxLayout()
        vbox1.addWidget(self.plotwidget)
        widget1 = QWidget()
        widget1.setLayout(vbox1)
        self.setCentralWidget(widget1)

        pen = fn.mkPen({'color': self.plotwidget.graphstyle['grid'], 'width': 1.5})
        vector1 = SimpleVector(pen)
        vector2 = SimpleVector(pen)
        vector2.setPos((1,1))
        vector2.setAngle(45)
        vector3 = SimpleVector(pen, tail=(0,1), length=2, angle=90)

        self.plotwidget.plot_item.addItem(vector1)
        self.plotwidget.plot_item.addItem(vector2)
        self.plotwidget.plot_item.addItem(vector3)

        self.show()

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    sys.exit(app.exec_())