import sys
import numpy as np
from kiwiplot.kiwiWindow import KiwiWindow
from kiwiplot.qtWrapper import *

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

if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = KiwiWindow(title='Bode plot of low-pass filter')
    win.resize(600, 400)
    fig1 = win.add_plot()
    fig2 = win.add_plot()
    fig2.link_x(fig1)
    fig1.plot_item.setLogMode(x=True)
    fig2.plot_item.setLogMode(x=True)
    

    f = np.logspace(1, 3, 100)
    mag, phase = calc_tf(f)
    fig1.plot(f, mag)
    fig2.plot(f, phase)
    fig1.grid(True)
    fig2.grid(True)
    fig1.set_ylabel('Magnitude (dB)')
    fig2.set_ylabel('Phase (deg)')
    fig2.set_xlabel('Frequency (Hz)')
    win.initZoomStack()
    sys.exit(app.exec())