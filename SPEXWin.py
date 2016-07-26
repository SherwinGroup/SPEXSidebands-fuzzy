# -*- coding: utf-8 -*-
"""
Created on Tue Feb 03 12:53:22 2015

@author: dvalovcin
"""

import numpy as np
from PyQt4 import QtGui, QtCore
from UIs.SPEXWindow_ui import Ui_SPEXController
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

import logging
log = logging.getLogger("SPEX")

class SPEXWin(QtGui.QMainWindow):
    updateDataSig = QtCore.pyqtSignal(object)
    statusSig = QtCore.pyqtSignal(object)
    scopeCollectionThread = None
    def __init__(self, SPEXInfo = None, parent = None):
        '''SPEXInfo should be either the GPIB to which it should open, or an actual instrument handle'''
        super(SPEXWin, self).__init__()
        if not parent is None:
            self.settings = parent.settings
            self.SPEX = parent.SPEX
            parent.wnUpdateSig.connect(self.updateStatusBarBoth)
            #Do some handling here to set up handling signals froma parent to update
            #values
        else:
            self.initSettings()
        self.parent = parent
        self.initUI()
        if parent is None:
            # hide it if no parent: no knowledge
            # of frequencies
            self.ui.sbSB.setVisible(False)
            self.ui.lSBO.setVisible(False)
        else:
            if 0 in [self.settings.get(ii, 0) for ii in ["fel_lambda", "nir_lambda"]]:
                self.ui.sbSB.setEnabled(False)
                self.ui.sbSB.setToolTip("Reopen after setting wavelengths")
            else:
                self.ui.sbSB.valueChanged.connect(self.setPosFromSB)

        if SPEXInfo is None:
            SPEXInfo = 'GPIB0::4::INSTR'
        if type(SPEXInfo) is str:
            self.settings['sGPIB'] = SPEXInfo
            self.openSPEX()
        # figure out where the spex is
        try:
            pos = self.SPEX.stepsToWN(self.SPEX.curStep())
        except TypeError:
            log.warning("Error, spex not initialized!")
            QtGui.QMessageBox.critical(self, "Error", "Error! SPEX not initalized!")
            pos = 0
        self.ui.sbGoto.setValue(pos)
            
            
        if parent:
            self.ui.cGPIB.setEnabled(False)
            
        self.statusSig.connect(self.updateStatusBar)
        

        
    def initUI(self):
        self.ui = Ui_SPEXController()
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
        self.ui.cGPIB.setCurrentIndex(res.index(self.settings['sGPIB'])) #-1 for counting from 0
        
        self.ui.bDone.clicked.connect(self.closeEvent)
        self.ui.bGo.clicked.connect(self.changeWN)

        self.ui.sbGoto.setOpts(step=1, decimals=1, bounds=(11000, 15000))
        self.ui.cGPIB.currentIndexChanged.connect(self.openSPEX)

        self.ui.actionInitiate_SPEX.triggered.connect(self.initSPEX)
        
        self.show()

    def openSPEX(self):
        try:
            self.SPEX.close()
        except:
            pass
        try:
            self.SPEX = SPEX(str(self.ui.cGPIB.currentText()))
            pos = self.SPEX.stepsToWN(self.SPEX.curStep())
            self.ui.sbGoto.setValue(pos)
            print 'SPEX opened'
        except AttributeError:
            # Don't reset open instrument if
            # you failed from a boot error
            if self.SPEX.whereAmI() == 'B':
                print "SPEX not initialized"
                return
        except Exception as e:
            print 'Error opening SPEX.'
            log.exception("Couldn't init")


            self.settings['sGPIB'] = 'Fake'
            self.SPEX = SPEX("Fake")
            self.ui.cGPIB.currentIndexChanged.disconnect(self.openSPEX)
            self.ui.cGPIB.setCurrentIndex(
                self.ui.cGPIB.findText("Fake")
            )
            self.ui.cGPIB.currentIndexChanged.connect(self.openSPEX)
            
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

    def initSPEX(self):
        """
        Input the exact value read on the SPEX. The subtraction
        is done automatically
        :return:
        """
        newWN, ok= QtGui.QInputDialog.getDouble(
            self, "Current SPEX Wavenumber",
            "Current SPEX Value (exact value)",
            13000, 11000, 15000
        )
        if not ok: return
        self.SPEX.initBoot(newWN)
        if self.parent is not None:
            self.parent.openSPEX()
            self.ui.sbGoto.setValue(
                self.SPEX.currentPositionWN
            )
        else:
            self.openSPEX()

    def changeWN(self):
        self.ui.sbGoto.setEnabled(False)
        self.ui.bGo.setEnabled(False)
        desiredWN = float(self.ui.sbGoto.text())
#        self.statusSig.emit([self.tWant, self.SPEX.wavenumberToSteps(desiredWN)])
        self.tWant.setText('Wanted: {}'.format(desiredWN))
        log.debug("Wanted {}wn, {} steps".format(desiredWN, self.SPEX.wavenumberToSteps(desiredWN)))
        self.SPEX.gotoWN(desiredWN)
        
#        self.statusSig.emit([self.tGot, self.SPEX.currentPositionSteps])
        self.tGot.setText('Got: {}'.format(self.SPEX.currentPositionWN))
        self.ui.sbGoto.setEnabled(True)
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

    def setPosFromSB(self):
        nir, thz = self.settings.get("nir_lambda", 0), self.settings.get("fel_lambda", 0)
        if 0 in [nir, thz]:
            # hsouldn't ever get here, since it shouldn't be connected, but prevent erros
            return
        want = nir + int(self.ui.sbSB.value())*thz
        self.ui.sbGoto.setValue(want)
        
    
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



