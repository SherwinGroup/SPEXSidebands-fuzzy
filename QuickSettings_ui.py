# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'QuickSettings.ui'
#
# Created: Fri Aug 28 14:01:38 2015
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

class Ui_QuickSettings(object):
    def setupUi(self, QuickSettings):
        QuickSettings.setObjectName(_fromUtf8("QuickSettings"))
        QuickSettings.resize(464, 156)
        self.verticalLayout_2 = QtGui.QVBoxLayout(QuickSettings)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.label_3 = QtGui.QLabel(QuickSettings)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.horizontalLayout_3.addWidget(self.label_3)
        self.tStartWN = QFNumberEdit(QuickSettings)
        self.tStartWN.setObjectName(_fromUtf8("tStartWN"))
        self.horizontalLayout_3.addWidget(self.tStartWN)
        self.label_4 = QtGui.QLabel(QuickSettings)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.horizontalLayout_3.addWidget(self.label_4)
        self.tStepWN = QFNumberEdit(QuickSettings)
        self.tStepWN.setObjectName(_fromUtf8("tStepWN"))
        self.horizontalLayout_3.addWidget(self.tStepWN)
        self.label_5 = QtGui.QLabel(QuickSettings)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.horizontalLayout_3.addWidget(self.label_5)
        self.tEndWN = QFNumberEdit(QuickSettings)
        self.tEndWN.setObjectName(_fromUtf8("tEndWN"))
        self.horizontalLayout_3.addWidget(self.tEndWN)
        self.label_10 = QtGui.QLabel(QuickSettings)
        self.label_10.setObjectName(_fromUtf8("label_10"))
        self.horizontalLayout_3.addWidget(self.label_10)
        self.tAverages = QINumberEdit(QuickSettings)
        self.tAverages.setObjectName(_fromUtf8("tAverages"))
        self.horizontalLayout_3.addWidget(self.tAverages)
        self.verticalLayout_2.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_11 = QtGui.QHBoxLayout()
        self.horizontalLayout_11.setObjectName(_fromUtf8("horizontalLayout_11"))
        self.label_18 = QtGui.QLabel(QuickSettings)
        self.label_18.setObjectName(_fromUtf8("label_18"))
        self.horizontalLayout_11.addWidget(self.label_18)
        self.tGotoSB = QFNumberEdit(QuickSettings)
        self.tGotoSB.setObjectName(_fromUtf8("tGotoSB"))
        self.horizontalLayout_11.addWidget(self.tGotoSB)
        self.label_19 = QtGui.QLabel(QuickSettings)
        self.label_19.setObjectName(_fromUtf8("label_19"))
        self.horizontalLayout_11.addWidget(self.label_19)
        self.tGotoBound = QFNumberEdit(QuickSettings)
        self.tGotoBound.setObjectName(_fromUtf8("tGotoBound"))
        self.horizontalLayout_11.addWidget(self.tGotoBound)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_11.addItem(spacerItem)
        self.verticalLayout_2.addLayout(self.horizontalLayout_11)
        self.horizontalLayout_7 = QtGui.QHBoxLayout()
        self.horizontalLayout_7.setObjectName(_fromUtf8("horizontalLayout_7"))
        self.label_13 = QtGui.QLabel(QuickSettings)
        self.label_13.setObjectName(_fromUtf8("label_13"))
        self.horizontalLayout_7.addWidget(self.label_13)
        self.cbPMHV = QtGui.QComboBox(QuickSettings)
        self.cbPMHV.setObjectName(_fromUtf8("cbPMHV"))
        self.cbPMHV.addItem(_fromUtf8(""))
        self.cbPMHV.addItem(_fromUtf8(""))
        self.horizontalLayout_7.addWidget(self.cbPMHV)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_7.addItem(spacerItem1)
        self.label_17 = QtGui.QLabel(QuickSettings)
        self.label_17.setObjectName(_fromUtf8("label_17"))
        self.horizontalLayout_7.addWidget(self.label_17)
        self.cbNDFilters = QtGui.QComboBox(QuickSettings)
        self.cbNDFilters.setObjectName(_fromUtf8("cbNDFilters"))
        self.cbNDFilters.addItem(_fromUtf8(""))
        self.cbNDFilters.addItem(_fromUtf8(""))
        self.cbNDFilters.addItem(_fromUtf8(""))
        self.cbNDFilters.addItem(_fromUtf8(""))
        self.horizontalLayout_7.addWidget(self.cbNDFilters)
        self.verticalLayout_2.addLayout(self.horizontalLayout_7)
        self.buttonBox = QtGui.QDialogButtonBox(QuickSettings)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.verticalLayout_2.addWidget(self.buttonBox)

        self.retranslateUi(QuickSettings)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), QuickSettings.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), QuickSettings.reject)
        QtCore.QMetaObject.connectSlotsByName(QuickSettings)
        QuickSettings.setTabOrder(self.tStartWN, self.tStepWN)
        QuickSettings.setTabOrder(self.tStepWN, self.tEndWN)
        QuickSettings.setTabOrder(self.tEndWN, self.tAverages)
        QuickSettings.setTabOrder(self.tAverages, self.tGotoSB)
        QuickSettings.setTabOrder(self.tGotoSB, self.tGotoBound)
        QuickSettings.setTabOrder(self.tGotoBound, self.cbPMHV)
        QuickSettings.setTabOrder(self.cbPMHV, self.cbNDFilters)
        QuickSettings.setTabOrder(self.cbNDFilters, self.buttonBox)

    def retranslateUi(self, QuickSettings):
        QuickSettings.setWindowTitle(_translate("QuickSettings", "Scan Settings", None))
        self.label_3.setText(_translate("QuickSettings", "Starting WN", None))
        self.label_4.setText(_translate("QuickSettings", "Step", None))
        self.label_5.setText(_translate("QuickSettings", "Ending WN", None))
        self.label_10.setText(_translate("QuickSettings", "Average", None))
        self.label_18.setText(_translate("QuickSettings", "Go to SB #:", None))
        self.label_19.setText(_translate("QuickSettings", "+/-", None))
        self.label_13.setText(_translate("QuickSettings", "PM HV", None))
        self.cbPMHV.setItemText(0, _translate("QuickSettings", "700", None))
        self.cbPMHV.setItemText(1, _translate("QuickSettings", "1000", None))
        self.label_17.setText(_translate("QuickSettings", "ND Filters", None))
        self.cbNDFilters.setItemText(0, _translate("QuickSettings", "None", None))
        self.cbNDFilters.setItemText(1, _translate("QuickSettings", "White Label", None))
        self.cbNDFilters.setItemText(2, _translate("QuickSettings", "Blue Label", None))
        self.cbNDFilters.setItemText(3, _translate("QuickSettings", "Both", None))

from InstsAndQt.customQt import QINumberEdit, QFNumberEdit
