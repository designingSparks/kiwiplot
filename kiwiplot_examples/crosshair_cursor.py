'''
'''
import os, sys
import sys
import numpy as np
from kiwiplot import KiwiPlot, plotstyle
from kiwiplot.qtWrapper import *
import pyqtgraph as pg #must come after importing kiwiplot.qt

_this_file = os.path.realpath(sys.argv[0])
BASEDIR = os.path.dirname(_this_file)
IMAGE_DIR = os.path.join(BASEDIR, 'images')


def get_bessel_data(x):
    import scipy.special as spl
    y1 = spl.jv(0,x)
    return y1

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setWindowTitle('Cursor Example')
        self.setStyleSheet('QToolBar{spacing:5px;};') #QStatusBar.item {border: none;}
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_height = self.status_bar.minimumSize().height()
        self.plotwidget1 = KiwiPlot(style='dark')
        self.update_plot()
        vbox = QVBoxLayout()
        widget = QWidget()
        vbox.addWidget(self.plotwidget1)
        widget.setLayout(vbox)
        self.setCentralWidget(widget)
        self.show()

    def update_plot(self):
        t = np.linspace(0,20,100)
        y1 = get_bessel_data(t)
        self.plotwidget1.plot(t,y1, name='y1')

        self.plotwidget1.grid()
        self.plotwidget1.show_legend()
        self.plotwidget1.set_xlabel('Time', 's') #Can also specify the base unit
        self.plotwidget1.set_ylabel('Magnitude')
        self.plotwidget1.set_title('Sine Wave Magnitude')
        self.plotwidget1.cursor_on(crosshair=True)
        self.plotwidget1.cursor.cursorDataSignal.connect(self.process_cursor_data)


    @Slot(object)
    def process_cursor_data(self, data):

        #x value shown on status bar
        x, y = data
        text = 'x = {:.3f} ms'.format(x[0]*1000)
        self.status_bar.showMessage(text)

        #y values shown in legend box
        legend_labels = list()
        for i, yval in enumerate(y):
            text = 'y{}: {:.2f}'.format(i+1, yval)
            legend_labels.append(text)
        self.plotwidget1.legend_box.update_legend_text(legend_labels)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    sys.exit(app.exec())