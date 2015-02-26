# -*- coding: utf-8 -*-
"""
Created on Tue Feb 03 12:53:22 2015
@author: dvalovcin
"""

import numpy as np
import scipy.integrate as spi
from PyQt4 import QtGui, QtCore
import threading
import time
import copy
import sys, os
try:
    from InstsAndQt.Instruments import SPEX, Agilent6000
except Exception as e:
    raise IOError('Instrument library not found. Often placed in another directory')
from SPEXWin import SPEXWin
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
    #emits when oscilloscope is done taking data so that
    #the data collecting thread knows it's ready to processes
    updateDataSig = QtCore.pyqtSignal()
    #emits when status bar needs updating.
    #Either a string or array of [str, int]
    #where str is message and int is time (ms) to display
    statusSig = QtCore.pyqtSignal(object)
    #Emits data from the oscilloscope. Updates graphs
    pyDataSig = QtCore.pyqtSignal(object)
    pmDataSig = QtCore.pyqtSignal(object)
    #emits the wavenumber changes so a child'ed SPEXWin can update.
    #order (wanted, got)
    wnUpdateSig = QtCore.pyqtSignal(object, object) 
    #emit to update the boxcar values
    boxcarSig = QtCore.pyqtSignal(object, object, object)
    
    #Thread which handles polling the oscilloscope
    scopeCollectionThread = None
    #Thread which handles scanning the SPEX and updating data, etc
    scanRunningThread = None
    def __init__(self):
        super(MainWin, self).__init__()
        self.initSettings()
        self.initUI()
        self.pyDataSig.connect(self.updatePyroGraph)
        self.pmDataSig.connect(self.updatePMTGraph)
        self.statusSig.connect(self.updateStatusBar)
        self.boxcarSig.connect(self.updateBoxcarTexts)
        
        self.openSPEX()
        self.openAgi()
        self.SPEXWindow = None
        
    def initUI(self):
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        #Initialize the plots (see imports at top for how to set the colors)
        self.pPyro = self.ui.gPyro.plot(pen='k')
        plotitem = self.ui.gPyro.getPlotItem()
        plotitem.setLabel('top',text='Pyro')
        plotitem.setLabel('left',text='Voltage',units='V')
        plotitem.setLabel('bottom',text='Time', units='s')
        
        self.pPMT = self.ui.gSignal.plot(pen='k')
        plotitem = self.ui.gSignal.getPlotItem()
        plotitem.setLabel('top',text='PMT')
        plotitem.setLabel('left',text='Voltage',units='V')
        plotitem.setLabel('bottom',text='Time', units='s')
        
        self.initLinearRegionBounds()
        #Now we make an array of all the textboxes for the linear regions to make it
        #easier to iterate through them. Set it up in memory identical to how it
        #appears on the panel for sanity, in a row-major fashion
        lrtb = []
        lrtb.append([self.ui.tPyBgSt, self.ui.tPyBgEn])
        lrtb.append([self.ui.tPyFpSt, self.ui.tPyFpEn])
        lrtb.append([self.ui.tPyCdSt, self.ui.tPyCdEn])
        lrtb.append([self.ui.tPmBgSt, self.ui.tPmBgEn])
        lrtb.append([self.ui.tPmSgSt, self.ui.tPmSgEn])
        for i in lrtb:
            for j in i:
                j.textAccepted.connect(self.updateLinearRegionsFromText)
        
        self.linearRegionTextBoxes = lrtb
        
        
        self.ui.bChooseDirectory.clicked.connect(self.updateSaveLoc)
        self.ui.bStart.clicked.connect(self.startScan)
        self.ui.bPause.clicked[bool].connect(self.togglePause)
#        self.ui.bAbort.clicked.connect(lambda self=self: setattr(self, "settings['runningScan']", False))
        self.ui.bAbort.clicked.connect(self.abortScan)
        self.ui.bSaveWaveforms.clicked.connect(self.saveWaveforms)
        self.ui.mFileSettings.triggered.connect(self.launchSettings)
        self.ui.mFileExit.triggered.connect(self.closeEvent)
        self.ui.mSpexOpen.triggered.connect(self.openSPEXWindow)
        
        self.tGeneralSB = QtGui.QLabel()
        self.tbcPyroFP = QtGui.QLabel()
        self.tbcPyroCD = QtGui.QLabel()
        self.tbcPMSG = QtGui.QLabel()
        
        self.ui.statusbar.addPermanentWidget(self.tGeneralSB)
        self.ui.statusbar.addPermanentWidget(self.tbcPyroFP, 1)
        self.ui.statusbar.addPermanentWidget(self.tbcPyroCD, 1)
        self.ui.statusbar.addPermanentWidget(self.tbcPMSG, 1)
        
        
        self.show()
    def abortScan(self):
        self.settings['runningScan'] = False        
    def initSettings(self):
        #Initializes all the settings for the window in one tidy location,
        #make it have a more logical place if settings are saved and recalled eac
        #time
        s = dict()
        #Communication settings
        s['aGPIB'] = 'Fake'#'GPIB0::5::INSTR' #GPIB of the agilent
        s['sGPIB'] = 'Fake'#'GPIB0::4::INSTR' #GPIB of the SPEX
        s['GPIBChoices'] = []   #List of the possible GPIB choices
        s['pyCh'] = 4  #Osc channel for the pyro
        s['pmCh'] = 1  #osc channel for the pmt 
        
        #saving settings
        s['saveLocation'] = '.'
        s['saveName'] = ''
        s['saveComments'] = ''
        s['NIRP'] = '' #NIR Power
        s['NIRlambda'] = '' #NIR wavenumber
        s['FELP'] = '' #FEL power
        s['FELlambda'] = '' #FEL wavenumber
        s['Temperature'] = ''
        s['PMHV'] = '' #PMT voltage
        s['repRate'] = 0.75
        
        #scan settings
        s['startWN'] = 0 #Starting wavenumber
        s['stepWN'] = 0 #how many wavenumbers to steop by
        s['endWN'] = 0 #Ending wavenumber
        s['ave'] = 1 #How many values to take an average of
        
        #running flags
        #Pausing causes the oscilloscope reading loop to wait until we are unpaused
        s['notPaused'] = True
        #This is flag specifies whether the oscilloscope thread should be running or not
        #making it false causes that thread to close
        s['collectingScope'] = False
        #This flag specifies whether we are in the middle of running a scan
        s['runningScan'] = False
        #This flag should be used to synchronize with the SPEX. When the SPEX
        #is moving between wavenumbers, the scope will still be collecting data
        #and we don't want to falsely collect data during these times
        s['collectingData'] = False
        
        #data
        s['pyData'] = None
        s['pmData'] = None
        #wavenumber, ref FP, ref CD, signal
        s['allData'] = np.empty((0,4))
        s['currentWN'] = 0
        
        #boundaries for boxcar integration
        #bc[py|pm] -> boxcar[Pyro|PMT]
        #bg -> background
        #fp -> front porch
        #cd -> cavity dump
        #sb -> sideband
        #st -> start
        #en -> end
        s['bcpyBG'] = [0, 0]
        s['bcpyFP'] = [0, 0]
        s['bcpyCD'] = [0, 0]
        s['bcpmBG'] = [0, 0]
        s['bcpmSB'] = [0, 0]
        
        
        
        self.settings = s
        
    def initLinearRegionBounds(self):
        #initialize array for all 5 boxcar regions
        self.boxcarRegions = [None]*5
        
        bgCol = pg.mkBrush(QtGui.QColor(255, 0, 0, 50))
        fpCol = pg.mkBrush(QtGui.QColor(0, 0, 255, 50))
        sgCol = pg.mkBrush(QtGui.QColor(0, 255, 0, 50))
        
        #Background region for the pyro plot
        self.boxcarRegions[0] = pg.LinearRegionItem(self.settings['bcpyBG'], brush = bgCol)
        self.boxcarRegions[1] = pg.LinearRegionItem(self.settings['bcpyFP'], brush = fpCol)
        self.boxcarRegions[2] = pg.LinearRegionItem(self.settings['bcpyCD'], brush = sgCol)
        self.boxcarRegions[3] = pg.LinearRegionItem(self.settings['bcpmBG'], brush = bgCol)
        self.boxcarRegions[4] = pg.LinearRegionItem(self.settings['bcpmSB'], brush = sgCol)
        
        #Connect it all to something that will update values when these all change
        for i in self.boxcarRegions:
            i.sigRegionChangeFinished.connect(self.updateLinearRegionValues)
            
        self.ui.gPyro.addItem(self.boxcarRegions[0])
        self.ui.gPyro.addItem(self.boxcarRegions[1])
        self.ui.gPyro.addItem(self.boxcarRegions[2])
        self.ui.gSignal.addItem(self.boxcarRegions[3])
        self.ui.gSignal.addItem(self.boxcarRegions[4])
        
    def launchSettings(self):
        try:
            res = list(visa.ResourceManager().list_resources())
            res = [i.encode('ascii') for i in res]
        except:
            self.statusSig.emit(['Error loading GPIB list', 5000])
            res = ['a', 'b','c']
        res.append('Fake')
        self.settings['GPIBChoices'] = res
        
        #need to pass a copy of the settings. Otherwise it passes the reference,
        #thus changing the values and we're unable to see whether things have changed.
        newSettings, ok = SettingsDialog.getSettings(self, copy.copy(self.settings))
        if not ok:
            print 'canceled'
            return
        
        #Need to check to see if the GPIB values changed so we can update them.
        #The opening procedure opens a fake isntrument if things go wrong, which 
        #means we can't assign the settings dict after calling openKeith() as that would
        #potentially overwrite if we needed to open a fake instr.
        #
        #We get the old values before updating the settings. Th
        
        oldaGPIB = self.settings['aGPIB']
        oldsGPIB = self.settings['sGPIB']

        self.settings = newSettings
        print oldaGPIB, newSettings['aGPIB']
        if not oldaGPIB == newSettings['aGPIB']:
            self.Agil.close()
            self.settings['aGPIB'] = newSettings['aGPIB']
            self.openAgi()
        print oldsGPIB, newSettings['sGPIB']
        if not oldsGPIB == newSettings['sGPIB']:
            self.SPEX.close()
            self.settings['sGPIB'] = newSettings['sGPIB']
            self.openSPEX()
        
        #enforce the correct sign
        self.settings['stepWN'] = np.sign(self.settings['endWN']-self.settings['startWN'])*np.abs(
                    self.settings['stepWN'])
            
    def openSPEXWindow(self):
        if self.SPEXWindow == None:
            self.SPEXWindow = SPEXWin(SPEXInfo = self.SPEX, parent=self)
        else:
            self.SPEXWindow.raise_()
        
        
    def updateLinearRegionValues(self, values):
        sender = self.sender()
        sendidx = -1
        for (i, v) in enumerate(self.boxcarRegions):
            #I was debugging something. I tried to use id(), which is effectively the memory
            #location to try and fix it. Found out it was anohter issue, but
            #id() seems a little safer(?) than just equating them in the sense that
            #it's explicitly asking if they're the same object, isntead of potentially
            #calling some weird __eq__() pyqt/graph may have set up
            if id(sender) == id(v):
                sendidx = i
        i = sendidx
        #Just being paranoid, no reason to think it wouldn't find the proper thing
        if sendidx<0:
            return
        self.linearRegionTextBoxes[i][0].setText('{:.9g}'.format(sender.getRegion()[0]))
        self.linearRegionTextBoxes[i][1].setText('{:.9g}'.format(sender.getRegion()[1]))
            
    def updateLinearRegionsFromText(self):
        sender = self.sender()
        #figure out where this was sent
        sendi, sendj = -1, -1
        for (i, v)in enumerate(self.linearRegionTextBoxes):
            for (j, w) in enumerate(v):
                if id(w) == id(sender):
                    sendi = i
                    sendj = j
        
        i = sendi
        j = sendj
        curVals = list(self.boxcarRegions[i].getRegion())
        curVals[j] = float(sender.text())
        self.boxcarRegions[i].setRegion(tuple(curVals))
        
    def updateSaveLoc(self):
        fname = str(QtGui.QFileDialog.getExistingDirectory(self, "Choose File Directory...",directory=self.settings['saveLocation']))
        print 'fname',fname
        if fname == '':
            return
        self.settings['saveLocation'] = fname + '/'
    
    def genSaveHeader(self):
        #save space
        s = self.settings
        st = ('PNIR={},lambdaNIR={},PTHz={},fTHz={},\nRep_rate={},Exptime={},Gain={},Center_lambda={},'+\
                 'Grating={},BG_image={},Series={},Ymin={},Ymax={},slits={},CCD_temp={},sample_temp={},PMVoltage={}')
                 
        st = st.format(s['NIRP'], s['NIRlambda'], s['FELP'], s['FELlambda'], s['repRate'], 
                   'Nil', 'Nil', 'Nil', 'Nil', 'Nil', 'Nil', 'Nil', 'Nil', 'Nil', 'Nil', s['Temperature'],s['PMHV'])
        return self.settings['saveComments'] + '\n' + st
    
    def saveWaveforms(self):
        pyro = self.settings['pyData']
        sig = self.settings['pmData']
        
        np.savetxt(self.settings['saveLocation'] + str(self.ui.tSaveName.text()) + '_referenceDetector.txt',
                   pyro, header = self.genSaveHeader()+'\nVoltage (V), Time(s)')
                   
        np.savetxt(self.settings['saveLocation'] + str(self.ui.tSaveName.text()) + '_signalWaveform.txt',
                   sig, header = self.genSaveHeader()+'\nVoltage (V), Time(s)')
        
    
    def openSPEX(self):
        try:
            self.SPEX = SPEX(self.settings['sGPIB'])
            print 'SPEX opened'
        except:
            print 'Error opening SPEX. Adding Fake'
            self.settings['sGPIB'] = 'Fake'
            self.SPEX = SPEX(self.settings['sGPIB'])
    
    def openAgi(self):
        #Stop collection if it's happening
        self.settings['collectingScope'] = False
        isPaused = not self.settings['notPaused']
        print 'isPaused', isPaused
        if isPaused:
            self.togglePause(False)
        try: 
            self.scopeCollectionThread.join()
        except:
            pass
        #Try to connect it
        try:
            self.Agil = Agilent6000(self.settings['aGPIB'])
            print 'Agilent opened'
        except:
            print 'Error opening Agilent. Adding Fake'
            self.settings['sGPIB'] = 'Fake'
            self.Agil = Agilent6000(self.settings['aGPIB'])
            
        self.Agil.setTrigger()
        self.settings['collectingScope'] = True
            
        self.scopeCollectionThread = threading.Thread(target = self.collectScopeLoop)
        self.scopeCollectionThread.start()
        if isPaused:
            self.togglePause(True)

    def startScan(self):
        if self.settings['NIRP'] == '-1':
            self.settings['startWN'] = 13160
            self.settings['stepWN'] = -1
            self.settings['endWN'] = 13130
            self.settings['ave'] = 3
        elif self.settings['stepWN'] == 0:
            self.statusSig.emit(['Please initialize scan settings', 10000])
            return
        
        #wavenumber, ref FP, ref CD, signal
        self.settings['allData'] = np.empty((0,4))
        self.settings['runningScan'] = True
        self.ui.bStart.setEnabled(False)
        
        self.scanRunningThread = threading.Thread(target = self.runScanLoop)
        self.scanRunningThread.start()
        
        
    def runScanLoop(self):
        WNRange = np.arange(self.settings['startWN'],
                                self.settings['endWN'], self.settings['stepWN'])
        WNRange = np.append(WNRange, self.settings['endWN'])
        
        for wavenumber in WNRange:
            if not self.settings['runningScan']:
                print 'breaking scan'
                break
            self.settings['collectingData'] = False
            self.SPEX.gotoWN(wavenumber)
            self.statusSig.emit(['Wavenumber: '+str(wavenumber), 0])
            self.wnUpdateSig.emit(str(wavenumber), str(self.SPEX.currentPositionSteps))
            num = 0 #number of averages. Doing it this way so that if we want to implement
                    #something where we don't count a number, then we can decline decrementing
                    #effectively saying the point didn't happen
            self.settings['collectingData'] = True
            while num < self.settings['ave']:
                
                if not self.settings['runningScan']:
                    print 'breaking scan'
                    break
            #Now want to take data. This means we need to wait for the oscilloscope to 
            #finish collecting its current round. Enter a waiting loop. 
                self.waitingForDataLoop = QtCore.QEventLoop()
                self.updateDataSig.connect(self.waitingForDataLoop.exit)
                self.waitingForDataLoop.exec_()
                refFP, refCD, sig = self.integrateData()
                self.boxcarSig.emit(refFP, refCD, sig)
                isValid = True #Flag for telling whether to keep the data or not
                if isValid:
                    num += 1
                    self.settings['allData'] = np.append(
                        self.settings['allData'], [[wavenumber, refFP, refCD, sig]],
                        axis=0)
            
            
        
        #save Data
        np.savetxt(self.settings['saveLocation'] + str(self.ui.tSaveName.text()) + '_scanData.txt',
                   self.settings['allData'], header = self.genSaveHeader() + '\nWavenumber, Integrated front porch, Integrated Cavity dump, integrated signal')
        
        #clean up after done
        self.settings['collectingData'] = False
        self.settings['runningScan'] = False
        self.ui.bStart.setEnabled(True)
        self.statusSig.emit(['Done', 3000])
            
    def updateBoxcarTexts(self, v1, v2, v3):
        v1 = '{:.3g}'.format(v1)
        v2 = '{:.3g}'.format(v2)
        v3 = '{:.3g}'.format(v3)
        self.tbcPyroFP.setText('PyFP Box: ' + v1)
        self.tbcPyroCD.setText('PyCD Box:' + v2)
        self.tbcPMSG.setText('PmSG Box: ' + v3)
        
    def togglePause(self, val):
        #True to pause
        #False to unpause
        self.settings['notPaused'] = not val
        if not val: #If we're unpausing, kill the waiting loop:
            try:
                self.pausingLoop.exit()
            except:
                pass
        
    def integrateData(self):
        #Neater and maybe solve issues if the data happens to update
        #while trying to do analysis?
        pyD = self.settings['pyData']
        pmD = self.settings['pmData']
        
        pyBGbounds = self.boxcarRegions[0].getRegion()
        pyBGidx = self.findIndices(pyBGbounds, pyD[:,0])
        
        pyFPbounds = self.boxcarRegions[1].getRegion()
        pyFPidx = self.findIndices(pyFPbounds, pyD[:,0])
        
        pyCDbounds = self.boxcarRegions[2].getRegion()
        pyCDidx = self.findIndices(pyCDbounds, pyD[:,0])
        
        pmBGbounds = self.boxcarRegions[3].getRegion()
        pmBGidx = self.findIndices(pmBGbounds, pmD[:,0])
        
        pmSGbounds = self.boxcarRegions[4].getRegion()
        pmSGidx = self.findIndices(pmSGbounds, pmD[:,0])
        
        pyBG = spi.simps(pyD[pyBGidx[0]:pyBGidx[1],1], pyD[pyBGidx[0]:pyBGidx[1], 0])
        pyFP = spi.simps(pyD[pyFPidx[0]:pyFPidx[1],1], pyD[pyFPidx[0]:pyFPidx[1], 0])
        pyCD = spi.simps(pyD[pyCDidx[0]:pyCDidx[1],1], pyD[pyCDidx[0]:pyCDidx[1], 0])
        
        pmBG = spi.simps(pmD[pmBGidx[0]:pmBGidx[1],1], pmD[pmBGidx[0]:pmBGidx[1], 0])
        pmSG = spi.simps(pmD[pmSGidx[0]:pmSGidx[1],1], pmD[pmSGidx[0]:pmSGidx[1], 0])
        
        return pyFP-pyBG, pyCD-pyBG, pmSG-pmBG
        
    def findIndices(self, values, dataset):
        '''Given an ordered dataset and a pair of values, returns the indices which
           correspond to these bounds  '''
        indx = list((dataset>values[0]) & (dataset<values[1]))
        #convert to string for easy finding
        st = ''.join([str(int(i)) for i in indx])
        start = st.find('1')
        if start == -1:
            start = 0
        end = start + st[start:].find('0')
        if end<=0:
            end = 1
        return (start, end)

    def updateStatusBar(self, args):
        '''function to update the status bar. Connects to a signal so it
           can be used from different threads. Pass a string to emit a message for
           3 seconds. Else pass a list, the first element the message and the second
           a ms value for the timeout'''
        if type(args) is str:
#            self.ui.statusbar.showMessage(args, 3000)
            self.tGeneralSB.setText(args)
        else:
#            self.ui.statusbar.showMessage(args[0], args[1])
            self.tGeneralSB.setText(args[0])
            
    def updatePyroGraph(self, data):
        self.settings['pyData'] = data
        self.pPyro.setData(data[:,0], data[:,1])
        
    def updatePMTGraph(self, data):
        self.settings['pmData'] = data
        self.pPMT.setData(data[:,0], data[:,1])
        



    def collectScopeLoop(self):
        while self.settings['collectingScope']:
            if not self.settings['notPaused']:
                #Have the scope updating remotely so it can be changed if needed
                self.Agil.write(':RUN')
                #If we want to pause, make a fake event loop and terminate it from outside forces
                self.pausingLoop = QtCore.QEventLoop()
                self.pausingLoop.exec_()
                pass
            pyCh = self.settings['pyCh']
            pmCh = self.settings['pmCh']
            pyData, pmData = self.Agil.getMultipleChannels(pyCh, pmCh)
            if self.settings['notPaused']:
                self.pyDataSig.emit(pyData)
                self.pmDataSig.emit(pmData)
                self.updateDataSig.emit()
#            time.sleep(.5)
            
    def closeEvent(self, event):
        print 'Close event handling'
        self.settings['collectingScope'] = False
        self.settings['runningScan'] = False
        #Stop pausing
        try:
            self.pausingLoop.exit()
        except:
            pass
        
        try:
            self.waitingForDataLoop.exit()
        except:
            pass
        try:
            self.scanRunningThread.join()
        except:
            pass
        
        #Stop the runnign thread for collecting from scope
        try:
            self.scopeCollectionThread.join()
        except:
            pass
        
        
        #Restart the scope to trigger as normal.
        self.Agil.write(':RUN')
        self.close()








class SettingsDialog(QtGui.QDialog):
    def __init__(self, parent = None, settings=None):
        super(SettingsDialog, self).__init__(parent)
        self.initUI(settings)
        
    def initUI(self, settings):
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.ui.cAGPIB.insertItems(0, settings['GPIBChoices'])
        self.ui.cAGPIB.setCurrentIndex(
                    settings['GPIBChoices'].index(settings['aGPIB'])
                                            )
        self.ui.cSGPIB.insertItems(0, settings['GPIBChoices'])
        self.ui.cSGPIB.setCurrentIndex(
                    settings['GPIBChoices'].index(settings['sGPIB'])
                                            )
        self.ui.tStartWN.setText(str(settings['startWN']))
        self.ui.tStepWN.setText(str(settings['stepWN']))
        self.ui.tEndWN.setText(str(settings['endWN']))
        self.ui.tAverages.setText(str(settings['ave']))
        
        self.ui.cPyroCh.insertItems(0, ['1', '2', '3', '4'])
        self.ui.cPyroCh.setCurrentIndex(settings['pyCh']-1)
        self.ui.cPMCh.insertItems(0, ['1', '2', '3', '4'])
        self.ui.cPMCh.setCurrentIndex(settings['pmCh']-1)
        
        self.ui.tNIRP.setText(str(settings['NIRP']))
        self.ui.tNIRLam.setText(str(settings['NIRlambda']))
        self.ui.tHV.setText(str(settings['PMHV']))
        self.ui.tFELP.setText(str(settings['FELP']))
        self.ui.tFELLam.setText(str(settings['FELlambda']))
        self.ui.tRepRate.setText(str(settings['repRate']))
        self.ui.tTemp.setText(str(settings['Temperature']))
        self.ui.tSaveComments.setText(settings['saveComments'])
        
        if settings['runningScan']:
            self.ui.tAverages.setEnabled(False)
            self.ui.tStartWN.setEnabled(False)
            self.ui.tStepWN.setEnabled(False)
            self.ui.tEndWN.setEnabled(False)
    @staticmethod
    def getSettings(parent = None, settings = None):
        dialog = SettingsDialog(parent, settings)
        result = dialog.exec_()
        settings['aGPIB'] = str(dialog.ui.cAGPIB.currentText())
        settings['sGPIB'] = str(dialog.ui.cSGPIB.currentText())
        settings['startWN'] = float(dialog.ui.tStartWN.text())
        settings['stepWN'] = float(dialog.ui.tStepWN.text())
        settings['endWN'] = float(dialog.ui.tEndWN.text())
        settings['ave'] = int(dialog.ui.tAverages.text())
        settings['pyCh'] = int(dialog.ui.cPyroCh.currentText())
        settings['pmCh'] = int(dialog.ui.cPMCh.currentText())
        settings['NIRP'] = str(dialog.ui.tNIRP.text())
        settings['NIRlambda'] = str(dialog.ui.tNIRLam.text())
        settings['PMHV'] = str(dialog.ui.tHV.text())
        settings['FELP'] = str(dialog.ui.tFELP.text())
        settings['FELlambda'] = str(dialog.ui.tFELLam.text())
        settings['repRate'] = str(dialog.ui.tRepRate.text())
        settings['Temperature'] = str(dialog.ui.tTemp.text())
        settings['saveComments'] = dialog.ui.tSaveComments.toPlainText()
        return (settings, result==QtGui.QDialog.Accepted)






























































def main():
    import sys
    app = QtGui.QApplication(sys.argv)
    ex = MainWin()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()

