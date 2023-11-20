import pyqtgraph as pg
from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *
import numpy as np
import sys
from dual_axis2 import AxisItemScaleFunction

class AxisItemScaleFunction(pg.AxisItem):
    """Extension of pyqtgraph AxisItem which allows the axis tick labels to be
    transformed using a user-specified function.

    Typical use would be to display the same axis data in two different unit
    systems. For example, temperature in C and F, or light wavelength as well as
    photon energy.

    Note that the axis range and scale is not changed, only the calculation of
    the axis tick labels."""

    def __init__(self, orientation, pen=None, linkView=None, parent=None, maxTickLength=-5, showValues=True, scalefunc=lambda x: x):
        self.scalefunc = scalefunc
        pg.AxisItem.__init__(self, orientation, pen=pen, linkView=linkView, parent=parent, maxTickLength=maxTickLength, showValues=showValues)

    def tickStrings(self, values, scale, spacing):
        """Generates the strings to use for tick labels."""

        if self.scalefunc is None:
            strings = []
            for v in values:
                vs = v * scale
                # if abs(vs) < .001 or abs(vs) >= 10000:
                #     vstr = "%g" % vs
                # else:
                #     vstr = ("%%0.%df" % places) % vs
                vstr = '{}'.format(v)
                strings.append(vstr)
            return strings
    
        
        if self.logMode:
            return self.logTickStrings(values, scale, spacing)

        # warnings.simplefilter("ignore")
        try:
            places = np.nanmax([0,
                np.ceil(-np.log10((np.abs(self.scalefunc(values[0] + spacing) - self.scalefunc(values[0])))*scale)),
                np.ceil(-np.log10((np.abs(self.scalefunc(values[-1]) - self.scalefunc(values[-1] - spacing)))*scale))])
        except IndexError:
            places = 0
        # warnings.simplefilter("default")
        strings = []
        for v in values:
            vs = self.scalefunc(v) * scale
            if abs(vs) < .001 or abs(vs) >= 10000:
                vstr = "%g" % vs
            else:
                vstr = ("%%0.%df" % places) % vs
            strings.append(vstr)
        return strings

    # def updateAutoSIPrefix(self):
    #     """Update the SI prefix for units, if displayed."""
    #     if self.label.isVisible():
    #         (scale, prefix) = pg.siScale(max(abs(self.scalefunc(self.range[0])), abs(self.scalefunc(self.range[1]))))
    #         if self.labelUnits == '' and prefix in ['k', 'm']:  ## If we are not showing units, wait until 1e6 before scaling.
    #             scale = 1.0
    #             prefix = ''
    #         self.setLabel(unitPrefix=prefix)
    #     else:
    #         scale = 1.0

    #     self.autoSIPrefixScale = scale
    #     self.picture = None
    #     self.update()

    # def logTickStrings(self, values, scale, spacing):
    #     """Return tick strings for a logarithmic axis."""
    #     # This one-line abomination isn't tested very extensively but seems to work...
    #     return ["%0.1g"%x for x in np.array([self.scalefunc(v) for v in 10 ** np.array(values).astype(float)])]


class CustomAxis(pg.AxisItem):

    def __init__(self, scale, label=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setLabel(label)
        self.scale = scale
        # self.setGrid(True)
        # self.setGridPen(pg.mkPen('k', width=0.5, style=Qt.DotLine))
    def tickStrings(self, values, scale, spacing):
        ret = list()
        for v in values:
            if v > 0:
                ret.append('{:.2f}%'.format(v*scale))
            else:
                ret.append('')
        return ret
    

def add_rax(layout):
    
    rax = AxisItemScaleFunction(orientation='right', scalefunc=None)
    p1 = layout.addPlot(row=0, col=0, axisItems={'right': rax}, enableMenu=False)
    p1.showGrid(True, True)


def add_lax(layout):
    # p1.showAxis('right')
    # p1.hideAxis('left')
    
    rax = AxisItemScaleFunction(orientation='right', scalefunc=None)
    lax = AxisItemScaleFunction(orientation='left', scalefunc=lambda x: x*0.3)
    tax = AxisItemScaleFunction(orientation='top', scalefunc=lambda x: x*0.9)

    p1 = layout.addPlot(row=0, col=0, axisItems={'left': lax, 'right': rax, 'top': tax}, enableMenu=False)
    p1.showGrid(True, True)
    x = np.arange(1, 10)
    y = x**2
    p1.plot(x,y)
    

def create_plot(pw):
    p1 = pw.plotItem
    p1.showAxis('right')
    p1.hideAxis('left')
    # p1.showAxis('top')
    p1.showGrid(True, True)
    p1.setLabels(right='PL absolute', bottom='SPX')
    # p1.showAxis('top')
    # p1.hideAxis('bottom')
    # p1.getAxis('bottom').setGrid(False)
    # p1.getAxis('left').setGrid(False)
    # p1.showGrid(False, False)

    p1.layout.removeItem(p1.getAxis('top'))
    tax = AxisItemScaleFunction(orientation='top', parent=p1, scalefunc=lambda x: 2.998e5/x if not x == 0 else np.inf)
    tax.linkToView(p1.vb)
    p1.axes['top']['item'] = tax
    p1.setAxisItems(axisItems = {'top': tax})


    #Custom top axis
    # p1.layout.removeItem(p1.getAxis('top'))
    # caxis = CustomAxis(0.95, 'Percent Value', orientation='top', parent=p1)
    # caxis.linkToView(p1.vb)
    # p1.axes['top']['item'] = caxis
    # p1.setAxisItems(axisItems = {'top': caxis})

    #Custom right axis
    # p1.layout.removeItem(p1.getAxis('right'))
    # raxis = CustomAxis(0.33, 'Saturation', orientation='right', parent=p1)
    # raxis.linkToView(p1.vb)
    # p1.axes['right']['item'] = raxis
    # p1.setAxisItems(axisItems = {'right': raxis})

    x = np.arange(1, 10)
    y = x**2
    p1.plot(x,y)
    


if __name__ == '__main__':

    app = pg.mkQApp("Gradiant Layout Example")
    view = pg.GraphicsView()
    layout = pg.GraphicsLayout(border=(100,100,100))
    view.setCentralItem(layout)
    view.show()
    view.setWindowTitle('pyqtgraph example: GraphicsLayout')
    view.resize(800,600)

    add_lax(layout)
    # fig1 = layout.addPlot(title='Risk Graph')
    # fig1.showGrid(True, True) #show x and y grids
    
    sys.exit(app.exec())

    # app = pg.mkQApp()
    # pw = pg.PlotWidget()
    # pw.show()
    # pw.setWindowTitle('pyqtgraph example: MultipleXAxes')
    # # create_plot(pw)
    # get_rax(pw)
    # sys.exit(app.exec())        

