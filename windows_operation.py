from PyQt5 import QtWidgets, QtCore, QtGui
from gui.mainWindow import Ui_MainWindow
import icon_rc
from service import Speech2TextService, EmotionAnalyzeService


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)
        self.label1.setText(chr(0xf282))
        QtGui.QFontDatabase.addApplicationFont(":font/awesome")
        self.label1.setFont(QtGui.QFont('FontAwesome', 34))
        png = QtGui.QMovie(':img/speaking')
        self.label.setMovie(png)
        png.start()

        # self.speech = EmotionAnalyzeService()
        # self.speech.trigger.connect(self.putout_data)
        # self.speech.start()

    def putout_data(self):
        print("lalal")


