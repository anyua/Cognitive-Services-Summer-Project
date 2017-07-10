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
        MainWindow.resize(863, 649)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label1 = QtWidgets.QLabel(self.centralwidget)
        self.label1.setGeometry(QtCore.QRect(80, 50, 81, 111))
        self.label1.setStyleSheet("font: 20pt \"FontAwesome\";\n"
"color: rgb(118, 118, 118);")
        self.label1.setObjectName("label1")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(200, 40, 541, 491))
        self.label.setObjectName("label")
        self.getEmotion = QtWidgets.QPushButton(self.centralwidget)
        self.getEmotion.setGeometry(QtCore.QRect(34, 240, 111, 23))
        self.getEmotion.setObjectName("getEmotion")
        self.getAudio = QtWidgets.QPushButton(self.centralwidget)
        self.getAudio.setGeometry(QtCore.QRect(50, 310, 75, 23))
        self.getAudio.setObjectName("getAudio")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 863, 23))
        self.menubar.setObjectName("menubar")
        self.menu = QtWidgets.QMenu(self.menubar)
        self.menu.setObjectName("menu")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.menubar.addAction(self.menu.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label1.setText(_translate("MainWindow", "111"))
        self.label.setText(_translate("MainWindow", "TextLabel"))
        self.getEmotion.setText(_translate("MainWindow", "开始检查表情"))
        self.getAudio.setText(_translate("MainWindow", "开始录音"))
        self.menu.setTitle(_translate("MainWindow", "啦啦啦"))

import icon_rc
