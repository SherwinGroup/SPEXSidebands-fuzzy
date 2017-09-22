
import pyqtgraph as pg
import numpy as np
import sys
from PyQt4 import QtCore, QtGui
from .clickablePlotSettings_ui import Ui_LineSettingsDialog

config_options = {
    "selectionThickness": 3
}


class PlotDataErrorItem(pg.PlotDataItem):
    """
    This class will wrap a pg.PlotDataItem
    (which, in turn, wraps a curveItem and scatterPlotItem)
    and an errorbarItem, so they can all be wrapped together.
    Really hate that this isn't a standard feature.

    Need to make this a subclass of PlotDataItem, because
    some stuff was hardcoded in LegendItems which would
    be a huge headache to work around if you don't subclass.
    """
    def __init__(self, *args, **kwargs):
        self.errorbars = pg.ErrorBarItem()
        super(PlotDataErrorItem, self).__init__(*args, **kwargs)
        self.errorbars.setParentItem(self)

    def setData(self, *args, **kwargs):
        # do I need to keep a reference to this?
        self.errorData = np.array(kwargs.pop("errorbars", None))
        super(PlotDataErrorItem, self).setData(*args, **kwargs)
        kwargs.update({'x': self.xData})
        kwargs.update({'y': self.yData})
        kwargs.update({'height': 2*self.errorData})
        self.errorbars.setData(**kwargs)

    def setPen(self, *args, **kwargs):
        super(PlotDataErrorItem, self).setPen(*args, **kwargs)
        self.errorbars.setOpts(pen=self.opts['pen'])

    def setLogMode(self, xMode, yMode):
        super(PlotDataErrorItem, self).setLogMode(xMode, yMode)

        # errrobaritem doesn't have an implementation
        # for doing log things. Try to do some hackish
        # stuff here so it at least won't break.
        kwargs = {}
        kwargs.update({'x': self.xDisp})
        kwargs.update({'y': self.yDisp})

        if yMode:
            kwargs.update({'height': np.log10(2*self.errorData)})
        else:
            kwargs.update({'height': 2*self.errorData})
        self.errorbars.setData(**kwargs)

    def updateItems(self):
        super(PlotDataErrorItem, self).updateItems()
        self.errorbars.setData(**self.opts)


class PlotDataErrorItemOld(pg.GraphicsObject):
    """
    This class will wrap a pg.PlotDataItem
    (which, in turn, wraps a curveItem and scatterPlotItem)
    and an errorbarItem, so they can all be wrapped together.
    Really hate that this isn't a standard feature.
    """
    sigClicked = QtCore.pyqtSignal(object)

    def __init__(self, *args, **kwargs):
        super(PlotDataErrorItem, self).__init__()

        self.setFlag(self.ItemHasNoContents)

        self.plotDataItem = pg.PlotDataItem()
        self.errorbarsItem = pg.ErrorBarItem()
        self.plotDataItem.setParentItem(self)
        self.errorbarsItem.setParentItem(self)

        self.plotDataItem.sigClicked.connect(self.curveClicked)

        # Wrap a ton of things to the plotDataItem
        for m in ['dataBounds', 'pixelPadding', 'setDownsampling',
                  'setSymbolSize', 'setSymbolBrush', 'setSymbolPen',
                  'setSymbol', 'name', 'opts', 'curve', 'scatter',
                  'opts'
                  ]:
            setattr(self, m, getattr(self.plotDataItem, m))

        self.setData(*args, **kwargs)


    def boundingRect(self):
        return QtCore.QRectF()  ## let child items handle this

    def setData(self, *args, **kwargs):
        # do I need to keep a reference to this?
        self.errorbars = np.array(kwargs.pop("errorbars", None))
        self.plotDataItem.setData(*args, **kwargs)
        kwargs.update({'x': self.plotDataItem.xData})
        kwargs.update({'y': self.plotDataItem.yData})
        kwargs.update({'height': 2*self.errorbars})
        self.errorbarsItem.setData(**kwargs)

    def setPen(self, *args, **kwargs):
        p = pg.mkPen(*args, **kwargs)
        # print("Setting pen. Color: {}, width: {}".format(p.color().name(), p.width()))
        self.plotDataItem.setPen(p)
        self.errorbarsItem.setOpts(pen=p)
        # print("After setting pens. self.width: {}".format(self.opts["pen"].width()))
        # print("After setting pens. curve.width: {}".format(self.plotDataItem.opts["pen"].width()))
        # print("self.opts is curve.opts?", self.opts is self.plotDataItem.opts)

    def setLogMode(self, xMode, yMode):
        self.plotDataItem.setLogMode(xMode, yMode)

        # errrobaritem doesn't have an implementation
        # for doing log things. Try to do some hackish
        # stuff here so it at least won't break.
        kwargs = {}
        kwargs.update({'x': self.plotDataItem.xDisp})
        kwargs.update({'y': self.plotDataItem.yDisp})
        # kwargs.update({'top': np.log10(self.errorbars+self.plotDataItem.yData) -
        #                np.log10(self.plotDataItem.yData) })
        # kwargs.update({'bottom': np.log10(self.errorbars-self.plotDataItem.yData) -
        #                np.log10(self.plotDataItem.yData) })
        kwargs.update({'height': np.log10(2*self.errorbars)})
        self.errorbarsItem.setData(**kwargs)

    def curveClicked(self):
        # print("\ncurve is clicked")
        self.sigClicked.emit(self)

    def updateItems(self):
        p = self.opts["pen"]
        # print("UpdateItemsColor: {}, width: {}".format(p.color().name(), p.width()))
        self.plotDataItem.updateItems()
        self.errorbarsItem.setData(**self.opts)

    def implements(self, interface=None):
        # pyqtgraph internals which I'd like to mimic
        ints = ['plotData']
        if interface is None:
            return ints
        return interface in ints


if __name__=='__main__':
    ex = QtGui.QApplication([])
    wid = pg.PlotWidget()
    # wid.plotItem.addLegend()


    it = PlotDataErrorItem([0, 1, 2, 3, 4], [1e2, 2e3, 1e1, 5e4, 2e2], errorbars=[1]*5)
    it.setPen('r', width=3)
    print(it.opts["pen"])
    # it = pg.PlotDataItem([0, 1, 2, 3, 4], [1, -2, 4, 8, 2])
    wid.addItem(it)

    wid.show()
    sys.exit(ex.exec_())