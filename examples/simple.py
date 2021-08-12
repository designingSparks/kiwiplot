'''
Plots three separate figures to show the three different graph style types
'''
import sys, os
from prettyplot import PrettyPlot
from prettyplot.qtWrapper import QApplication
import numpy as np

def get_sine_data(t):
    y1 = 2*np.sin(2*np.pi*50*t)
    y2 = 1.5*np.sin(2*np.pi*50*t)
    y3 = 1*np.sin(2*np.pi*50*t)
    y4 = 0.5*np.sin(2*np.pi*50*t)
    return y1, y2, y3, y4

def get_bessel_data(x):
    import scipy.special as spl
    y1 = spl.jv(0,x)
    y2 = spl.jv(1,x)
    y3 = spl.jv(2,x)
    y4 = spl.jv(3,x)
    y5 = spl.jv(5,x)
    y6 = spl.jv(6,x)
    return y1, y2, y3, y4, y5, y6

def update_plot(fig):
    # t = np.linspace(0, 20e-3, 100)
    # y1, y2, y3, y4 = get_sine_data(t)
    t = np.linspace(0,20,100)
    y1, y2, y3, y4, y5, y6 = get_bessel_data(t)
    fig.plot(t,y1, name='y1')
    fig.plot(t,y2, name='y2')
    fig.plot(t,y3, name='y3')
    fig.plot(t,y4, name='y4')
    fig.plot(t,y5, name='y5')
    fig.plot(t,y6, name='y6')
    fig.grid()
    fig.legend()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    fig1 = PrettyPlot()
    fig1.setWindowTitle('Style default')
    update_plot(fig1)
    fig2 = PrettyPlot(style='grey')
    fig2.setWindowTitle('Style grey')
    update_plot(fig2)
    fig3 = PrettyPlot(style='dark')
    fig3.setWindowTitle('Style dark')
    update_plot(fig3)
    sys.exit(app.exec_())