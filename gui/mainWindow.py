# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainWindow.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(372, 586)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.toolBox = QtWidgets.QToolBox(self.centralwidget)
        self.toolBox.setObjectName("toolBox")
        self.page = QtWidgets.QWidget()
        self.page.setGeometry(QtCore.QRect(0, 0, 354, 490))
        self.page.setObjectName("page")
        self.cortana = QtWidgets.QPushButton(self.page)
        self.cortana.setGeometry(QtCore.QRect(100, 150, 141, 131))
        self.cortana.setObjectName("cortana")
        self.feedBackBrowser = QtWidgets.QTextBrowser(self.page)
        self.feedBackBrowser.setGeometry(QtCore.QRect(40, 380, 251, 61))
        self.feedBackBrowser.setObjectName("feedBackBrowser")
        self.layoutWidget = QtWidgets.QWidget(self.page)
        self.layoutWidget.setGeometry(QtCore.QRect(50, 10, 261, 36))
        self.layoutWidget.setObjectName("layoutWidget")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.layoutWidget)
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.airConditionerLable = QtWidgets.QLabel(self.layoutWidget)
        self.airConditionerLable.setObjectName("airConditionerLable")
        self.gridLayout_2.addWidget(self.airConditionerLable, 0, 2, 1, 1)
        self.doorLable = QtWidgets.QLabel(self.layoutWidget)
        self.doorLable.setObjectName("doorLable")
        self.gridLayout_2.addWidget(self.doorLable, 0, 1, 1, 1)
        self.lightRadioButton = QtWidgets.QRadioButton(self.layoutWidget)
        self.lightRadioButton.setText("")
        self.lightRadioButton.setObjectName("lightRadioButton")
        self.gridLayout_2.addWidget(self.lightRadioButton, 1, 0, 1, 1)
        self.airConditionerRadioButton = QtWidgets.QRadioButton(self.layoutWidget)
        self.airConditionerRadioButton.setText("")
        self.airConditionerRadioButton.setObjectName("airConditionerRadioButton")
        self.gridLayout_2.addWidget(self.airConditionerRadioButton, 1, 2, 1, 1)
        self.doorRadioButton = QtWidgets.QRadioButton(self.layoutWidget)
        self.doorRadioButton.setText("")
        self.doorRadioButton.setObjectName("doorRadioButton")
        self.gridLayout_2.addWidget(self.doorRadioButton, 1, 1, 1, 1)
        self.lightLabel = QtWidgets.QLabel(self.layoutWidget)
        self.lightLabel.setObjectName("lightLabel")
        self.gridLayout_2.addWidget(self.lightLabel, 0, 0, 1, 1)
        self.toolBox.addItem(self.page, "")
        self.page_2 = QtWidgets.QWidget()
        self.page_2.setGeometry(QtCore.QRect(0, 0, 354, 490))
        self.page_2.setObjectName("page_2")
        self.webBrowser = QtWidgets.QTextBrowser(self.page_2)
        self.webBrowser.setGeometry(QtCore.QRect(10, 10, 331, 331))
        self.webBrowser.setObjectName("webBrowser")
        self.pushButton_2 = QtWidgets.QPushButton(self.page_2)
        self.pushButton_2.setGeometry(QtCore.QRect(130, 380, 61, 61))
        self.pushButton_2.setObjectName("pushButton_2")
        self.toolBox.addItem(self.page_2, "")
        self.gridLayout.addWidget(self.toolBox, 0, 0, 1, 1)
        self.textEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.textEdit.setObjectName("textEdit")
        self.gridLayout.addWidget(self.textEdit, 1, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        self.toolBox.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.cortana.setText(_translate("MainWindow", "小娜的标志"))
        self.feedBackBrowser.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'SimSun\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>"))
        self.airConditionerLable.setText(_translate("MainWindow", "空调"))
        self.doorLable.setText(_translate("MainWindow", "门"))
        self.lightLabel.setText(_translate("MainWindow", "灯"))
        self.toolBox.setItemText(self.toolBox.indexOf(self.page), _translate("MainWindow", "Page 1"))
        self.pushButton_2.setText(_translate("MainWindow", "PushButton"))
        self.toolBox.setItemText(self.toolBox.indexOf(self.page_2), _translate("MainWindow", "Page 2"))

import icon_rc
