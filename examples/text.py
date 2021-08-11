from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *
import sys, os
import numpy as np
import pyqtgraph as pg
pg.setConfigOption('background', 'w')
pg.setConfigOption('antialias', True) #Plotted curve looks nicer


class MainWindow(QMainWindow):
    
    def __init__(self):
        super(MainWindow, self).__init__()
        self.plotwidget1 = pg.PlotWidget()
        self.plot_item = self.plotwidget1.getPlotItem()
        vbox1 = QVBoxLayout()
        vbox1.addWidget(self.plotwidget1)
        widget1 = QWidget()
        widget1.setLayout(vbox1)
        self.setCentralWidget(widget1)
        self.show()
        self.raise_()
        self.plot()
        self.set_plot_labels()

    def plot(self):
        t = np.linspace(0, 20e-3, 100)
        y1 = 2*np.sin(2*np.pi*50*t)
        pen = pg.functions.mkPen({'color': '#1F77B4', 'width': 2})
        self.plot_item.plot(t, y1, pen=pen)

    def set_plot_labels(self):
        label_style = {'color': 'k', 'font-size': '10pt'}
        title_style = {'color': 'k', 'size': '12pt'}
        # self.plot_item.setLabel('left', 'Magnitude', **label_style)
        # self.plot_item.setTitle('Sine wave demo', **title_style)

        axis = self.plot_item.getAxis('bottom')
        # axis.showLabel(True)
        axis.label.setFont(QFont("Roboto"))
        # axis.label.setPlainText('Time')
        # axis._adjustSize()
        # axis.picture = None
        # axis.update()
        # font = QFont("Roboto")
        # axis.setTickFont(font) #Just changes the tick font

        axis.setLabel('Time', 's', **label_style)

    # def _updateLabel(self):
    #     """Internal method to update the label according to the text"""
    #     self.label = QtGui.QGraphicsTextItem(self)
    #     self.label.setHtml(self.labelString())
    #     self._adjustSize()
    #     self.picture = None
    #     self.update()

if __name__ == '__main__':
    print('In main')
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    sys.exit(app.exec_())