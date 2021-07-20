import sys, os
from prettyplot import PrettyPlot
from prettyplot.qtWrapper import QApplication

if __name__ == '__main__':
    app = QApplication(sys.argv)
    fig = PrettyPlot()
    import numpy as np
    t = np.linspace(0, 20e-3, 100)
    y1 = 2*np.sin(2*np.pi*50*t)
    fig.plot(t,y1, name='y1')
    sys.exit(app.exec_())