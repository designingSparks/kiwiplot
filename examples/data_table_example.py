'''
'''
import os, sys
import sys
import numpy as np
from prettyplot import PrettyPlot, plotstyle
from prettyplot.qtWrapper import *
import pyqtgraph as pg #must come after importing prettyplot.qt
from prettyplot.data_table import DataTable

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setWindowTitle('Data Table Example')
        self.setStyleSheet('QToolBar{spacing:5px;};') #QStatusBar.item {border: none;}
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_height = self.status_bar.minimumSize().height()
        self.plotwidget1 = PrettyPlot(style='grey')
        self.data_table = DataTable(['y1', 'y2', 'y3', 'y4'], ['x', 'Val'])
        self.update_plot()

        vbox = QVBoxLayout()
        widget = QWidget()
        vbox.addWidget(self.plotwidget1)
        vbox.addWidget(self.data_table)
        widget.setLayout(vbox)
        self.setCentralWidget(widget)
        self.show()

    def update_plot(self):
        t = np.linspace(0, 20e-3, 100)
        y1 = 2*np.sin(2*np.pi*50*t)
        y2 = np.sin(2*np.pi*100*t)
        y3 = 0.5*np.sin(2*np.pi*150*t)
        y4 = 0.25*np.sin(2*np.pi*200*t)
        t = t*1000 #convert to ms

        #Legend uses name keyword in plot()
        self.plotwidget1.plot(t,y1, name='y1')
        self.plotwidget1.plot(t,y2, name='y2')
        self.plotwidget1.plot(t,y3, name='y3')
        self.plotwidget1.plot(t,y4, name='y4')
        self.plotwidget1.grid()
        self.plotwidget1.legend()
        self.plotwidget1.set_xlabel('Time (ms)')
        self.plotwidget1.set_ylabel('Magnitude')
        self.plotwidget1.add_cursor(name='x1')
        self.plotwidget1.cursor_list[0].cursorDataSignal.connect(self.data_table.update_data)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    sys.exit(app.exec_())
