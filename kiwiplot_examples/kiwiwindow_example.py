'''
'''
import sys
import numpy as np
from kiwiplot.kiwiWindow import KiwiWindow
from kiwiplot.qtWrapper import *

def get_bessel_data(x):
    import scipy.special as spl
    y1 = spl.jv(0,x)
    y2 = spl.jv(1,x)
    y3 = spl.jv(2,x)
    y4 = spl.jv(3,x)
    return y1, y2, y3, y4

if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = KiwiWindow()
    fig1 = win.add_plot()
    fig2 = win.add_plot()
    # fig3 = win.add_plot()
    fig2.link_x(fig1)
    # fig3.link_x(fig1)
    t = np.linspace(0,20,100)
    y1, y2, y3, y4 = get_bessel_data(t)
    fig1.plot(t,y1,t,y2,t,y3,t,y4)
    fig2.plot(t,2*y1,t,2*y2,t,2*y3,t,2*y4)
    # fig3.plot(t,3*y1,t,3*y2,t,3*y3,t,3*y4)
    fig1.grid(True)
    fig2.grid(True)
    # fig3.grid(True)
    win.initZoomStack()
    sys.exit(app.exec_())