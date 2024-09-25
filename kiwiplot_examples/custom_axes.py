'''
This example shows how to use custom axis items with KiwiPlot.
With this approach, you need to provide all axisItems needed for the plot, not just the axis you want to customize.

TODO: In the init function of CustomAxis, use the kiwiplot style for the font size and type.
'''
import sys, os
from kiwiplot import KiwiPlot
from kiwiplot.qtWrapper import QApplication
import numpy as np
import pyqtgraph as pg
from kiwiplot.qtWrapper import *

format_comma = lambda x: f'{x:,.0f}'
format_percent_deviation = lambda x: f'{(x - 10) / 10 * 100:.2f}%'
format_default = lambda x: f'{x:g}'  # Default formatting, 'g' for general format

class CustomAxis(pg.AxisItem):
    def __init__(self, format_func, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.format_func = format_func
        self.setTextPen('k')  # 'k' => black
        font = QFont("Roboto", 8)
        self.setTickFont(font)

    def tickStrings(self, values, scale, spacing):
        return [self.format_func(value) for value in values]


def get_sine_data(t):
    y1 = 2*np.sin(2*np.pi*50*t)
    y2 = 1.5*np.sin(2*np.pi*50*t)
    y3 = 1*np.sin(2*np.pi*50*t)
    y4 = 0.5*np.sin(2*np.pi*50*t)
    return y1, y2, y3, y4

def get_bessel_data(x):
    import scipy.special as spl
    GAIN = 1e6
    y1 = spl.jv(0,x)*GAIN
    y2 = spl.jv(1,x)*GAIN
    y3 = spl.jv(2,x)*GAIN
    y4 = spl.jv(3,x)*GAIN
    y5 = spl.jv(5,x)*GAIN
    y6 = spl.jv(6,x)*GAIN
    return y1, y2, y3, y4, y5, y6


def update_plot(fig):
    t = np.linspace(0,20,100)
    y1, y2, y3, y4, y5, y6 = get_bessel_data(t)
    fig.plot(t,y1, name='y1')
    fig.plot(t,y2, name='y2')
    fig.plot(t,y3, name='y3')
    fig.plot(t,y4, name='y4')
    fig.plot(t,y5, name='y5')
    fig.plot(t,y6, name='y6')
    fig.grid()
    fig.show_legend()
    fig.show_label('Bessel Curves')

    #Limits the zoom extents when zooming with the mouse scroll wheel
    #This must be done after the plot is drawn
    range_ = fig.viewbox.viewRange() 
    fig.viewbox.setLimits(xMin=range_[0][0], xMax=range_[0][1],   
                                yMin=range_[1][0], yMax=range_[1][1]) 

if __name__ == '__main__':
    app = QApplication(sys.argv)
    fig1 = KiwiPlot()
    fig1.setWindowTitle('Default style')
    la = CustomAxis(format_comma, orientation='left')
    la.setWidth(60)
    ta = CustomAxis(format_percent_deviation, orientation='top')
    ba = CustomAxis(format_default, orientation='bottom')

    #When setAxisItems is called, all other axisItems are removed. Therefore, you must
    #provide all axisItems needed for the plot.
    fig1.plotItem.setAxisItems(axisItems={'top': ta, 'bottom': ba, 'left': la})
    update_plot(fig1)
    sys.exit(app.exec())