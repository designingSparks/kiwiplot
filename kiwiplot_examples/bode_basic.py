import pyqtgraph as pg
import numpy as np
import os


def calc_tf(f):
    '''
    Returns the magnitude and phase response of a low-pass filter
    '''
    s = 2.0j*np.pi*f
    fc = 100
    tau = 1/(2*np.pi*fc)
    tf = 1/(s*tau + 1)
    mag = 20*np.log10(abs(tf))
    phase = (np.angle(tf))*180/np.pi
    return mag, phase

pg.mkQApp()
pw = pg.PlotWidget()
pw.show()
pi = pw.getPlotItem()
pi.setLogMode(x=True, y=False)
f = np.logspace(1, 3, 50)
mag1, phase1 = calc_tf(f)
pi.plot(f, mag1, symbol='o')
pi.showGrid (True, True)
pg.exec()