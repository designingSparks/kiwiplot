from PyQt5 import QtCore, QtWidgets
import pyqtgraph as pg
import numpy as np
import warnings


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
        if self.logMode:
            return self.logTickStrings(values, scale, spacing)

        warnings.simplefilter("ignore")
        try:
            places = np.nanmax([0,
                np.ceil(-np.log10((np.abs(self.scalefunc(values[0] + spacing) - self.scalefunc(values[0])))*scale)),
                np.ceil(-np.log10((np.abs(self.scalefunc(values[-1]) - self.scalefunc(values[-1] - spacing)))*scale))])
        except IndexError:
            places = 0
        warnings.simplefilter("default")
        strings = []
        for v in values:
            vs = self.scalefunc(v) * scale
            if abs(vs) < .001 or abs(vs) >= 10000:
                vstr = "%g" % vs
            else:
                vstr = ("%%0.%df" % places) % vs
            strings.append(vstr)
        return strings

    def updateAutoSIPrefix(self):
        """Update the SI prefix for units, if displayed."""
        if self.label.isVisible():
            (scale, prefix) = pg.siScale(max(abs(self.scalefunc(self.range[0])), abs(self.scalefunc(self.range[1]))))
            if self.labelUnits == '' and prefix in ['k', 'm']:  ## If we are not showing units, wait until 1e6 before scaling.
                scale = 1.0
                prefix = ''
            self.setLabel(unitPrefix=prefix)
        else:
            scale = 1.0

        self.autoSIPrefixScale = scale
        self.picture = None
        self.update()

    def logTickStrings(self, values, scale, spacing):
        """Return tick strings for a logarithmic axis."""
        # This one-line abomination isn't tested very extensively but seems to work...
        return ["%0.1g"%x for x in np.array([self.scalefunc(v) for v in 10 ** np.array(values).astype(float)])]


class TwinScales(pg.GraphicsLayoutWidget):

    def __init__(self):
        super().__init__()
        rax = AxisItemScaleFunction(orientation='right', scalefunc=lambda x: 2.998e5/x if not x == 0 else np.inf)
        self.spectrum = self.addPlot(row=0, col=0, axisItems={'right': rax}, enableMenu=False)
        self.spectrum.showGrid(x=True, y=True)
        self.spectrum.addLegend(offset=(-10, 5))
        self.spectrum.setLabels(left="Frequency (THz)", bottom="Intensity (a.u.)", right="Wavelength (nm)")

        y = np.linspace(400, 800, num=200)
        self.p1 = self.spectrum.plot(56.7*np.sin(y/20), y, pen=(255, 255, 0), name="Spectral slice t = 123.4 fs")
        self.p2 = self.spectrum.plot(45.6*np.cos(y/30), y, pen=(255, 0, 0), name="Other slice t = 567.8 fs")

        self.spectrum.setLogMode(x=False, y=True)


def main():
    import sys
    app = QtWidgets.QApplication(sys.argv)
    mainwindow = TwinScales()
    mainwindow.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()