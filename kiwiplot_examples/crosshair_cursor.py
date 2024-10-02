'''
'''
import os, sys
import sys
import numpy as np
from kiwiplot import KiwiPlot, plotstyle
from kiwiplot.qtWrapper import *
from kiwiplot.constants import HLINE_TOP, VLINE_RIGHT
import pyqtgraph as pg #must come after importing kiwiplot.qt

_this_file = os.path.realpath(sys.argv[0])
BASEDIR = os.path.dirname(_this_file)
IMAGE_DIR = os.path.join(BASEDIR, 'images')


def get_bessel_data(x):
    import scipy.special as spl
    y1 = spl.jv(0,x)
    y2 = spl.jv(1,x)
    return y1, y2

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setWindowTitle('Cursor Crosshair Example')
        self.setStyleSheet('QToolBar{spacing:5px;};') #QStatusBar.item {border: none;}
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_height = self.status_bar.minimumSize().height()
        self.plotwidget1 = KiwiPlot(style='white')
        self.update_plot()
        vbox = QVBoxLayout()
        widget = QWidget()
        vbox.addWidget(self.plotwidget1)
        widget.setLayout(vbox)
        self.setCentralWidget(widget)
        self.show()


    def add_cursor_labels(self):
        # labelOpts1={'position':0.03, 'color': 'w', 'fill': (0x1F, 0x77, 0xB4, 200), 'movable': True} #bottom
        labelOpts1={'position':0.03, 'color': 'w', 'fill': (0x1F, 0x77, 0xB4, 200)} 
        format1 = lambda x: f'{x:.2f}'
        format2 = lambda x: f'{x:.3f}'
        self.plotwidget1.cursor.add_label('', format1, labelOpts1) #cursor label is in bottom left
        self.plotwidget1.hcursor.add_label('', format2, labelOpts1)
        # self.plotwidget1.cursor.labels[0].set_left(True) #alternative positioning
        # self.plotwidget1.hcursor.labels[0].set_below(True)


    def update_plot(self):
        t = np.linspace(0,20,100)
        y1, y2 = get_bessel_data(t)
        self.plotwidget1.plot(t,y1, name='y1')
        self.plotwidget1.plot(t,y2, name='y2')

        self.plotwidget1.grid()
        self.plotwidget1.show_legend()
        self.plotwidget1.set_xlabel('Time', 's') #Can also specify the base unit
        self.plotwidget1.set_ylabel('Magnitude')
        self.plotwidget1.set_title('Bessel Function')
        self.plotwidget1.cursor_on(hcursor=True)
        self.add_cursor_labels()
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