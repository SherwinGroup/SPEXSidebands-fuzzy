# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Z:\Darren\Python\SPEXSidebands\MainWindow.ui'
#
# Created: Tue Feb 03 12:59:22 2015
#      by: PyQt4 UI code generator 4.9.6
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
        MainWindow.resize(724, 490)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.gPyro = PlotWidget(self.centralwidget)
        self.gPyro.setObjectName(_fromUtf8("gPyro"))
        self.horizontalLayout_2.addWidget(self.gPyro)
        self.gSignal = PlotWidget(self.centralwidget)
        self.gSignal.setObjectName(_fromUtf8("gSignal"))
        self.horizontalLayout_2.addWidget(self.gSignal)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.label = QtGui.QLabel(self.centralwidget)
        self.label.setObjectName(_fromUtf8("label"))
        self.horizontalLayout.addWidget(self.label)
        self.tSaveName = QtGui.QLineEdit(self.centralwidget)
        self.tSaveName.setObjectName(_fromUtf8("tSaveName"))
        self.horizontalLayout.addWidget(self.tSaveName)
        self.bChooseDirectory = QtGui.QPushButton(self.centralwidget)
        self.bChooseDirectory.setObjectName(_fromUtf8("bChooseDirectory"))
        self.horizontalLayout.addWidget(self.bChooseDirectory)
        self.horizontalLayout_3.addLayout(self.horizontalLayout)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem)
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.bStart = QtGui.QPushButton(self.centralwidget)
        self.bStart.setObjectName(_fromUtf8("bStart"))
        self.gridLayout.addWidget(self.bStart, 0, 1, 1, 1)
        self.bAbort = QtGui.QPushButton(self.centralwidget)
        self.bAbort.setObjectName(_fromUtf8("bAbort"))
        self.gridLayout.addWidget(self.bAbort, 1, 1, 1, 1)
        self.bPause = QtGui.QPushButton(self.centralwidget)
        self.bPause.setCheckable(True)
        self.bPause.setObjectName(_fromUtf8("bPause"))
        self.gridLayout.addWidget(self.bPause, 0, 0, 1, 1)
        self.horizontalLayout_3.addLayout(self.gridLayout)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 724, 21))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.menuFile = QtGui.QMenu(self.menubar)
        self.menuFile.setObjectName(_fromUtf8("menuFile"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)
        self.actionSettings = QtGui.QAction(MainWindow)
        self.actionSettings.setObjectName(_fromUtf8("actionSettings"))
        self.actionExit = QtGui.QAction(MainWindow)
        self.actionExit.setObjectName(_fromUtf8("actionExit"))
        self.menuFile.addAction(self.actionSettings)
        self.menuFile.addAction(self.actionExit)
        self.menubar.addAction(self.menuFile.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "Sideband Measurements", None))
        self.label.setText(_translate("MainWindow", "Save File Name", None))
        self.bChooseDirectory.setText(_translate("MainWindow", "Choose Directory", None))
        self.bStart.setText(_translate("MainWindow", "Start", None))
        self.bAbort.setText(_translate("MainWindow", "Abort", None))
        self.bPause.setText(_translate("MainWindow", "Pause", None))
        self.menuFile.setTitle(_translate("MainWindow", "File", None))
        self.actionSettings.setText(_translate("MainWindow", "Settings", None))
        self.actionExit.setText(_translate("MainWindow", "Exit", None))

from pyqtgraph import PlotWidget
