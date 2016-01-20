# -*- coding: utf-8 -*-
"""
Created on Tue Feb 03 12:53:22 2015
@author: dvalovcin
"""

import numpy as np
import scipy.integrate as spi
from scipy.interpolate import interp1d
from PyQt4 import QtGui, QtCore
import threading
import json
import glob
import time
import datetime
import copy
try:
    from InstsAndQt.Instruments import SPEX, Agilent6000
    import InstsAndQt.Instruments
    InstsAndQt.Instruments.PRINT_OUTPUT = False
except Exception as e:
    raise IOError('Instrument library not found. Often placed in another directory')
from InstsAndQt.PyroOscope.OscWid import OscWid
import motordriver as md
from SPEXWin import SPEXWin
from UIs.MainWindow_ui import Ui_MainWindow
from UIs.Settings_ui import Ui_Settings
from UIs.QuickSettings_ui import Ui_QuickSettings
import pyqtgraph as pg
pg.setConfigOption('background', 'w')
pg.setConfigOption('foreground', 'k')
try:
    import visa
except:
    print 'Error. VISA library not installed'

# http://stackoverflow.com/questions/1551605/how-to-set-applications-taskbar-icon-in-windows-7/1552105#1552105
# Don't want python app window to clump
# with the other windows
import ctypes, os
if os.name is not "posix":
    myappid = 'Sherwin.Group.SPEXSidebands.100' # arbitrary string
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)


import logging
log = logging.getLogger("SPEX")
log.setLevel(logging.DEBUG)
handler1 = logging.StreamHandler()
handler1.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - [%(filename)s:%(lineno)s - %(funcName)s()] - %(levelname)s - %(message)s')
handler1.setFormatter(formatter)
log.addHandler(handler1)



seriesTags = {"FELL": "fel_lambda",
              "FELP": "fel_power",
              "NIRP": "nir_power",
              "NIRL": "nir_lambda",
              "FELTRANS": "fel_transmission",
              "PMHV": "pm_hv",
              "TEMP": "temperature"}




"""
Calibrating the NE20A filters:

15-10-20 Filters were calibrated over a very wide range
using the blue (halogen?) lamps. The transmission was saved
in the file NDfilter_stats.
"""
# Text file with the three filters [Wavelength (nm), Mr. Blue, Mr. White, Three sisters] raw transmission values
ndFilters_trans = np.loadtxt('NDfilter_stats.txt', comments='#', delimiter=',')
# The linear interpolation function of the three ND filters we use
mrBlue = interp1d(ndFilters_trans[:, 0], ndFilters_trans[:, 1]) # NE20A filter with blue 'A'
mrWhite = interp1d(ndFilters_trans[:, 0], ndFilters_trans[:, 2]) # NE20A filter with no coloring
mrTriplet = interp1d(ndFilters_trans[:, 0], ndFilters_trans[:, 3]) # Combination of three ND filters
filterBFWhite    = 0b001
filterBFBlue     = 0b010
filterBFTriplet  = 0b100


# Need a global reference for keeping the
# dialog popups, to prevent garbage collection
# Less stressful than having to manage class
# references
dialogList = []


plotColors = [pg.intColor(i, hues = 20,
                          values = 1,
                          maxValue = 255,
                          minValue = 150,
                          maxHue = 360,
                          minHue = 0,
                          sat = 255) for i in range(20)]

import itertools
plotColors = itertools.cycle(plotColors)


def group_data(data, deadtime = 8):
    """
    Given a list of numbers, group them up based on where
    they're continuous.
    i.e. into sets of [[n, n+1, n+2], [m, m+1, m+1+cutoff]]

    Use by passing in a set of indexes which come from
    np.where(cond)[0]

    :param deadtime: How large a gap to still be considered
     "continuous"
    """
    groupedData = []
    curData = []
    for d in list(data):
        if curData:
            if np.abs(d-curData[-1])>deadtime:
                groupedData.append(curData)
                curData = [d]
            else:
                curData.append(d)
        else:
            curData.append(d)
    groupedData.append(curData)
    return groupedData

def getPhotonCountedWaveform(wf, cutoff=20):
    """
    :type wf: np.ndarray
    """
    wfOrig = wf.copy()
    time = wfOrig[:,0]
    wf = wfOrig[:,1]
    photons = np.zeros_like(wf)

    flg = (wf>cutoff).astype(int)
    if np.any(flg): #empty
        pkGroups = group_data(np.where(flg)[0])

        peaks = []
        for gp in pkGroups:
            pkPos = gp[0] + np.argmax(wf[gp])
            peaks.append(pkPos)
        photons[peaks] = 1
    wfOrig[:,1] = photons

    return wfOrig

class MainWin(QtGui.QMainWindow):
    #emits when oscilloscope is done taking data so that
    #the data collecting thread knows it's ready to processes
    updateDataSig = QtCore.pyqtSignal()

    #emits when status bar needs updating.
    #Either a string or array of [str, int]
    #where str is message and int is time (ms) to display
    statusSig = QtCore.pyqtSignal(object)

    #Emits data from the oscillscope. Updates graphs
    pyDataSig = QtCore.pyqtSignal(object)
    pmDataSig = QtCore.pyqtSignal(object)

    # emits when PC data needs to be udpated
    sigPCData = QtCore.pyqtSignal(object)

    #emits the wavenumber changes so a child'ed SPEXWin can update.
    #order (wanted, got)
    wnUpdateSig = QtCore.pyqtSignal(object, object)

    #emit to update the boxcar values
    boxcarSig = QtCore.pyqtSignal(object, object, object)

    # Signal emitted each time a data point is taken, used
    # for updating graph in real time
    sigNewStep = QtCore.pyqtSignal()

    sigScanFinished = QtCore.pyqtSignal()
    
    #Thread which handles polling the oscilloscope
    scopeCollectionThread = None
    #Thread which handles scanning the SPEX and updating data, etc
    scanRunningThread = None
    def __init__(self):
        super(MainWin, self).__init__()
        self.initSettings()
        if self.checkSaveFile():
            self.loadSettings()


        self.initUI()
        # self.pyDataSig.connect(self.updatePyroGraph)
        self.pyDataSig.connect(self.oscWidget.setData)
        self.pmDataSig.connect(self.updatePMTGraph)
        self.sigPCData.connect(self.updatePCGraph)
        self.statusSig.connect(self.updateStatusBar)
        self.boxcarSig.connect(self.updateBoxcarTexts)
        self.sigNewStep.connect(self.updateScan)
        self.sigScanFinished.connect(self.finishScan)

        
        self.openSPEX()
        self.openAgi()
        self.SPEXWindow = None
        self.pulseWidth = 2e-6
        try:
            self.motorDriver = md.MotorWindow()
        except Exception as e:
            log.error("Error loading motor driver!")
            self.motorDriver = None
        
    def initUI(self):
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        #Initialize the plots (see imports at top for how to set the colors)

        self.pPMT = self.ui.gSignal.plot(pen='k')
        plotitem = self.ui.gSignal.getPlotItem()
        plotitem.setLabel('top',text='PMT')
        plotitem.setLabel('left',text='Voltage',units='V')
        plotitem.setLabel('bottom',text='Time', units='us')

        self.pScan = self.ui.gScan.plot(pen='k')
        self.ui.gScan.addLegend()
        plotitem = self.ui.gScan.getPlotItem()
        plotitem.setLabel('top',text='PMT')

        if not self.settings["saveWaveforms"]:
            plotitem.setLabel('left',text='Integrated Voltage',units='V')
            plotitem.setLabel('bottom',text='Wavenumber (cm-1)')
        if self.settings["saveWaveforms"]:
            plotitem.setLabel('left',text='Voltage',units='V')
            plotitem.setLabel('bottom',text='Time (us)')



        self.ui.linePCThreshold = pg.InfiniteLine(pos=self.settings['PCThreshold'], angle=0, movable=True)
        self.ui.gPC.p2.addItem(self.ui.linePCThreshold)
        self.ui.gPC.setXLabel("Time", units='s')
        self.ui.gPC.setY1Label("Photons")
        self.ui.gPC.setY2Label("PMT", units='V')

        self.ui.tPCThreshold.setText(str(self.settings['PCThreshold']))
        self.ui.linePCThreshold.sigPositionChanged.connect(self.updatePCThreshFromVal)
        self.ui.tPCThreshold.textAccepted.connect(self.updatePCThresFromText)

        if self.settings["doPC"]:
            pass
        else:
            self.ui.tabWidget.removeTab(1)


        self.initLinearRegionBounds()
        #Now we make an array of all the textboxes for the linear regions to make it
        #easier to iterate through them. Set it up in memory identical to how it
        #appears on the panel for sanity, in a row-major fashion
        lrtb = []
        lrtb.append([self.ui.tPmBgSt, self.ui.tPmBgEn])
        lrtb.append([self.ui.tPmSgSt, self.ui.tPmSgEn])

        d = {0: "bcpmBG",
             1: "bcpmSB"
        }
        for i, v in enumerate(lrtb):
            v[0].setText(str(self.settings[d[i]][0]))
            v[1].setText(str(self.settings[d[i]][1]))
        for i in lrtb:
            for j in i:
                j.textAccepted.connect(self.updateLinearRegionsFromText)
        
        self.linearRegionTextBoxes = lrtb
        
        
        self.ui.bChooseDirectory.clicked.connect(self.updateSaveLoc)
        self.ui.bQuickStart.clicked.connect(self.quickStartScan)
        self.ui.bStart.clicked.connect(self.startScan)
        self.ui.bPause.clicked[bool].connect(self.togglePause)
        self.ui.bPause.setChecked(not self.settings['notPaused'])
#        self.ui.bAbort.clicked.connect(lambda self=self: setattr(self, "settings['runningScan']", False))
        self.ui.bAbort.clicked.connect(self.abortScan)
        self.ui.bSaveWaveforms.clicked.connect(self.saveWaveforms)
        self.ui.bInitPMT.clicked.connect(self.initRegions)


        self.ui.tSaveName.editingFinished.connect(self.makeSaveDir)
        self.ui.bClearScan.clicked.connect(self.clearScans)

        self.ui.mFileSettings.triggered.connect(self.launchSettings)
        self.ui.mFileExit.triggered.connect(self.closeEvent)
        self.ui.mSpexOpen.triggered.connect(self.openSPEXWindow)

        self.ui.tSaveName.setText(self.settings['saveName'])
        self.ui.tSeries.setText(self.settings['seriesName'])
        self.ui.tSidebandNumber.setText(str(self.settings['autoSBN']))

        self.tGeneralSB = QtGui.QLabel()
        self.tbcPyroFP = QtGui.QLabel()
        self.tbcPyroCD = QtGui.QLabel()
        self.tbcPMSG = QtGui.QLabel()
        
        self.ui.statusbar.addPermanentWidget(self.tGeneralSB)
        self.ui.statusbar.addPermanentWidget(self.tbcPyroFP, 1)
        self.ui.statusbar.addPermanentWidget(self.tbcPyroCD, 1)
        self.ui.statusbar.addPermanentWidget(self.tbcPMSG, 1)

        # self.ui.splitter_2.setStretchFactor(0, 1)
        # self.ui.splitter_2.setStretchFactor(1, 1)
        self.oscWidget = OscWid(**self.settings)
        self.oscWidget.setParentScope(self)
        self.ui.splitter.insertWidget(0, self.oscWidget)

        
        
        self.show()
    def initSettings(self):
        #Initializes all the settings for the window in one tidy location,
        #make it have a more logical place if settings are saved and recalled eac
        #time
        s = dict()
        #Communication settings
        try:
            s['GPIBChoices'] = [i.encode("ascii") for i in visa.ResourceManager().list_resources()]
        except:
            s['GPIBChoices'] = ["a", "b", "c"]
        s['GPIBChoices'].append("Fake")
        s['aGPIB'] = 'USB0::0x0957::0x1734::MY44007041::INSTR' if 'USB0::0x0957::0x1734::MY44007041::INSTR' in s['GPIBChoices'] else "Fake"#GPIB of the agilent
        s['sGPIB'] = 'GPIB0::4::INSTR' if 'GPIB0::4::INSTR' in s['GPIBChoices'] else "Fake"#'GPIB0::4::INSTR' #GPIB of the SPEX
        s['pyCh'] = 3  #Osc channel for the pyro
        s['pmCh'] = 2  #osc channel for the pmt
        
        #saving settings
        s['saveLocation'] = '.'
        s['saveName'] = ''
        s['seriesName'] = ''
        s['saveComments'] = ''
        s['nir_power'] = 0 #NIR Power
        s['nir_lambda'] = 0 #NIR wavenumber
        s['fel_power'] = 0 #FEL power
        s['fel_lambda'] = 0 #FEL wavenumber
        s['temperature'] = 0
        s['pm_hv'] = 700 #PMT voltage
        s["filter"] = 0 # Which filter is in place?
        s['fel_reprate'] = 0.75

        s["autoSBN"] = 2 # automatic sideband, desired sb
        s["autoSBW"] = 4  # automatic SB, desired width
        
        #scan settings
        s['startWN'] = 0 #Starting wavenumber
        s['stepWN'] = -0.5 #how many wavenumbers to steop by
        s['endWN'] = 0 #Ending wavenumber
        s['ave'] = 10 #How many values to take an average of
        
        #running flags
        #Pausing causes the oscilloscope reading loop to wait until we are unpaused
        s['notPaused'] = False # start paused
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
        s['pcData'] = None # photon counted data
        s['pmData'] = None
        #wavenumber, ref FP, ref CD, signal
        s['allData'] = np.empty((0,4))
        s["allSignalWaveforms"] = np.empty((10000, 0))
        s["allReferenceWaveforms"] = np.empty((10000, 0))

        s['currentWN'] = 0
        s["saveWaveforms"] = False
        s["doPC"] = False
        s["PCThreshold"] = 0
        
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

    def abortScan(self):
        self.settings['runningScan'] = False
    def launchSettings(self):
        try:
            res = list(visa.ResourceManager().list_resources())
            res = [i.encode('ascii') for i in res]
        except:
            self.statusSig.emit(['Error loading GPIB list', 5000])
            res = ['a', 'b','c']
        res.append('Fake')
        self.settings['GPIBChoices'] = res
        self.settings["fel_power"] = str(self.oscWidget.ui.tFELP.text())
        self.settings["fel_lambda"] = str(self.oscWidget.ui.tFELFreq.text())
        self.settings["fel_reprate"] = str(self.oscWidget.ui.tFELRR.text())
        
        #need to pass a copy of the settings. Otherwise it passes the reference,
        #thus changing the values and we're unable to see whether things have changed.
        newSettings, ok = SettingsDialog.getSettings(self, copy.copy(self.settings))
        if not ok:
            return


        self.oscWidget.ui.tFELP.setText(str(newSettings["fel_power"]))
        self.oscWidget.ui.tFELFreq.setText(str(newSettings["fel_lambda"]))
        self.oscWidget.ui.tFELRR.setText(str(newSettings["fel_reprate"]))

        del newSettings['pcData']
        del newSettings['pmData']
        del newSettings['allData']
        # Update the sideband textbox if you used the
        # autocalculator to move to a new one.
        if not self.settings["autoSBN"] == newSettings["autoSBN"]:
            self.ui.tSidebandNumber.setText(str(newSettings["autoSBN"]))

        #Need to check to see if the GPIB values changed so we can update them.
        #The opening procedure opens a fake isntrument if things go wrong, which 
        #means we can't assign the settings dict after calling openKeith() as that would
        #potentially overwrite if we needed to open a fake instr.
        #
        #We get the old values before updating the settings. Th
        
        oldaGPIB = self.settings['aGPIB']
        oldsGPIB = self.settings['sGPIB']

        if self.settings["doPC"] and not newSettings["doPC"]:
            # No longer wanted
            self.ui.tabWidget.removeTab(1)
        elif not self.settings["doPC"] and newSettings["doPC"]:
            # Now wanted
            self.ui.tabWidget.insertTab(1, self.ui.tabPC, "Photon Counting")

        if self.settings["saveWaveforms"] and not newSettings["saveWaveforms"]:
            plotitem = self.ui.gScan.getPlotItem()
            plotitem.setLabel('left',text='Integrated Voltage',units='V')
            plotitem.setLabel('bottom',text='Wavenumber (cm-1)')
        if not self.settings["saveWaveforms"] and newSettings["saveWaveforms"]:
            plotitem = self.ui.gScan.getPlotItem()
            plotitem.setLabel('left',text='Voltage',units='V')
            plotitem.setLabel('bottom',text='Time (us)')

        self.settings.update(newSettings)
        log.debug("Old Agi GPIB: {}. New Agi GPIB: {}".format(oldaGPIB, newSettings['aGPIB']))
        if not oldaGPIB == newSettings['aGPIB']:
            self.Agil.close()
            self.settings['aGPIB'] = newSettings['aGPIB']
            self.openAgi()
        log.debug("Old SPEX GPIB: {}. New SPEX GPIB: {}".format(oldsGPIB, newSettings['sGPIB']))
        if not oldsGPIB == newSettings['sGPIB']:
            self.SPEX.close()
            self.settings['sGPIB'] = newSettings['sGPIB']
            self.openSPEX()

        
        #enforce the correct sign
        self.settings['stepWN'] = np.sign(self.settings['endWN']-self.settings['startWN'])*np.abs(
                    self.settings['stepWN'])
        self.saveSettings()
            
    def openSPEXWindow(self):
        if self.SPEXWindow is None:
            self.SPEXWindow = SPEXWin(SPEXInfo = self.SPEX, parent=self)
        else:
            self.SPEXWindow.raise_()
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
            self.settings['aGPIB'] = 'Fake'
            self.Agil = Agilent6000(self.settings['aGPIB'])
            
        # self.Agil.setTrigger()
        self.settings['collectingScope'] = True

        # Without these settings, the oscilloscope will only transfer
        # 1000 data points, which means a lot gets lost and the signal
        # can change quality significantly.
        # Maybe this can eventually be specified somewhere in the GUI?
        self.Agil.write("STOP")
        self.Agil.write(":WAV:POIN:MODE MAX")
        self.Agil.write(":WAV:POIN 10000")
        if isPaused:
            self.togglePause(True)
            
        self.scopeCollectionThread = threading.Thread(target = self.collectScopeLoop)
        self.scopeCollectionThread.start()

            
    def updateBoxcarTexts(self, v1=0, v2=0, v3=0):
        return
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
        
    def integrateData(self, data):
        dt = np.diff(data[:2,0])[0]

        pmBGbounds = self.boxcarRegions[0].getRegion()
        pmBGidx = self.findIndices(pmBGbounds, data[:,0])
        
        pmSGbounds = self.boxcarRegions[1].getRegion()
        pmSGidx = self.findIndices(pmSGbounds, data[:,0])


        if self.settings["doPC"]:
            pmBG = data[pmBGidx[0]:pmBGidx[1],1].sum()
            pmSG = data[pmSGidx[0]:pmSGidx[1],1].sum()
        else:
            pmBG = spi.simps(data[pmBGidx[0]:pmBGidx[1],1], data[pmBGidx[0]:pmBGidx[1], 0])/(
                pmBGidx[1] - pmBGidx[0]
            )/dt
            pmSG = spi.simps(data[pmSGidx[0]:pmSGidx[1],1], data[pmSGidx[0]:pmSGidx[1], 0])/(
                pmSGidx[1] - pmSGidx[0]
            )/dt


        return pmSG-pmBG


    @staticmethod
    def findIndices(values, dataset):
        """Given an ordered dataset and a pair of values, returns the indices which
           correspond to these bounds  """
        indx = list((dataset>values[0]) & (dataset<values[1]))
        # convert to string for easy finding
        st = ''.join([str(int(i)) for i in indx])
        start = st.find('1')
        if start == -1:
            start = 0
        end = (start + st[start:].find('0') if st[start:].find('0')!=-1 else len(indx))
        if end<=0:
            end = 1 + start
        return start, end

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

    def getSeries(self):
        sers = str(self.ui.tSeries.text())
        # try:
        #     s = {"fel_transmission": float(self.motorDriver.ui.tCosCalc.text())}
        # except:
        #     s = {"fel_transmission": 1.0}
        sers = sers.format(NIRP=self.settings['nir_power'],
                     NIRL=self.settings['nir_lambda'],
                     FELP=self.settings['fel_power'],
                     FELL=self.settings['fel_lambda'],
                     TEMP=self.settings['temperature'],
                     PMHV=self.settings['pm_hv'])
        return sers


    @staticmethod
    def _____LOOPING():pass


    def quickStartScan(self):
        if self.settings['nir_power'] == -1.0:
            self.settings['startWN'] = 13160
            self.settings['stepWN'] = -1
            self.settings['endWN'] = 13130
            self.settings['ave'] = 3
        elif self.settings['startWN']*self.settings['endWN'] == 0:
            self.statusSig.emit(['Please initialize scan settings', 10000])
            MessageDialog(self, "Please initialize scan settings.", 3000)
            return
        self.saveSettings()

        if self.settings["saveWaveforms"]:
            self.settings["allSignalWaveforms"] = np.empty((0, 0))
            self.settings["allReferenceWaveforms"] = np.empty((0, 0))
        else:
            #wavenumber, ref FP, ref CD, signal
            self.settings['allData'] = np.empty((0,4))

        self.updateScan() # clear the graph
        self.settings['runningScan'] = True
        self.ui.bStart.setEnabled(False)
        self.ui.bQuickStart.setEnabled(False)
        self.statusSig.emit(['Starting Scan', 3000])

        self.scanRunningThread = threading.Thread(target = self.runScanLoop)
        self.scanRunningThread.start()

    def startScan(self):
        """
        Called to open up settings to confirm
        PM HV and filters, which we often fuck up.
        :return:
        """
        sets, ok = QuickSettingsDialog.getSettings(self, self.settings)
        if not ok:
            return

        # Update the sideband textbox if you used the
        # autocalculator to move to a new one.

        print self.settings["autoSBN"], sets["autoSBN"]

        if not self.settings["autoSBN"] == sets["autoSBN"]:
            self.ui.tSidebandNumber.setText(str(sets["autoSBN"]))

        self.settings.update(sets)

        #enforce the correct sign
        self.settings['stepWN'] = np.sign(self.settings['endWN']-self.settings['startWN'])*np.abs(
                    self.settings['stepWN'])

        self.quickStartScan()

    def runScanLoop(self):
        # Lets the scope know to start counting pulses,
        # calculating fields, intensities and
        # emitting signals for it
        self.oscWidget.startExposure()
        if self.settings["stepWN"] == 0 or self.settings["saveWaveforms"]:
            WNRange = np.array([self.settings['endWN']])
        else:
            WNRange = np.arange(self.settings['startWN'],
                                    self.settings['endWN'], self.settings['stepWN'])
            WNRange = np.append(WNRange, self.settings['endWN'])

        for wavenumber in WNRange:
            if not self.settings['runningScan']:
                log.info('breaking scan')
                break
            self.settings['collectingData'] = False
            self.SPEX.gotoWN(wavenumber)
            self.statusSig.emit(['Wavenumber: {}/{}. No. {}/{}'.format(
                wavenumber, WNRange[-1], 0, self.settings['ave']), 0])
            self.wnUpdateSig.emit(str(wavenumber), str(self.SPEX.currentPositionWN))
            num = 0 # number of averages. Doing it this way so that if we want to implement
                    # something where we don't count a number, then we can decline decrementing
                    # effectively saying the point didn't happen
            missed = 0
            self.settings['collectingData'] = True
            while num < self.settings['ave']:
                if not self.settings['runningScan']:
                    break
                # Now want to take data. This means we need to wait for the oscilloscope to
                # finish collecting its current round. Enter a waiting loop.
                # Note: the event loop has to be instantiated here. I'm not sure why,
                # probably a main thread/worker thread/mutexing bullshit reason.
                #
                # Also note, it's connected to the oscWidget, which is really the
                # pyro widget. This signal will inform the thread whether
                # the pulse was valid or not, since it handles that logic
                self.waitingForDataLoop = QtCore.QEventLoop()
                self.oscWidget.sigPulseCounted.connect(self.waitingForDataLoop.exit)
                ret = self.waitingForDataLoop.exec_()

                # the exit value of the waiting loop is given by the signal from
                # oscWid, and is negative for missed pulses
                isValid = True
                if ret<0: isValid = False

                # If you don't disconnect it, you get a really bad memory leak
                # I think qt will keep an internal reference when you connect
                # signals/slots, and this was just creating a vast amount of
                # qeventloop's
                self.oscWidget.sigPulseCounted.disconnect(self.waitingForDataLoop.exit)


                if str(self.ui.tSidebandNumber.text()) == '0':
                    # Don't worry about FEL when looking at the
                    # laser line
                    isValid = True
                if isValid:
                    num += 1




                    # decide which data set we want
                    if self.settings["doPC"]:
                        data = self.settings["pcData"]
                    else:
                        data = self.settings["pmData"]



                    if self.settings["saveWaveforms"]:
                        pyD = self.oscWidget.getData()

                        oldpyD = self.settings['allReferenceWaveforms']
                        oldpmD = self.settings['allSignalWaveforms']

                        if pyD.shape[0] != oldpyD.shape[0]:
                            # This is the first one, grab the time as well
                            oldpyD = pyD.copy()
                            oldpmD = data.copy()
                        else:
                            # otherwise, we only want the data
                            oldpyD = np.column_stack((oldpyD, pyD.copy()[:,1]))
                            oldpmD = np.column_stack((oldpmD, data.copy()[:,1]))

                        self.settings['allReferenceWaveforms'] = oldpyD
                        self.settings['allSignalWaveforms'] = oldpmD

                    else:
                        # scale the data by the appropriate filters/HV setting
                        if self.settings['pm_hv'] == 700:
                            mult = 10
                        else:
                            mult = 1

                        data[:,1] *= mult # to account for the difference between 700 V and 1kV

                        # also account for the attenuation due to the filters
                        T = 1
                        T = T * mrWhite(1e7/wavenumber) if self.settings["filter"] & filterBFWhite else T
                        T = T * mrBlue(1e7/wavenumber) if self.settings["filter"] & filterBFBlue else T
                        T = T * mrTriplet(1e7/wavenumber) if self.settings["filter"] & filterBFTriplet else T
                        data[:,1] /= T

                        sig = self.integrateData(data)

                        self.settings['allData'] = np.append(
                            self.settings['allData'],
                            [[wavenumber,
                              self.oscWidget.settings["pyFP"],
                              self.oscWidget.settings["pyCD"],
                              sig]],
                            axis=0)
                else:
                    missed += 1
                self.sigNewStep.emit()
                self.statusSig.emit(['Wavenumber: {}/{}. No. {}({})/{}'.format(
                    wavenumber, WNRange[-1], num, missed, self.settings['ave']), 0])
        self.oscWidget.stopExposure()
        self.saveData()

        #clean up after done
        self.sigScanFinished.emit()

    """
    def runScanLoopOld(self):
        # Lets the scope know to start counting pulses,
        # calculating fields, intensities and
        # emitting signals for it
        self.oscWidget.startExposure()
        if self.settings["stepWN"] == 0 or self.settings["saveWaveforms"]:
            WNRange = np.array([self.settings['endWN']])
        else:
            WNRange = np.arange(self.settings['startWN'],
                                    self.settings['endWN'], self.settings['stepWN'])
            WNRange = np.append(WNRange, self.settings['endWN'])

        for wavenumber in WNRange:
            if not self.settings['runningScan']:
                log.info('breaking scan')
                break
            self.settings['collectingData'] = False
            self.SPEX.gotoWN(wavenumber)
            self.statusSig.emit(['Wavenumber: {}/{}. No. {}/{}'.format(
                wavenumber, WNRange[-1], 0, self.settings['ave']), 0])
            self.wnUpdateSig.emit(str(wavenumber), str(self.SPEX.currentPositionWN))
            num = 0 # number of averages. Doing it this way so that if we want to implement
                    # something where we don't count a number, then we can decline decrementing
                    # effectively saying the point didn't happen
            missed = 0
            self.settings['collectingData'] = True
            while num < self.settings['ave']:
                if not self.settings['runningScan']:
                    break
                # Now want to take data. This means we need to wait for the oscilloscope to
                # finish collecting its current round. Enter a waiting loop.
                # Note: the event loop has to be instantiated here. I'm not sure why,
                # probably a main thread/worker thread/mutexing bullshit reason.
                #
                # Also note, it's connected to the oscWidget, which is really the
                # pyro widget. This signal will inform the thread whether
                # the pulse was valid or not, since it handles that logic
                self.waitingForDataLoop = QtCore.QEventLoop()
                self.oscWidget.sigPulseCounted.connect(self.waitingForDataLoop.exit)
                ret = self.waitingForDataLoop.exec_()

                # the exit value of the waiting loop is given by the signal from
                # oscWid, and is negative for missed pulses
                isValid = True
                if ret<0: isValid = False

                # If you don't disconnect it, you get a really bad memory leak
                # I think qt will keep an internal reference when you connect
                # signals/slots, and this was just creating a vast amount of
                # qeventloop's
                self.oscWidget.sigPulseCounted.disconnect(self.waitingForDataLoop.exit)
                sig = self.integrateData()

                if self.settings['pm_hv'] == 700:
                    mult = 10
                    # print "700 V setting, mult = {}".format(mult)
                else:
                    mult = 1
                    # print "Not 700 V setting, {}, mult = {}".format(self.settings['pm_hv'], mult)

                sig *= mult # to account for the difference between 700 V and 1kV

                # also account for the attenuation due to the filters
                T = 1
                T = T * mrWhite(1e7/wavenumber) if self.settings["filter"] & filterBFWhite else T
                T = T * mrBlue(1e7/wavenumber) if self.settings["filter"] & filterBFBlue else T
                T = T * mrTriplet(1e7/wavenumber) if self.settings["filter"] & filterBFTriplet else T
                sig /= T

                if str(self.ui.tSidebandNumber.text()) == '0':
                    # Don't worry about FEL when looking at the
                    # laser line
                    isValid = True
                if isValid:
                    num += 1
                    if self.settings["saveWaveforms"]:
                        pyD = self.oscWidget.getData()
                        pmD = self.settings['pmData']
                        if self.settings["doPC"]:
                            pmD = getPhotonCountedWaveform(pmD, self.ui.linePCThreshold.value())

                        oldpyD = self.settings['allReferenceWaveforms']
                        oldpmD = self.settings['allSignalWaveforms']

                        if pyD.shape[0] != oldpyD.shape[0]:
                            # This is the first one, grab the time
                            oldpyD = pyD.copy()
                            oldpmD = pmD.copy()
                        else:
                            oldpyD = np.column_stack((oldpyD, pyD.copy()[:,1]))
                            oldpmD = np.column_stack((oldpmD, pmD.copy()[:,1]))

                        self.settings['allReferenceWaveforms'] = oldpyD
                        self.settings['allSignalWaveforms'] = oldpmD

                    else:
                        self.settings['allData'] = np.append(
                            self.settings['allData'],
                            [[wavenumber,
                              self.oscWidget.settings["pyFP"],
                              self.oscWidget.settings["pyCD"],
                              sig]],
                            axis=0)
                else:
                    missed += 1
                self.sigNewStep.emit()
                self.statusSig.emit(['Wavenumber: {}/{}. No. {}({})/{}'.format(
                    wavenumber, WNRange[-1], num, missed, self.settings['ave']), 0])
        self.oscWidget.stopExposure()
        filename = str(self.ui.tSaveName.text())

        # Automatically add the sideband to the filename,
        # using 'p' or 'm' prefix for positive or negative
        # (since you can't use '-6' and '+6' in filenames
        sb = str(self.ui.tSidebandNumber.text())
        if sb: # string is not empty
            if int(sb)>=0:
                filename += '_p{}'.format(abs(int(sb)))
            else:
                filename += '_m{}'.format(abs(int(sb)))

        filename += '_scanData'

        #save Data. Check if there are any in the folder yet
        files = glob.glob(os.path.join(self.settings['saveLocation'],str(self.ui.tSaveName.text())
                                       , filename + '*.txt'))
        num = len(files)

        if self.settings["saveWaveforms"]:
            data = self.settings['allSignalWaveforms']
            time = data[:,0]
            if self.settings["doPC"]:
                sigData = data[:,1:].sum(axis=1)
            else:
                sigData = data[:,1:].mean(axis=1)*1e3
            sigErr = data[:,1:].std(axis=1)/np.sqrt(data.shape[1]-1)*1e3
            data = self.settings['allReferenceWaveforms']
            refData = data[:,1:].mean(axis=1)*1e3
            refErr = data[:,1:].std(axis=1)/np.sqrt(data.shape[1]-1)*1e3

            saveData = np.column_stack((time, sigData,sigErr, refData, refErr))


            originheader = 'Time,PMT Signal,PMT MeanErr,Ref Signal,Ref MeanErr\n'
            if self.settings["doPC"]:
                originheader += 'ms,photons,,mV,mV\n'
            else:
                originheader += 'ms,mV,mV,mV,mV\n'
            originheader += 't,{} PMT,,{} Ref,'.format(self.getSeries(), self.getSeries())
            fmt = '%.10e'

        else:
            saveData = self.settings["allData"]
            originheader = 'Wavenumber, Integrated front porch, Integrated Cavity dump, integrated signal\n'
            originheader += 'cm-1, arb.u., arb.u., arb.u.'
            fmt = '%.18e'
        np.savetxt(os.path.join(
            self.settings['saveLocation'],str(self.ui.tSaveName.text()),'{}{}.txt'.format(filename, num)),
            saveData,
            header = '#'+self.genSaveHeader().replace('\n', '\n#') +  '\n'+originheader,
            comments='',
            delimiter=',',
            fmt = fmt)

        #clean up after done
        self.sigScanFinished.emit()
        """
    def finishScan(self):
        self.settings['collectingData'] = False
        self.settings['runningScan'] = False
        self.ui.bStart.setEnabled(True)
        self.ui.bQuickStart.setEnabled(True)

        if not self.settings["saveWaveforms"]:
            # Plot the new data as an independent line
            data = self.settings["allData"]
            # Find duplicates. wnIdx is a list such that
            # d[i, 0] = wn[wnIdx[i]]
            wn, wnIdx = np.unique(data[:,0], return_inverse=True)
            # make a nan array for easy summing
            newData = np.empty((len(wn), len(wnIdx) ))
            newData.fill(np.nan)

            # Set the array of data
            # This separates it so all of the data for one
            # wavenumber is in one row, and the rest are nan
            newData[wnIdx, range(len(data[:,3]))] = data[:,3]
            # sum over them, ignoring the nan values
            newVal = np.nanmean(newData, axis=1)
            errs = np.nanstd(newData, axis=1)/np.sqrt(
                np.sum(1-np.isnan(newData), axis=1)
            )
            label = self.getSeries() + '_' + str(self.ui.tSidebandNumber.text())
            col = plotColors.next()
            self.ui.gScan.errorbars(x=wn, y=newVal, errorbars=errs, pen=col, name=label)
        else:
            data = self.settings['allSignalWaveforms']
            time = data[:,0]
            data = data[:, 1:].mean(axis=1)
            label = self.getSeries() + '_' + str(self.ui.tSidebandNumber.text())
            col = plotColors.next()
            self.ui.gScan.plot(x=time, y=data, name=label, pen=col)
        self.statusSig.emit(['Done', 3000])

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
                self.pmDataSig.emit(pmData)
                if self.settings["doPC"]:
                    self.sigPCData.emit(pmData)
                self.pyDataSig.emit(pyData)
#            time.sleep(.5)

    @staticmethod
    def _____GRAPH_UPDATES():pass

    def initRegions(self):
        sent = self.sender()
        if sent is self.ui.bInitPMT:
            boxcarRegions = self.boxcarRegions # the ones for the PMT
            try:
                length = len(self.settings['pmData'])
                point = self.settings['pmData'][length/2,0]
            except:
                return

        # set all of the linear regions
        # [[i.setText(str(point)) for i in j] for j in zip(*linearRegions)]
        # [[i.setText(str(point)) for i in j] for j in zip(*linearRegions)]
        [i.setRegion((point, point)) for i in boxcarRegions]

    def initLinearRegionBounds(self):
        #initialize array for all 5 boxcar regions
        self.boxcarRegions = [None]*2

        bgCol = pg.mkBrush(QtGui.QColor(255, 0, 0, 50))
        sgCol = pg.mkBrush(QtGui.QColor(0, 255, 0, 50))

        #Background region for the pyro plot
        self.boxcarRegions[0] = pg.LinearRegionItem(self.settings['bcpmBG'], brush = bgCol)
        self.boxcarRegions[1] = pg.LinearRegionItem(self.settings['bcpmSB'], brush = sgCol)

        #Connect it all to something that will update values when these all change
        for i in self.boxcarRegions:
            i.sigRegionChangeFinished.connect(self.updateLinearRegionValues)


        self.ui.gSignal.addItem(self.boxcarRegions[0])
        self.ui.gSignal.addItem(self.boxcarRegions[1])


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

        # Restrict it so the sideband signal is always 40ns
        # (width of the cavity dump)
        if sendidx == 4:
            a = list(sender.getRegion())
            a[1] = a[0]+self.pulseWidth
            sender.setRegion(a)
        d = {0: "bcpyBG",
             1: "bcpyFP",
             2: "bcpyCD",
             3: "bcpmBG",
             4: "bcpmSB"
        }
        self.settings[d[i]] = list(sender.getRegion())
        self.saveSettings()

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
        if i==4:
            self.linearRegionTextBoxes[i][1-j].blockSignals(True)
            self.linearRegionTextBoxes[i][1-j].setText(str(
                float(sender.text()) + (-1)**(j) * self.pulseWidth)
            )
            self.linearRegionTextBoxes[i][1-j].blockSignals(False)
            # sender.setText(str(
            #     float(self.linearRegionTextBoxes[-1][0].text())+40e-9
            # ))
            curVals = [float(ii.text()) for ii in self.linearRegionTextBoxes[i]]
        else:
            curVals = list(self.boxcarRegions[i].getRegion())
            curVals[j] = float(sender.text())

        self.boxcarRegions[i].blockSignals(True)
        self.boxcarRegions[i].setRegion(tuple(curVals))
        self.boxcarRegions[i].blockSignals(False)

        d = {0: "bcpyBG",
             1: "bcpyFP",
             2: "bcpyCD",
             3: "bcpmBG",
             4: "bcpmSB"
        }
        self.settings[d[i]] = list(curVals)
        self.saveSettings()


    def updatePCThreshFromVal(self, lin):
        self.ui.tPCThreshold.blockSignals(True)
        self.ui.tPCThreshold.setText("{}".format(lin.value()))
        self.ui.tPCThreshold.blockSignals(False)

    def updatePCThresFromText(self, val):
        self.ui.linePCThreshold.blockSignals(True)
        self.ui.linePCThreshold.setPos(val)
        self.ui.linePCThreshold.blockSignals(False)

    def updatePMTGraph(self, data):
        self.settings['pmData'] = data
        self.pPMT.setData(data[:,0], data[:,1])

    def updatePCGraph(self, data):
        self.ui.gPC.setY2Data(data)
        pcdata = getPhotonCountedWaveform(data, self.ui.linePCThreshold.value())
        self.settings["pcData"] = pcdata
        self.ui.gPC.setY1Data(pcdata)


    def updateScan(self):
        """

        """
        # if wn is None or newVal is None:
        if not self.settings["saveWaveforms"]:
            data = self.settings["allData"]
            # Find duplicates. wnIdx is a list such that
            # d[i, 0] = wn[wnIdx[i]]
            wn, wnIdx = np.unique(data[:,0], return_inverse=True)
            # make a nan array for easy summing
            newData = np.empty((len(wn), len(wnIdx) ))
            newData.fill(np.nan)

            # Set the array of data
            # This separates it so all of the data for one
            # wavenumber is in one row, and the rest are nan
            newData[wnIdx, range(len(data[:,3]))] = data[:,3]
            # sum over them, ignoring the nan values
            newVal = np.nanmean(newData, axis=1)
        else:
            data = self.settings['allSignalWaveforms']
            # nothing collected yet
            if 0 in data.shape:
                wn = []
                newVal = []
            else:
                wn = data[:,0]
                newVal = data[:,1:].mean(axis=1)
                if self.settings["doPC"]:
                    self.ui.gPC.setY2Data(self.settings['pmData'])
                    self.ui.gPC.setY1Data(wn, data[:,1:].sum(axis=1))
        self.pScan.setData(wn, newVal)

    def clearScans(self):
        self.ui.gScan.clear()
        self.ui.gScan.plotItem.legend.items = []
        self.ui.gScan.addItem(self.pScan)


    @staticmethod
    def _____SAVING():pass

    def saveData(self):
        filename = str(self.ui.tSaveName.text())

        # Automatically add the sideband to the filename,
        # using 'p' or 'm' prefix for positive or negative
        # (since you can't use '+6' in filenames
        sb = str(self.ui.tSidebandNumber.text())
        if sb: # string is not empty
            if int(sb)>=0:
                filename += '_p{}'.format(abs(int(sb)))
            else:
                filename += '_m{}'.format(abs(int(sb)))

        filename += '_scanData'

        #save Data. Check if there are any in the folder yet
        files = glob.glob(os.path.join(self.settings['saveLocation'],str(self.ui.tSaveName.text())
                                       , filename + '*.txt'))
        num = len(files)

        if self.settings["saveWaveforms"]:
            data = self.settings['allSignalWaveforms']
            time = data[:,0]
            if self.settings["doPC"]:
                sigData = data[:,1:].sum(axis=1)
            else:
                sigData = data[:,1:].mean(axis=1)
            sigErr = data[:,1:].std(axis=1)/np.sqrt(data.shape[1]-1)
            data = self.settings['allReferenceWaveforms']
            refData = data[:,1:].mean(axis=1)
            refErr = data[:,1:].std(axis=1)/np.sqrt(data.shape[1]-1)

            saveData = np.column_stack((time, sigData,sigErr, refData, refErr))


            originheader = 'Time,PMT Signal,PMT MeanErr,Ref Signal,Ref MeanErr\n'
            if self.settings["doPC"]:
                originheader += 'us,photons,,V,V\n'
            else:
                originheader += 'ms,V,V,V,V\n'
            originheader += 't,{} PMT,,{} Ref,'.format(self.getSeries(), self.getSeries())
            fmt = '%.10e'

        else:
            saveData = self.settings["allData"]
            originheader = 'Wavenumber, Integrated front porch, Integrated Cavity dump, integrated signal\n'
            originheader += 'cm-1,arb.u.,arb.u.,arb.u.\n'
            originheader += 'cm-1,{} FP,{} CD,{} Sig'.format(*[self.getSeries()]*3)
            fmt = '%.18e'
        np.savetxt(os.path.join(
            self.settings['saveLocation'],str(self.ui.tSaveName.text()),'{}{}.txt'.format(filename, num)),
            saveData,
            header = self.genSaveHeader()+originheader,
            comments='',
            delimiter=',',
            fmt = fmt)

    def updateSaveLoc(self):
        fname = str(QtGui.QFileDialog.getExistingDirectory(self, "Choose File Directory...",directory=self.settings['saveLocation']))
        if fname == '':
            return
        self.settings['saveLocation'] = fname + '/'

    def makeSaveDir(self):
        specFold = os.path.join(self.settings["saveLocation"],
                                 str(self.ui.tSaveName.text()))
        if not os.path.exists(specFold):
            try:
                os.mkdir(specFold)
            except Exception as e:
                log.warning("Could not make folder for data {}. Error: {}".format(specFold, e))

    def genSaveHeader(self):
        #Return a string of header information required for processing
        s = dict()
        s['nir_power'] = self.settings['nir_power']
        s['nir_lambda'] = self.settings['nir_lambda']
        s['pm_hv'] = self.settings['pm_hv']
        s['temperature'] = self.settings['temperature']
        s['series'] = self.getSeries()
        s["filter"] = ''
        s["filter"] = s["filter"] + 'White ' if self.settings["filter"] & filterBFWhite else s["filter"]
        s["filter"] = s["filter"] + 'Blue ' if self.settings["filter"] & filterBFBlue else s["filter"]
        s["filter"] = s["filter"] + 'Triplet ' if self.settings["filter"] & filterBFTriplet else s["filter"]

        # assume transmission is flat enough that it
        # can be approximated at the end
        aveWN = np.mean(self.settings['endWN'])
        # add the actual transmission used, useful if you want
        # to get the actual scope voltage by multiplying by
        # this transmission
        T = 1
        T = T * mrWhite(1e7/aveWN) if self.settings["filter"] & filterBFWhite else T
        T = T * mrBlue(1e7/aveWN) if self.settings["filter"] & filterBFBlue else T
        T = T * mrTriplet(1e7/aveWN) if self.settings["filter"] & filterBFTriplet else T
        s["filterTrans"] = T
        s["boxcar_pyroBackground"] = self.oscWidget.boxcarRegions[0].getRegion()
        s["boxcar_pyroFP"] = self.oscWidget.boxcarRegions[1].getRegion()
        s["boxcar_pyroSignal"] = self.oscWidget.boxcarRegions[2].getRegion()
        s["boxcar_PMTBackground"] = self.boxcarRegions[0].getRegion()
        s["boxcar_PMTSignal"] = self.boxcarRegions[1].getRegion()
        s["date"] = time.strftime('%x')

        if self.settings["saveWaveforms"]:
            s["SPEXFreq"] = self.settings['endWN']
            s["numAve"] = self.settings['ave']
            if self.settings["doPC"]:
                s["PCThreshold"] = self.ui.tPCThreshold.value()

        s.update(self.oscWidget.getExposureResults())
        st = str(self.ui.tSidebandNumber.text()) + "\n"
        s.update({"comments": self.settings['saveComments']})
        st += json.dumps(s, separators=(',', ': '),
                      sort_keys=True, indent=4 ) + "\n"
        # st += self.settings['saveComments']
        # Gotta do this manually so we can specify
        # an origin header without too much dancing
        st = '#' + st.replace('\n', '\n#') + '\n'
        return  st

    def saveWaveforms(self):
        """
        This saves the waveforms which are immediately on the
        screen when the 'Save Waveforms' button is selected
        :return:
        """
        pyro = self.oscWidget.getData()
        sig = self.settings['pmData']

        if sig is None: #it's empty
            return

        num = 1
        files = glob.glob(self.settings['saveLocation'] + str(self.ui.tSaveName.text()) + '_referenceDetector*.txt')

        oh = 'Voltage,Time\n'
        oh += 'V,us\n'
        oh += ',{}'.format(self.getSeries())

        num = str(len(files) * num) if len(files)>0 else ''
        np.savetxt(
            self.settings['saveLocation'] + str(self.ui.tSaveName.text()) + '_referenceDetector' + num + '.txt',
            pyro, header = self.genSaveHeader()+oh,
            delimiter=',',
            comments='')



        num = 1
        files = glob.glob(self.settings['saveLocation'] + str(self.ui.tSaveName.text()) + '_signalWaveform*.txt')

        num = str(len(files) * num) if len(files)>0 else ''
        np.savetxt(
            self.settings['saveLocation'] + str(self.ui.tSaveName.text()) + '_signalWaveform' + num + '.txt',
            sig, header = self.genSaveHeader()+oh,
            delimiter=',',
            comments='')
        # np.savetxt(self.settings['saveLocation'] + str(self.ui.tSaveName.text()) + '_signalWaveform.txt',
        #            sig, header = self.genSaveHeader()+'Voltage (V), Time(s)')

    def saveScanWaveforms(self):
        """
        This function gets called when the user has selected
        to save the averaged waveforms, instead of the
        boxcar values.
        :return:
        """
        pass


    @staticmethod
    def _____STATE_SAVING():pass

    @staticmethod
    def checkSaveFile():
        """
        This will check to see wheteher there's a previous settings file,
        and if it's recent enough that it should be loaded
        :return:
        """
        if not os.path.isfile('Settings.txt'):
            # File doesn't exist
            return False
        if (time.time() - os.path.getmtime('Settings.txt')) > 120 * 60:
            # It's been longer than 5 minutes and likely isn't worth
            # keeping open
            return False
        try:
            with open('Settings.txt') as fh:
                json.load(fh)
        except ValueError:
            return False


        return True

    def saveSettings(self):
        saveDict = {}
        saveDict.update(self.settings)
        badkeys=['pyData',
                'pmData',
                'allData',
                'GPIBChoices',
                'runningScan',
                'allSignalWaveforms',
                'allReferenceWaveforms']
        s = self.oscWidget.getSaveSettings()
        s.update({
            'bcpmBG': self.boxcarRegions[0].getRegion(),
            'bcpmSB': self.boxcarRegions[1].getRegion()
        })
        saveDict.update(s)


        for k in badkeys:
            try:
                del saveDict[k]
            except KeyError:
                pass
        saveDict['saveName'] = str(self.ui.tSaveName.text())
        saveDict['seriesName'] = str(self.ui.tSeries.text())
        saveDict['PCThreshold'] = self.ui.tPCThreshold.value()



        with open('Settings.txt', 'w') as fh:
            json.dump(saveDict, fh, separators=(',', ': '),
                      sort_keys=True, indent=4, default=lambda x: 'NotSerial')

    def loadSettings(self):
        with open('Settings.txt') as fh:
            savedDict = json.load(fh)
        if not 'aGPIB' in savedDict:
            del savedDict['aGPIB']
        if not 'sGPIB' in savedDict:
            del savedDict['sGPIB']

        self.settings.update(savedDict)

    def closeEvent(self, event):
        self.saveSettings()
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


class QuickSettingsDialog(QtGui.QDialog):
    def __init__(self, parent = None, settings=None):
        super(QuickSettingsDialog, self).__init__(parent)
        self.initUI(settings)

        self.FELLam = float(settings["fel_lambda"])
        self.NIRLam = float(settings["nir_lambda"])

        if self.FELLam * self.NIRLam > 0: # both are non-zero
            self.calcSBBoxes = [ #Easy iteration list
                self.ui.tGotoBound,
                self.ui.tGotoSB
            ]
            [i.textAccepted.connect(self.calcAutoSB) for i in self.calcSBBoxes]


    def initUI(self, settings):
        self.ui = Ui_QuickSettings()
        self.ui.setupUi(self)

        self.ui.tStartWN.setText(str(settings['startWN']))
        self.ui.tStepWN.setText(str(settings['stepWN']))
        self.ui.tEndWN.setText(str(settings['endWN']))
        self.ui.tAverages.setText(str(settings['ave']))



        self.ui.tGotoBound.setText(str(settings["autoSBW"]))
        self.ui.tGotoSB.setText(str(settings["autoSBN"]))

        self.ui.cbPMHV.setCurrentIndex(
            self.ui.cbPMHV.findText(str(settings["pm_hv"]))
        )

        self.ui.cbFilterWhite.setChecked(
            settings["filter"] & filterBFWhite
        )
        self.ui.cbFilterBlue.setChecked(
            settings["filter"] & filterBFBlue
        )
        self.ui.cbFilterTriplet.setChecked(
            settings["filter"] & filterBFTriplet
        )

        if settings['runningScan']:
            self.ui.tAverages.setEnabled(False)
            self.ui.tStartWN.setEnabled(False)
            self.ui.tStepWN.setEnabled(False)
            self.ui.tEndWN.setEnabled(False)


        enabled = settings["saveWaveforms"]
        self.ui.lStartWN.setVisible(not enabled)
        self.ui.tStartWN.setVisible(not enabled)
        self.ui.tStepWN.setVisible(not enabled)
        self.ui.lStepWN.setVisible(not enabled)
        if enabled:
            self.ui.lEndWN.setText("Wavenumber")
        else:
            self.ui.lEndWN.setText("Ending WN")

    @staticmethod
    def getSettings(parent = None, settings = None):
        dialog = QuickSettingsDialog(parent, settings)
        result = dialog.exec_()

        s = dict()
        s['startWN'] = dialog.ui.tStartWN.value()
        s['stepWN'] = dialog.ui.tStepWN.value()
        s['endWN'] = dialog.ui.tEndWN.value()
        s['ave'] = dialog.ui.tAverages.value()

        s['pm_hv'] = int(dialog.ui.cbPMHV.currentText())
        s["filter"] = filterBFWhite * int(dialog.ui.cbFilterWhite.isChecked()) | \
            filterBFBlue * int(dialog.ui.cbFilterBlue.isChecked()) | \
            filterBFTriplet * int(dialog.ui.cbFilterTriplet.isChecked())

        s["autoSBN"] = int(dialog.ui.tGotoSB.value())
        s["autoSBW"] = int(dialog.ui.tGotoBound.value())

        return (s, result==QtGui.QDialog.Accepted)

    def calcAutoSB(self):
        # if 0 in [int(i.value()) for i in self.calcSBBoxes]:
        #     return


        sbWN = self.NIRLam + \
               self.FELLam * self.ui.tGotoSB.value()
        bound = self.ui.tGotoBound.value()

        self.ui.tStartWN.setText(str(int(sbWN + bound)))
        # self.ui.tStepWN.setText("-1")
        self.ui.tEndWN.setText(str(int(sbWN - bound)))


    def calcNIRLam(self, val):
        if val<10000:
            self.ui.tNIRLam.setText("{:.1f}".format(10000000./val))
        self.calcAutoSB()

class SettingsDialog(QtGui.QDialog):
    def __init__(self, parent = None, settings=None):
        super(SettingsDialog, self).__init__(parent)
        self.initUI(settings)
        self.calcSBBoxes = [ #Easy iteration list
            self.ui.tFELLam,
            self.ui.tGotoBound,
            self.ui.tGotoSB
        ]
        [i.textAccepted.connect(self.calcAutoSB) for i in self.calcSBBoxes]
        self.ui.cbSaveWaveforms.toggled.connect(self.toggleWFs)
        self.toggleWFs(settings["saveWaveforms"])

        self.calcSBBoxes.pop(self.calcSBBoxes.index(self.ui.tGotoSB))
        # Want this to be connected to something else so
        # you can parse a nm input
        self.ui.tNIRLam.textAccepted.connect(self.calcNIRLam)
        # But still want to iterate over later
        self.calcSBBoxes.append(self.ui.tNIRLam)
        
    def initUI(self, settings):
        self.ui = Ui_Settings()
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

        self.ui.tGotoBound.setText(str(settings["autoSBW"]))
        self.ui.tGotoSB.setText(str(settings["autoSBN"]))
        
        self.ui.tNIRP.setText(str(settings['nir_power']))
        self.ui.tNIRLam.setText(str(settings['nir_lambda']))
        self.ui.cbPMHV.setCurrentIndex(
            self.ui.cbPMHV.findText(str(settings["pm_hv"]))
        )

        self.ui.cbFilterWhite.setChecked(
            settings["filter"] & filterBFWhite
        )
        self.ui.cbFilterBlue.setChecked(
            settings["filter"] & filterBFBlue
        )
        self.ui.cbFilterTriplet.setChecked(
            settings["filter"] & filterBFTriplet
        )

        self.ui.tFELP.setText(str(settings['fel_power']))
        self.ui.tFELLam.setText(str(settings['fel_lambda']))
        self.ui.tRepRate.setText(str(settings['fel_reprate']))
        self.ui.tTemp.setText(str(settings['temperature']))
        self.ui.tSaveComments.setText(settings['saveComments'])

        self.ui.cbSaveWaveforms.setChecked(settings["saveWaveforms"])
        self.ui.cbPC.setEnabled(True)
        self.ui.cbPC.setChecked(settings["doPC"])

        
        if settings['runningScan']:
            self.ui.tAverages.setEnabled(False)
            self.ui.tStartWN.setEnabled(False)
            self.ui.tStepWN.setEnabled(False)
            self.ui.tEndWN.setEnabled(False)
        # self.setWindowModality(QtCore.Qt.WindowModal)

    @staticmethod
    def getSettings(parent = None, settings = None):
        dialog = SettingsDialog(parent, settings)
        result = dialog.exec_()
        # loop = QtCore.QEventLoop()
        # dialog.buttonClicked.connect(loop.exit)
        settings['aGPIB'] = str(dialog.ui.cAGPIB.currentText())
        settings['sGPIB'] = str(dialog.ui.cSGPIB.currentText())
        settings['startWN'] = dialog.ui.tStartWN.value()
        settings['stepWN'] = dialog.ui.tStepWN.value()
        settings['endWN'] = dialog.ui.tEndWN.value()
        settings['ave'] = dialog.ui.tAverages.value()
        settings['pyCh'] = int(dialog.ui.cPyroCh.currentText())
        settings['pmCh'] = int(dialog.ui.cPMCh.currentText())
        settings['nir_power'] = dialog.ui.tNIRP.value()
        settings['nir_lambda'] = dialog.ui.tNIRLam.value()
        settings['pm_hv'] = int(dialog.ui.cbPMHV.currentText())

        settings["filter"] = filterBFWhite * int(dialog.ui.cbFilterWhite.isChecked()) | \
            filterBFBlue * int(dialog.ui.cbFilterBlue.isChecked()) | \
            filterBFTriplet * int(dialog.ui.cbFilterTriplet.isChecked())


        settings["autoSBN"] = int(dialog.ui.tGotoSB.value())
        settings["autoSBW"] = int(dialog.ui.tGotoBound.value())
        settings['fel_power'] = dialog.ui.tFELP.value()
        settings['fel_lambda'] = dialog.ui.tFELLam.value()
        settings['fel_reprate'] = dialog.ui.tRepRate.value()
        settings['temperature'] = dialog.ui.tTemp.value()
        settings['saveComments'] = str(dialog.ui.tSaveComments.toPlainText())
        settings["saveWaveforms"] = bool(dialog.ui.cbSaveWaveforms.isChecked())
        settings["doPC"] = bool(dialog.ui.cbPC.isChecked())


        # print '-'*10
        # print "Settings things"
        # print '-'*10
        # print result
        # print dialog.clickedButton()
        # print dialog.buttonRole(dialog.clickedButton())
        # print '-'*10

        return (settings, result==QtGui.QDialog.Accepted)



    def calcAutoSB(self):
        if 0 in [int(i.value()) for i in self.calcSBBoxes]:
            return
        sbWN = self.ui.tNIRLam.value() + \
               self.ui.tFELLam.value() * self.ui.tGotoSB.value()
        bound = self.ui.tGotoBound.value()

        self.ui.tStartWN.setText(str(int(sbWN + bound)))
        # self.ui.tStepWN.setText("-1")
        self.ui.tEndWN.setText(str(int(sbWN - bound)))

    def calcNIRLam(self, val):
        if val<10000:
            self.ui.tNIRLam.setText("{:.1f}".format(10000000/val))
        self.calcAutoSB()

    def toggleWFs(self, enabled):
        self.ui.lStartWN.setVisible(not enabled)
        self.ui.tStartWN.setVisible(not enabled)
        self.ui.tStepWN.setVisible(not enabled)
        self.ui.lStepWN.setVisible(not enabled)
        if enabled:
            self.ui.lEndWN.setText("Wavenumber")
        else:
            self.ui.lEndWN.setText("Ending WN")

class MessageDialog(QtGui.QDialog):
    def __init__(self, parent, message="", duration=3000):
        if isinstance(parent, str):
            message = parent
            parent = None
        super(MessageDialog, self).__init__(parent=parent)
        layout  = QtGui.QVBoxLayout(self)
        text = QtGui.QLabel("<font size='6'>{}</font>".format(message), self)
        layout.addWidget(text)
        self.setLayout(layout)
        self.setModal(False)

        dialogList.append(self)

        self.timer = QtCore.QTimer.singleShot(duration, self.close)
        self.show()
        self.raise_()

    def close(self):
        try:
            dialogList.remove(self)
        except Exception as E:
            print "ERror removing from list, ",E

        super(MessageDialog, self).close()












def main():
    import sys
    app = QtGui.QApplication(sys.argv)
    ex = MainWin()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()


