# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Z:\Darren\Python\SPEXSidebands\SPEXWindow.ui'
#
# Created: Wed Feb 04 13:11:09 2015
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
        MainWindow.resize(300, 127)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.label = QtGui.QLabel(self.centralwidget)
        self.label.setObjectName(_fromUtf8("label"))
        self.horizontalLayout.addWidget(self.label)
        self.tGotoWN = QFNumberEdit(self.centralwidget)
        self.tGotoWN.setObjectName(_fromUtf8("tGotoWN"))
        self.horizontalLayout.addWidget(self.tGotoWN)
        self.bGo = QtGui.QPushButton(self.centralwidget)
        self.bGo.setObjectName(_fromUtf8("bGo"))
        self.horizontalLayout.addWidget(self.bGo)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.label_2 = QtGui.QLabel(self.centralwidget)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.horizontalLayout_2.addWidget(self.label_2)
        self.cGPIB = QtGui.QComboBox(self.centralwidget)
        self.cGPIB.setObjectName(_fromUtf8("cGPIB"))
        self.horizontalLayout_2.addWidget(self.cGPIB)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.bDone = QtGui.QPushButton(self.centralwidget)
        self.bDone.setObjectName(_fromUtf8("bDone"))
        self.horizontalLayout_2.addWidget(self.bDone)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        spacerItem2 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem2)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 300, 21))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.menuFile = QtGui.QMenu(self.menubar)
        self.menuFile.setObjectName(_fromUtf8("menuFile"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)
        self.actionInitiate_SPEX = QtGui.QAction(MainWindow)
        self.actionInitiate_SPEX.setObjectName(_fromUtf8("actionInitiate_SPEX"))
        self.menuFile.addAction(self.actionInitiate_SPEX)
        self.menubar.addAction(self.menuFile.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))
        self.label.setText(_translate("MainWindow", "Goto Wavenumber:", None))
        self.bGo.setText(_translate("MainWindow", "Go", None))
        self.label_2.setText(_translate("MainWindow", "SPEX GPIB:", None))
        self.bDone.setText(_translate("MainWindow", "OK", None))
        self.menuFile.setTitle(_translate("MainWindow", "File", None))
        self.actionInitiate_SPEX.setText(_translate("MainWindow", "Initiate SPEX...", None))

from customQt import QFNumberEdit
