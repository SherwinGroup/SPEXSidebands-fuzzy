# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\dvalovcin\Documents\GitHub\SPEXSidebands-fuzzy\MainWindow.ui'
#
# Created: Fri Oct 23 10:25:26 2015
#      by: PyQt4 UI code generator 4.10.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(823, 503)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.tabWidget = QtGui.QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName(_fromUtf8("tabWidget"))
        self.tab = QtGui.QWidget()
        self.tab.setObjectName(_fromUtf8("tab"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.tab)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.gPyro = PlotWidget(self.tab)
        self.gPyro.setObjectName(_fromUtf8("gPyro"))
        self.horizontalLayout_2.addWidget(self.gPyro)
        self.gSignal = PlotWidget(self.tab)
        self.gSignal.setObjectName(_fromUtf8("gSignal"))
        self.horizontalLayout_2.addWidget(self.gSignal)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)
        self.gridLayout_2 = QtGui.QGridLayout()
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.tPmBgEn = QFNumberEdit(self.tab)
        self.tPmBgEn.setObjectName(_fromUtf8("tPmBgEn"))
        self.gridLayout_2.addWidget(self.tPmBgEn, 1, 9, 1, 1)
        self.tPmSgEn = QFNumberEdit(self.tab)
        self.tPmSgEn.setObjectName(_fromUtf8("tPmSgEn"))
        self.gridLayout_2.addWidget(self.tPmSgEn, 1, 11, 1, 1)
        self.tPyFpEn = QFNumberEdit(self.tab)
        self.tPyFpEn.setObjectName(_fromUtf8("tPyFpEn"))
        self.gridLayout_2.addWidget(self.tPyFpEn, 1, 4, 1, 1)
        self.label_11 = QtGui.QLabel(self.tab)
        self.label_11.setObjectName(_fromUtf8("label_11"))
        self.gridLayout_2.addWidget(self.label_11, 1, 10, 1, 1)
        self.tPyCdEn = QFNumberEdit(self.tab)
        self.tPyCdEn.setObjectName(_fromUtf8("tPyCdEn"))
        self.gridLayout_2.addWidget(self.tPyCdEn, 1, 6, 1, 1)
        self.tPmBgSt = QFNumberEdit(self.tab)
        self.tPmBgSt.setObjectName(_fromUtf8("tPmBgSt"))
        self.gridLayout_2.addWidget(self.tPmBgSt, 0, 9, 1, 1)
        self.tPyFpSt = QFNumberEdit(self.tab)
        self.tPyFpSt.setObjectName(_fromUtf8("tPyFpSt"))
        self.gridLayout_2.addWidget(self.tPyFpSt, 0, 4, 1, 1)
        self.tPyBgSt = QFNumberEdit(self.tab)
        self.tPyBgSt.setObjectName(_fromUtf8("tPyBgSt"))
        self.gridLayout_2.addWidget(self.tPyBgSt, 0, 2, 1, 1)
        self.label_9 = QtGui.QLabel(self.tab)
        self.label_9.setObjectName(_fromUtf8("label_9"))
        self.gridLayout_2.addWidget(self.label_9, 1, 5, 1, 1)
        self.label_10 = QtGui.QLabel(self.tab)
        self.label_10.setObjectName(_fromUtf8("label_10"))
        self.gridLayout_2.addWidget(self.label_10, 1, 8, 1, 1)
        self.label_7 = QtGui.QLabel(self.tab)
        self.label_7.setObjectName(_fromUtf8("label_7"))
        self.gridLayout_2.addWidget(self.label_7, 1, 1, 1, 1)
        self.label_6 = QtGui.QLabel(self.tab)
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.gridLayout_2.addWidget(self.label_6, 0, 10, 1, 1)
        self.label_3 = QtGui.QLabel(self.tab)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.gridLayout_2.addWidget(self.label_3, 0, 3, 1, 1)
        self.label_8 = QtGui.QLabel(self.tab)
        self.label_8.setObjectName(_fromUtf8("label_8"))
        self.gridLayout_2.addWidget(self.label_8, 1, 3, 1, 1)
        self.label_4 = QtGui.QLabel(self.tab)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.gridLayout_2.addWidget(self.label_4, 0, 5, 1, 1)
        self.label_5 = QtGui.QLabel(self.tab)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.gridLayout_2.addWidget(self.label_5, 0, 8, 1, 1)
        self.tPyBgEn = QFNumberEdit(self.tab)
        self.tPyBgEn.setObjectName(_fromUtf8("tPyBgEn"))
        self.gridLayout_2.addWidget(self.tPyBgEn, 1, 2, 1, 1)
        self.tPyCdSt = QFNumberEdit(self.tab)
        self.tPyCdSt.setObjectName(_fromUtf8("tPyCdSt"))
        self.gridLayout_2.addWidget(self.tPyCdSt, 0, 6, 1, 1)
        self.tPmSgSt = QFNumberEdit(self.tab)
        self.tPmSgSt.setObjectName(_fromUtf8("tPmSgSt"))
        self.gridLayout_2.addWidget(self.tPmSgSt, 0, 11, 1, 1)
        self.label_2 = QtGui.QLabel(self.tab)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout_2.addWidget(self.label_2, 0, 1, 1, 1)
        self.bInitPyro = QtGui.QPushButton(self.tab)
        self.bInitPyro.setObjectName(_fromUtf8("bInitPyro"))
        self.gridLayout_2.addWidget(self.bInitPyro, 0, 7, 1, 1)
        self.bInitPMT = QtGui.QPushButton(self.tab)
        self.bInitPMT.setObjectName(_fromUtf8("bInitPMT"))
        self.gridLayout_2.addWidget(self.bInitPMT, 1, 7, 1, 1)
        self.verticalLayout_2.addLayout(self.gridLayout_2)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.groupBox_3 = QtGui.QGroupBox(self.tab)
        self.groupBox_3.setFlat(True)
        self.groupBox_3.setObjectName(_fromUtf8("groupBox_3"))
        self.horizontalLayout_7 = QtGui.QHBoxLayout(self.groupBox_3)
        self.horizontalLayout_7.setContentsMargins(0, 10, 0, 0)
        self.horizontalLayout_7.setObjectName(_fromUtf8("horizontalLayout_7"))
        self.tSeries = QtGui.QLineEdit(self.groupBox_3)
        self.tSeries.setPlaceholderText(_fromUtf8(""))
        self.tSeries.setObjectName(_fromUtf8("tSeries"))
        self.horizontalLayout_7.addWidget(self.tSeries)
        self.horizontalLayout.addWidget(self.groupBox_3)
        self.groupBox_2 = QtGui.QGroupBox(self.tab)
        self.groupBox_2.setFlat(True)
        self.groupBox_2.setObjectName(_fromUtf8("groupBox_2"))
        self.horizontalLayout_6 = QtGui.QHBoxLayout(self.groupBox_2)
        self.horizontalLayout_6.setContentsMargins(0, 10, 0, 0)
        self.horizontalLayout_6.setObjectName(_fromUtf8("horizontalLayout_6"))
        self.tSaveName = QtGui.QLineEdit(self.groupBox_2)
        self.tSaveName.setObjectName(_fromUtf8("tSaveName"))
        self.horizontalLayout_6.addWidget(self.tSaveName)
        self.horizontalLayout.addWidget(self.groupBox_2)
        self.bChooseDirectory = QtGui.QPushButton(self.tab)
        self.bChooseDirectory.setObjectName(_fromUtf8("bChooseDirectory"))
        self.horizontalLayout.addWidget(self.bChooseDirectory)
        self.groupBox = QtGui.QGroupBox(self.tab)
        self.groupBox.setFlat(True)
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.horizontalLayout_5 = QtGui.QHBoxLayout(self.groupBox)
        self.horizontalLayout_5.setContentsMargins(0, 10, 0, 0)
        self.horizontalLayout_5.setObjectName(_fromUtf8("horizontalLayout_5"))
        self.tSidebandNumber = QtGui.QLineEdit(self.groupBox)
        self.tSidebandNumber.setObjectName(_fromUtf8("tSidebandNumber"))
        self.horizontalLayout_5.addWidget(self.tSidebandNumber)
        self.horizontalLayout.addWidget(self.groupBox)
        self.horizontalLayout_3.addLayout(self.horizontalLayout)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem)
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.bAbort = QtGui.QPushButton(self.tab)
        self.bAbort.setObjectName(_fromUtf8("bAbort"))
        self.gridLayout.addWidget(self.bAbort, 1, 2, 1, 1)
        self.bQuickStart = QtGui.QPushButton(self.tab)
        self.bQuickStart.setObjectName(_fromUtf8("bQuickStart"))
        self.gridLayout.addWidget(self.bQuickStart, 0, 2, 1, 1)
        self.bSaveWaveforms = QtGui.QPushButton(self.tab)
        self.bSaveWaveforms.setObjectName(_fromUtf8("bSaveWaveforms"))
        self.gridLayout.addWidget(self.bSaveWaveforms, 1, 0, 1, 1)
        self.bPause = QtGui.QPushButton(self.tab)
        self.bPause.setCheckable(True)
        self.bPause.setObjectName(_fromUtf8("bPause"))
        self.gridLayout.addWidget(self.bPause, 0, 0, 1, 1)
        self.bStart = QtGui.QPushButton(self.tab)
        self.bStart.setObjectName(_fromUtf8("bStart"))
        self.gridLayout.addWidget(self.bStart, 0, 1, 1, 1)
        self.horizontalLayout_3.addLayout(self.gridLayout)
        self.verticalLayout_2.addLayout(self.horizontalLayout_3)
        self.tabWidget.addTab(self.tab, _fromUtf8(""))
        self.tab_2 = QtGui.QWidget()
        self.tab_2.setObjectName(_fromUtf8("tab_2"))
        self.verticalLayout_3 = QtGui.QVBoxLayout(self.tab_2)
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.gScan = PlotWidget(self.tab_2)
        self.gScan.setObjectName(_fromUtf8("gScan"))
        self.verticalLayout_3.addWidget(self.gScan)
        self.horizontalLayout_4 = QtGui.QHBoxLayout()
        self.horizontalLayout_4.setObjectName(_fromUtf8("horizontalLayout_4"))
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem1)
        self.bClearScan = QtGui.QPushButton(self.tab_2)
        self.bClearScan.setObjectName(_fromUtf8("bClearScan"))
        self.horizontalLayout_4.addWidget(self.bClearScan)
        self.verticalLayout_3.addLayout(self.horizontalLayout_4)
        self.tabWidget.addTab(self.tab_2, _fromUtf8(""))
        self.verticalLayout.addWidget(self.tabWidget)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 823, 21))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.menuFile = QtGui.QMenu(self.menubar)
        self.menuFile.setObjectName(_fromUtf8("menuFile"))
        self.menuSPEX = QtGui.QMenu(self.menubar)
        self.menuSPEX.setObjectName(_fromUtf8("menuSPEX"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)
        self.mFileSettings = QtGui.QAction(MainWindow)
        self.mFileSettings.setObjectName(_fromUtf8("mFileSettings"))
        self.mFileExit = QtGui.QAction(MainWindow)
        self.mFileExit.setObjectName(_fromUtf8("mFileExit"))
        self.actionInitialize = QtGui.QAction(MainWindow)
        self.actionInitialize.setObjectName(_fromUtf8("actionInitialize"))
        self.actionGoto_Wavenumber = QtGui.QAction(MainWindow)
        self.actionGoto_Wavenumber.setObjectName(_fromUtf8("actionGoto_Wavenumber"))
        self.mSpexOpen = QtGui.QAction(MainWindow)
        self.mSpexOpen.setObjectName(_fromUtf8("mSpexOpen"))
        self.menuFile.addAction(self.mFileSettings)
        self.menuFile.addAction(self.mFileExit)
        self.menuSPEX.addAction(self.mSpexOpen)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuSPEX.menuAction())

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        MainWindow.setTabOrder(self.tPyBgSt, self.tPyBgEn)
        MainWindow.setTabOrder(self.tPyBgEn, self.tPyFpSt)
        MainWindow.setTabOrder(self.tPyFpSt, self.tPyFpEn)
        MainWindow.setTabOrder(self.tPyFpEn, self.tPyCdSt)
        MainWindow.setTabOrder(self.tPyCdSt, self.tPyCdEn)
        MainWindow.setTabOrder(self.tPyCdEn, self.tPmBgSt)
        MainWindow.setTabOrder(self.tPmBgSt, self.tPmBgEn)
        MainWindow.setTabOrder(self.tPmBgEn, self.tPmSgSt)
        MainWindow.setTabOrder(self.tPmSgSt, self.tPmSgEn)
        MainWindow.setTabOrder(self.tPmSgEn, self.bChooseDirectory)
        MainWindow.setTabOrder(self.bChooseDirectory, self.bPause)
        MainWindow.setTabOrder(self.bPause, self.bQuickStart)
        MainWindow.setTabOrder(self.bQuickStart, self.bSaveWaveforms)
        MainWindow.setTabOrder(self.bSaveWaveforms, self.bAbort)
        MainWindow.setTabOrder(self.bAbort, self.gPyro)
        MainWindow.setTabOrder(self.gPyro, self.gSignal)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "Sideband Measurements", None))
        self.tPmBgEn.setText(_translate("MainWindow", "0", None))
        self.tPmSgEn.setText(_translate("MainWindow", "0", None))
        self.tPyFpEn.setText(_translate("MainWindow", "0", None))
        self.label_11.setText(_translate("MainWindow", "PMT Sig En", None))
        self.tPyCdEn.setText(_translate("MainWindow", "0", None))
        self.tPmBgSt.setText(_translate("MainWindow", "0", None))
        self.tPyFpSt.setText(_translate("MainWindow", "0", None))
        self.tPyBgSt.setText(_translate("MainWindow", "0", None))
        self.label_9.setText(_translate("MainWindow", "Pyro CD End", None))
        self.label_10.setText(_translate("MainWindow", "PMT BG End", None))
        self.label_7.setText(_translate("MainWindow", "Pyro BG End", None))
        self.label_6.setText(_translate("MainWindow", "PMT Sig Start", None))
        self.label_3.setText(_translate("MainWindow", "Pyro FP Start", None))
        self.label_8.setText(_translate("MainWindow", "Pyro FP End", None))
        self.label_4.setText(_translate("MainWindow", "Pyro CD Start", None))
        self.label_5.setText(_translate("MainWindow", "PMT BG Start", None))
        self.tPyBgEn.setText(_translate("MainWindow", "0", None))
        self.tPyCdSt.setText(_translate("MainWindow", "0", None))
        self.tPmSgSt.setText(_translate("MainWindow", "0", None))
        self.label_2.setText(_translate("MainWindow", "Pyro BG Start", None))
        self.bInitPyro.setText(_translate("MainWindow", "Init Pyro", None))
        self.bInitPMT.setText(_translate("MainWindow", "Init PMT", None))
        self.groupBox_3.setTitle(_translate("MainWindow", "Series", None))
        self.tSeries.setToolTip(_translate("MainWindow", "{NIRP, NIRL, FELP, FELL, TEMP, PMHV}", None))
        self.groupBox_2.setTitle(_translate("MainWindow", "Save Name", None))
        self.bChooseDirectory.setText(_translate("MainWindow", "Choose Directory", None))
        self.groupBox.setTitle(_translate("MainWindow", "Sideband Number", None))
        self.bAbort.setText(_translate("MainWindow", "Abort", None))
        self.bQuickStart.setText(_translate("MainWindow", "Quick Start", None))
        self.bSaveWaveforms.setText(_translate("MainWindow", "Save Waveforms", None))
        self.bPause.setText(_translate("MainWindow", "Pause", None))
        self.bStart.setText(_translate("MainWindow", "Start", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("MainWindow", "Experimental Settings", None))
        self.bClearScan.setText(_translate("MainWindow", "Clear", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("MainWindow", "Scan", None))
        self.menuFile.setTitle(_translate("MainWindow", "File", None))
        self.menuSPEX.setTitle(_translate("MainWindow", "SPEX", None))
        self.mFileSettings.setText(_translate("MainWindow", "Settings", None))
        self.mFileExit.setText(_translate("MainWindow", "Exit", None))
        self.actionInitialize.setText(_translate("MainWindow", "Initialize...", None))
        self.actionGoto_Wavenumber.setText(_translate("MainWindow", "Goto Wavenumber...", None))
        self.mSpexOpen.setText(_translate("MainWindow", "Open SPEX Settings", None))

from pyqtgraph import PlotWidget
from InstsAndQt.customQt import QFNumberEdit
