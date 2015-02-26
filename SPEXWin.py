# -*- coding: utf-8 -*-
"""
Created on Tue Feb 03 12:53:22 2015

@author: dvalovcin
"""

import numpy as np
from PyQt4 import QtGui, QtCore
from SPEXWindow_ui import Ui_MainWindow
import threading
import time
from InstsAndQt.Instruments import SPEX
import pyqtgraph as pg
pg.setConfigOption('background', 'w')
pg.setConfigOption('foreground', 'k')
try:
    import visa
except:
    print 'Error. VISA library not installed' 

class SPEXWin(QtGui.QMainWindow):
    updateDataSig = QtCore.pyqtSignal(object)
    statusSig = QtCore.pyqtSignal(object)
    scopeCollectionThread = None
    def __init__(self, SPEXInfo = None, parent = None):
        '''SPEXInfo should be either the GPIB to which it should open, or an actual instrument handle'''
        super(SPEXWin, self).__init__()
        if not parent == None:
            self.settings = parent.settings
            self.SPEX = parent.SPEX
            parent.wnUpdateSig.connect(self.updateStatusBarBoth)
            #Do some handling here to set up handling signals froma parent to update
            #values
        else:
            self.initSettings()
        self.parent = parent
        self.initUI()
        if SPEXInfo == None:
            SPEXInfo = 'Fake'
        if type(SPEXInfo) is str:
            self.settings['sGPIB'] = SPEXInfo
            self.openSPEX()
            
            
        if parent:
            self.ui.cGPIB.setEnabled(False)
            
        self.statusSig.connect(self.updateStatusBar)
        

        
    def initUI(self):
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        self.tGot = QtGui.QLabel(self)
        self.tWant = QtGui.QLabel(self)
        self.ui.statusbar.addPermanentWidget(self.tWant, 1)
        self.ui.statusbar.addPermanentWidget(self.tGot, 1)

        try:
            res = list(visa.ResourceManager().list_resources())
            res = [i.encode('ascii') for i in res]
        except:
            res = ['a', 'b','c']
        res.append('Fake')
        self.settings['GPIBChoices'] = res
        self.ui.cGPIB.addItems(res)
        self.ui.cGPIB.setCurrentIndex(res.index(self.settings['sGPIB']))
        
        self.ui.bDone.clicked.connect(self.closeEvent)
        self.ui.bGo.clicked.connect(self.changeWN)
        
        
        self.show()
    
    
    def openSPEX(self):
        try:
            self.SPEX = SPEX(self.settings['sGPIB'])
            print 'SPEX opened'
        except:
            print 'Error opening SPEX. Adding Fake'
            self.settings['sGPIB'] = 'Fake'
            self.SPEX = SPEX(self.settings['sGPIB'])
            
            
    def initSettings(self):
        #Initializes all the settings for the window in one tidy location,
        #make it have a more logical place if settings are saved and recalled eac
        #time
        s = dict()
        #Communication settings
        s['aGPIB'] = 'Fake'
        s['sGPIB'] = 'Fake'
        s['GPIBChoices'] = []
        
        
        self.settings = s
    
    def changeWN(self):
        self.ui.tGotoWN.setEnabled(False)
        self.ui.bGo.setEnabled(False)
        desiredWN = float(self.ui.tGotoWN.text())
#        self.statusSig.emit([self.tWant, self.SPEX.wavenumberToSteps(desiredWN)])
        self.tWant.setText('Wanted: ' + str(self.SPEX.wavenumberToSteps(desiredWN)))
        self.SPEX.gotoWN(desiredWN)
        
#        self.statusSig.emit([self.tGot, self.SPEX.currentPositionSteps])
        self.tGot.setText('Got: ' + str(self.SPEX.currentPositionSteps))
        self.ui.tGotoWN.setEnabled(True)
        self.ui.bGo.setEnabled(True)
        
    def updateStatusBar(self, args):
        '''Update the two status bar things
        first element of arg shold be reference to QLabel to eidt
        second should be what to write'''
        pre = 'Wanted: '
        if id(args[0]==id(self.tGot)):
            pre = 'Got: '
        args[0].setText(pre+str(args[1]))
        
    def updateStatusBarBoth(self, want, got):
        '''Updates the status bar when both are pass.
        Unique from updateStatusBar() in that it needs both simultanously.
        Previous one is used for asynchronous updating'''
        self.tWant.setText('Wanted: '+want)
        self.tGot.setText('Got: ' + got)
        
    
    def closeEvent(self, event):
        print 'Close event handling'
        #A little hacky way to let the main window know that this window has closed
        #the legitimate way to do it would be to emit a signal and have the main window
        #connect the signal, incase this class ever gets used to be called by a class
        #wwhich doens't have self.SPEXWindow
        if not self.parent ==None:
            self.parent.SPEXWindow = None
#            self.hide()
#        else:
#            self.close()
        self.close()
        #Restart the scope to trigger as normal.




























def main():
    import sys
    app = QtGui.QApplication(sys.argv)
    ex = SPEXWin()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()



