# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'SPEXWindow.ui'
#
# Created: Sun May 22 09:20:53 2016
#      by: PyQt4 UI code generator 4.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

try:
    _encoding = QtWidgets.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtCore.QCoreApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtCore.QCoreApplication.translate(context, text, disambig)

class Ui_SPEXController(object):
    def setupUi(self, SPEXController):
        SPEXController.setObjectName("SPEXController")
        SPEXController.resize(301, 115)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/test/SPEXIcon.jpg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        SPEXController.setWindowIcon(icon)
        self.centralwidget = QtWidgets.QWidget(SPEXController)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.sbGoto = SpinBox(self.centralwidget)
        self.sbGoto.setObjectName("sbGoto")
        self.horizontalLayout.addWidget(self.sbGoto)
        self.bGo = QtWidgets.QPushButton(self.centralwidget)
        self.bGo.setObjectName("bGo")
        self.horizontalLayout.addWidget(self.bGo)
        self.lSBO = QtWidgets.QLabel(self.centralwidget)
        self.lSBO.setObjectName("lSBO")
        self.horizontalLayout.addWidget(self.lSBO)
        self.sbSB = QtWidgets.QSpinBox(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sbSB.sizePolicy().hasHeightForWidth())
        self.sbSB.setSizePolicy(sizePolicy)
        self.sbSB.setMinimum(-100)
        self.sbSB.setMaximum(100)
        self.sbSB.setObjectName("sbSB")
        self.horizontalLayout.addWidget(self.sbSB)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_2.addWidget(self.label_2)
        self.cGPIB = QtWidgets.QComboBox(self.centralwidget)
        self.cGPIB.setObjectName("cGPIB")
        self.horizontalLayout_2.addWidget(self.cGPIB)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.bDone = QtWidgets.QPushButton(self.centralwidget)
        self.bDone.setObjectName("bDone")
        self.horizontalLayout_2.addWidget(self.bDone)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        SPEXController.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(SPEXController)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 394, 22))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        SPEXController.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(SPEXController)
        self.statusbar.setObjectName("statusbar")
        SPEXController.setStatusBar(self.statusbar)
        self.actionInitiate_SPEX = QtWidgets.QAction(SPEXController)
        self.actionInitiate_SPEX.setObjectName("actionInitiate_SPEX")
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

from . import resources_rc

