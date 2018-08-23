# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\dvalovcin\Documents\GitHub\SPEXSidebands-fuzzy\UIs\QuickSettings.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
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

class Ui_QuickSettings(object):
    def setupUi(self, QuickSettings):
        QuickSettings.setObjectName("QuickSettings")
        QuickSettings.resize(451, 125)
        self.verticalLayout = QtWidgets.QVBoxLayout(QuickSettings)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.lStartWN = QtWidgets.QLabel(QuickSettings)
        self.lStartWN.setObjectName("lStartWN")
        self.horizontalLayout_3.addWidget(self.lStartWN)
        self.tStartWN = QFNumberEdit(QuickSettings)
        self.tStartWN.setObjectName("tStartWN")
        self.horizontalLayout_3.addWidget(self.tStartWN)
        self.lStepWN = QtWidgets.QLabel(QuickSettings)
        self.lStepWN.setObjectName("lStepWN")
        self.horizontalLayout_3.addWidget(self.lStepWN)
        self.tStepWN = QFNumberEdit(QuickSettings)
        self.tStepWN.setObjectName("tStepWN")
        self.horizontalLayout_3.addWidget(self.tStepWN)
        self.lEndWN = QtWidgets.QLabel(QuickSettings)
        self.lEndWN.setObjectName("lEndWN")
        self.horizontalLayout_3.addWidget(self.lEndWN)
        self.tEndWN = QFNumberEdit(QuickSettings)
        self.tEndWN.setObjectName("tEndWN")
        self.horizontalLayout_3.addWidget(self.tEndWN)
        self.label_10 = QtWidgets.QLabel(QuickSettings)
        self.label_10.setObjectName("label_10")
        self.horizontalLayout_3.addWidget(self.label_10)
        self.tAverages = QINumberEdit(QuickSettings)
        self.tAverages.setObjectName("tAverages")
        self.horizontalLayout_3.addWidget(self.tAverages)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_11 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_11.setObjectName("horizontalLayout_11")
        self.label_18 = QtWidgets.QLabel(QuickSettings)
        self.label_18.setObjectName("label_18")
        self.horizontalLayout_11.addWidget(self.label_18)
        self.tGotoSB = QFNumberEdit(QuickSettings)
        self.tGotoSB.setObjectName("tGotoSB")
        self.horizontalLayout_11.addWidget(self.tGotoSB)
        self.label_19 = QtWidgets.QLabel(QuickSettings)
        self.label_19.setObjectName("label_19")
        self.horizontalLayout_11.addWidget(self.label_19)
        self.tGotoBound = QFNumberEdit(QuickSettings)
        self.tGotoBound.setObjectName("tGotoBound")
        self.horizontalLayout_11.addWidget(self.tGotoBound)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_11.addItem(spacerItem)
        self.verticalLayout.addLayout(self.horizontalLayout_11)
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.label_13 = QtWidgets.QLabel(QuickSettings)
        self.label_13.setObjectName("label_13")
        self.horizontalLayout_7.addWidget(self.label_13)
        self.cbPMHV = QtWidgets.QComboBox(QuickSettings)
        self.cbPMHV.setObjectName("cbPMHV")
        self.cbPMHV.addItem("")
        self.cbPMHV.addItem("")
        self.horizontalLayout_7.addWidget(self.cbPMHV)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_7.addItem(spacerItem1)
        self.cbFilterWhite = QtWidgets.QCheckBox(QuickSettings)
        self.cbFilterWhite.setObjectName("cbFilterWhite")
        self.horizontalLayout_7.addWidget(self.cbFilterWhite)
        self.cbFilterBlue = QtWidgets.QCheckBox(QuickSettings)
        self.cbFilterBlue.setObjectName("cbFilterBlue")
        self.horizontalLayout_7.addWidget(self.cbFilterBlue)
        self.cbFilterTriplet = QtWidgets.QCheckBox(QuickSettings)
        self.cbFilterTriplet.setObjectName("cbFilterTriplet")
        self.horizontalLayout_7.addWidget(self.cbFilterTriplet)
        self.verticalLayout.addLayout(self.horizontalLayout_7)
        self.buttonBox = QtWidgets.QDialogButtonBox(QuickSettings)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(QuickSettings)
        self.buttonBox.accepted.connect(QuickSettings.accept)
        self.buttonBox.rejected.connect(QuickSettings.reject)
        QtCore.QMetaObject.connectSlotsByName(QuickSettings)
        QuickSettings.setTabOrder(self.tStartWN, self.tStepWN)
        QuickSettings.setTabOrder(self.tStepWN, self.tEndWN)
        QuickSettings.setTabOrder(self.tEndWN, self.tAverages)
        QuickSettings.setTabOrder(self.tAverages, self.tGotoSB)
        QuickSettings.setTabOrder(self.tGotoSB, self.tGotoBound)
        QuickSettings.setTabOrder(self.tGotoBound, self.cbPMHV)
        QuickSettings.setTabOrder(self.cbPMHV, self.buttonBox)

    def retranslateUi(self, QuickSettings):
        QuickSettings.setWindowTitle(_translate("QuickSettings", "Scan Settings", None))
        self.lStartWN.setText(_translate("QuickSettings", "Starting WN", None))
        self.lStepWN.setText(_translate("QuickSettings", "Step", None))
        self.lEndWN.setText(_translate("QuickSettings", "Ending WN", None))
        self.label_10.setText(_translate("QuickSettings", "Average", None))
        self.label_18.setText(_translate("QuickSettings", "Go to SB #:", None))
        self.label_19.setText(_translate("QuickSettings", "+/-", None))
        self.label_13.setText(_translate("QuickSettings", "PM HV", None))
        self.cbPMHV.setItemText(0, _translate("QuickSettings", "700", None))
        self.cbPMHV.setItemText(1, _translate("QuickSettings", "1000", None))
        self.cbFilterWhite.setText(_translate("QuickSettings", "White", None))
        self.cbFilterBlue.setText(_translate("QuickSettings", "Blue", None))
        self.cbFilterTriplet.setText(_translate("QuickSettings", "Triplet", None))

from InstsAndQt.customQt import QFNumberEdit, QINumberEdit

