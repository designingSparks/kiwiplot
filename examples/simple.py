import sys, os
from prettyplot import PrettyPlot
from prettyplot.qtWrapper import QApplication
import numpy as np

if __name__ == '__main__':
    app = QApplication(sys.argv)
    fig = PrettyPlot(style='white')
    fig.setWindowTitle('Vanilla prettyplot')
    t = np.linspace(0, 20e-3, 100)
    y1 = 2*np.sin(2*np.pi*50*t)
    y2 = 1.5*np.sin(2*np.pi*50*t)
    y3 = 1*np.sin(2*np.pi*50*t)
    fig.plot(t,y1, name='y1')
    fig.plot(t,y2, name='y2')
    fig.plot(t,y3, name='y3')
    fig.grid()
    fig.legend()
    sys.exit(app.exec_())