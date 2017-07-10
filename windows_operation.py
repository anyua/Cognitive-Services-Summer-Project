from PyQt5 import QtWidgets, QtCore, QtGui
from gui.mainWindow import Ui_MainWindow
import icon_rc


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)
        self.label1.setText(chr(0xf282))
        QtGui.QFontDatabase.addApplicationFont("gui/resources/fontawesome-webfont.ttf")
        self.label1.setFont(QtGui.QFont('FontAwesome', 34))
        png = QtGui.QMovie(':img/speaking')
        # 在l1里面，调用setPixmap命令，建立一个图像存放框，并将之前的图像png存放在这个框框里。
        self.label.setMovie(png)
        png.start()
