# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'SPEXWindow.ui'
#
# Created: Sun May 22 09:20:53 2016
#      by: PyQt4 UI code generator 4.11.3
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

class Ui_SPEXController(object):
    def setupUi(self, SPEXController):
        SPEXController.setObjectName(_fromUtf8("SPEXController"))
        SPEXController.resize(394, 164)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/test/SPEXIcon.jpg")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        SPEXController.setWindowIcon(icon)
        self.centralwidget = QtGui.QWidget(SPEXController)
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
        self.sbGoto = SpinBox(self.centralwidget)
        self.sbGoto.setObjectName(_fromUtf8("sbGoto"))
        self.horizontalLayout.addWidget(self.sbGoto)
        self.bGo = QtGui.QPushButton(self.centralwidget)
        self.bGo.setObjectName(_fromUtf8("bGo"))
        self.horizontalLayout.addWidget(self.bGo)
        self.lSBO = QtGui.QLabel(self.centralwidget)
        self.lSBO.setObjectName(_fromUtf8("lSBO"))
        self.horizontalLayout.addWidget(self.lSBO)
        self.sbSB = QtGui.QSpinBox(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sbSB.sizePolicy().hasHeightForWidth())
        self.sbSB.setSizePolicy(sizePolicy)
        self.sbSB.setMinimum(-100)
        self.sbSB.setMaximum(100)
        self.sbSB.setObjectName(_fromUtf8("sbSB"))
        self.horizontalLayout.addWidget(self.sbSB)
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
        SPEXController.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(SPEXController)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 394, 22))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.menuFile = QtGui.QMenu(self.menubar)
        self.menuFile.setObjectName(_fromUtf8("menuFile"))
        SPEXController.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(SPEXController)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        SPEXController.setStatusBar(self.statusbar)
        self.actionInitiate_SPEX = QtGui.QAction(SPEXController)
        self.actionInitiate_SPEX.setObjectName(_fromUtf8("actionInitiate_SPEX"))
        self.menuFile.addAction(self.actionInitiate_SPEX)
        self.menubar.addAction(self.menuFile.menuAction())

        self.retranslateUi(SPEXController)
        QtCore.QMetaObject.connectSlotsByName(SPEXController)

    def retranslateUi(self, SPEXController):
        SPEXController.setWindowTitle(_translate("SPEXController", "SPEX Control Window", None))
        self.label.setText(_translate("SPEXController", "Goto Wavenumber:", None))
        self.bGo.setText(_translate("SPEXController", "Go", None))
        self.lSBO.setText(_translate("SPEXController", "SB Order", None))
        self.label_2.setText(_translate("SPEXController", "SPEX GPIB:", None))
        self.bDone.setText(_translate("SPEXController", "OK", None))
        self.menuFile.setTitle(_translate("SPEXController", "File", None))
        self.actionInitiate_SPEX.setText(_translate("SPEXController", "Initiate SPEX...", None))

from pyqtgraph import SpinBox
import resources_rc
