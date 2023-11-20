import sys
import pyqtgraph as pg
import numpy as np
from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *
import sys

#These imports take a while
from py_vollib.black_scholes import black_scholes
import py_vollib.black_scholes.greeks.numerical as greeks
from py_vollib.black_scholes.implied_volatility import implied_volatility

from datetime import datetime
import py_vollib_vectorized  #Apply patch to pyvollib
import os
import timeit

DIR_PATH = os.path.dirname(os.path.realpath(__file__))
SPOT = 4240
RFR = 0.052
expiry = '20240516'


class CustomAxis(pg.AxisItem):
    '''
    The values are basically the values of the ticks on the bottom x axis.
    These are transformed here into percentages.
    '''
    def tickStrings(self, values, scale, spacing):
        ret = list()
        for v in values:
            print(v)
            if v > 0:
                percent_val = (v - SPOT) / SPOT * 100
                print(percent_val)
                ret.append('{:.1f}%'.format(percent_val))
            else:
                ret.append('')
        return ret
    

def get_option_data():
    # Load the data from the text file
    p = os.path.join(DIR_PATH, 'option_data.txt')   
    data = np.loadtxt(p, delimiter=',')

    # Split the data into separate arrays
    strikes = data[:, 0]
    mid = data[:, 1]
    return strikes, mid


def calc_dte():
    # Calculate the DTE
    exp_date = datetime.strptime(expiry, '%Y%m%d')
    current_date = datetime.now()
    dte = (exp_date - current_date).days + 1
    return dte


def calc_iv(dte):
    # Calculate the implied volatility using the slow method
    ivs = []
    for i in range(len(strikes)):
        iv = implied_volatility(mid[i], SPOT, strikes[i], dte/365, RFR, 'p')
        ivs.append(iv)
    return ivs


def calc_iv_v(mid, SPOT, strikes, dte, RFR, flag='p'):
    dte = calc_dte()
    # iv = py_vollib_vectorized.vectorized_implied_volatility(mid, SPOT, strikes, dte/365, RFR)
    iv = py_vollib_vectorized.vectorized_implied_volatility(mid, SPOT, strikes, dte/365, RFR, flag,
                                  return_as="array")
    return iv


def calc_delta_v(iv, SPOT, strikes, dte, RFR, flag='p'):
    return py_vollib_vectorized.vectorized_delta(flag, SPOT, strikes, dte/365, RFR, iv, model='black_scholes', return_as='numpy')


if __name__ == '__main__':

    app = pg.mkQApp("Gradiant Layout Example")
    view = pg.GraphicsView()
    layout = pg.GraphicsLayout(border=(100,100,100))
    view.setCentralItem(layout)
    view.show()
    view.setWindowTitle('pyqtgraph example: GraphicsLayout')
    view.resize(800,600)

    fig1 = layout.addPlot(title='Price')
    fig1.showGrid(True, True) #show x and y grids
    layout.nextRow()
    fig2 = layout.addPlot(title='Gamma')
    fig2.showGrid(True, True) #show x and y grids
    fig1.setXLink(fig2)

    #Add custom top axis
    #https://stackoverflow.com/questions/33352694/pyqtgraph-multiple-horizontal-axes
    fig2.layout.removeItem(fig2.getAxis('top'))
    caxis = CustomAxis(orientation='top', parent=fig2)
    # caxis.setLabel('inverted')
    caxis.linkToView(fig2.vb)
    fig2.axes['top']['item'] = caxis
    fig2.layout.addItem(caxis, 1, 1)


    strikes, mid = get_option_data()
    dte = 224 #5 Oct 23 calc_dte()
    iv = calc_iv_v(mid, SPOT, strikes, dte, RFR, flag='p')
    gamma = py_vollib_vectorized.vectorized_gamma('p', SPOT, strikes, dte/365, RFR, iv, return_as='numpy')

    fig1.addLegend() 
    fig1.plot(strikes, mid, name='gamma')
    

    fig2.plot(strikes, gamma)

    sys.exit(app.exec())

