# -*- coding: utf-8 -*-
"""
Created on Tue Feb 03 12:53:22 2015

@author: dvalovcin
"""

import numpy as np
from PyQt4 import QtGui, QtCore
from MainWindow_ui import Ui_MainWindow
from Settings_ui import Ui_Dialog
import pyqtgraph as pg
pg.setConfigOption('background', 'w')
pg.setConfigOption('foreground', 'k')
try:
    import visa
except:
    print 'Error. VISA library not installed' 

class MainWin(QtGui.QMainWindow):
    updateDataSig = QtCore.pyqtSignal(object)
    statusSig = QtCore.pyqtSignal(object)
    def __init__(self):
        super(MainWin, self).__init__()
        self.initUI()
        self.initSettings()
        
        self.openSPEX()
        self.openAgi()
        
    def initUI(self):
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        #Initialize the plots (see imports at top for how to set the colors)
        self.pPyro = self.ui.gPyro.plot()
        plotitem = self.ui.gPyro.getPlotItem()
        plotitem.setLabel('top',text='Pyro')
        plotitem.setLabel('left',text='Voltage',units='V')
        plotitem.setLabel('bottom',text='Time', units='s')
        
        self.pPMT = self.ui.gSignal.plot()
        plotitem = self.ui.gSignal.getPlotItem()
        plotitem.setLabel('top',text='PMT')
        plotitem.setLabel('left',text='Voltage',units='V')
        plotitem.setLabel('bottom',text='Time', units='s')
        
        self.ui.bChooseDirectory.clicked.connect(self.updateSaveLoc)
        self.ui.bStart.clicked.connect(self.startScan)
        self.ui.bPause.clicked[bool].connect(self.togglePause)
        
        
        self.show()
        
    def initSettings(self):
        #Initializes all the settings for the window in one tidy location,
        #make it have a more logical place if settings are saved and recalled eac
        #time
        s = dict()
        #Communication settings
        s['aGPIB'] = 'Fake'
        s['sGPIB'] = 'Fake'
        s['GPIBChoices'] = []
        s['pyChannel'] = 4
        s['pmChannel'] = 1
        
        #saving settings
        s['saveLocation'] = '.'
        s['saveName'] = ''
        s['saveComments'] = ''
        s['NIRP'] = 0
        s['NIRlambda'] = 0
        s['FELP'] = 0
        s['FELlambda'] = 0
        s['Temperature'] = 0
        s['PMHV'] = 0
        
        #scan settings
        s['startWN'] = 0
        s['stepWN'] = 0
        s['endWN'] = 0
        s['ave'] = 1
        
        #running flags
        s['notPaused'] = True
        s['runningFlag'] = False
        
        
        
        self.settings = s
        
    def updateSaveLoc(self):
        pass
    
    def openSPEX(self):
        pass
    
    def openAgi(self):
        pass

    def startScan(self):
        pass
    
    def togglePause(self, val):
        print val
        pass

    def updateStatusBar(self, args):
        '''function to update the status bar. Connects to a signal so it
           can be used from different threads. Pass a string to emit a message for
           3 seconds. Else pass a list, the first element the message and the second
           a ms value for the timeout'''
        if type(args) is str:
            self.ui.statusbar.showMessage(args, 3000)
        else:
            self.ui.statusbar.showMessage(args[0], args[1])











































































def main():
    import sys
    app = QtGui.QApplication(sys.argv)
    ex = MainWin()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()



