'''
'''
import os, sys
import sys
import numpy as np
from prettyplot import PrettyPlot, plotstyle
from prettyplot.qtWrapper import *
import pyqtgraph as pg #must come after importing prettyplot.qt

_this_file = os.path.realpath(sys.argv[0])
BASEDIR = os.path.dirname(_this_file)
IMAGE_DIR = os.path.join(BASEDIR, 'images')

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setWindowTitle('Plot Example')
        self.setStyleSheet('QToolBar{spacing:5px;};') #QStatusBar.item {border: none;}
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_height = self.status_bar.minimumSize().height()
        self.plotwidget1 = PrettyPlot(style='grey')
        self.update_plot()
        vbox = QVBoxLayout()
        widget = QWidget()
        vbox.addWidget(self.plotwidget1)
        widget.setLayout(vbox)
        self.setCentralWidget(widget)
        self.show()

    def update_plot(self):
        t = np.linspace(0, 20e-3, 100)
        y1 = 2*np.sin(2*np.pi*50*t)
        y2 = np.sin(2*np.pi*100*t)
        y3 = 0.5*np.sin(2*np.pi*150*t)
        y4 = 0.25*np.sin(2*np.pi*200*t)
        # t = t*1000 #convert to ms

        #Legend uses name keyword in plot()
        self.plotwidget1.plot(t,y1, name='y1')
        self.plotwidget1.plot(t,y2, name='y2')
        self.plotwidget1.plot(t,y3, name='y3')
        self.plotwidget1.plot(t,y4, name='y4')
        self.plotwidget1.grid()
        self.plotwidget1.legend()
        self.plotwidget1.set_xlabel('Time', 's') #Can also specify the base unit
        self.plotwidget1.set_ylabel('Magnitude')
        self.plotwidget1.set_title('Sine Wave Magnitude')
        self.plotwidget1.add_cursor()
        self.plotwidget1.cursor_list[0].cursorDataSignal.connect(self.process_cursor_data)


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
    sys.exit(app.exec_())