from PyQt5 import QtWidgets, QtCore, QtGui
from gui.mainWindow import Ui_MainWindow
import icon_rc
from service import Speech2TextService, EmotionAnalyzeService, LanguageUnderstandingService


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)
        self.thread_list = []
        self.emotion_count = -1
        self.emotion_api_timer = QtCore.QTimer(self)
        self.emotion_api_timer.timeout.connect(self.get_emotion_once)
        # 向字体库中添加字体
        QtGui.QFontDatabase.addApplicationFont(":font/awesome")
        # 设置字体
        self.label1.setFont(QtGui.QFont('FontAwesome', 34))
        self.label1.setText(chr(0xf282))
        self.lightLabel.setFont(QtGui.QFont('FontAwesome', 34))
        self.lightLabel.setText(chr(0xf0eb))

        # 添加动图
        png = QtGui.QMovie(':img/speaking')
        self.label.setMovie(png)
        png.start()
        png.setPaused(True)

        # 绑定按钮
        self.getEmotion.clicked.connect(self.get_emotion)
        self.getAudio.clicked.connect(self.get_audio)
        self.pushButton.clicked.connect(self.get_luis)

    def new_voice(self):
        self.label.movie().setPaused(False)
        speech = Speech2TextService()
        speech.trigger.connect(self.analyze_text)
        speech.stop_the_cat.connect(self.label.movie().setPaused)
        speech.start()
        self.thread_list.append(speech)

    def analyze_text(self, text):
        if text.strip() == "":
            pass
        else:
            self.textBrowser.append(text)
            understanding = LanguageUnderstandingService(text)
            understanding.trigger.connect(self.printout_data)
            understanding.start()
            self.thread_list.append(understanding)

    def analyze_cmd(self, cmd):
        if cmd == {}:
            pass
        else:
            # 去处理图标
            pass

    def get_emotion(self):
        self.emotion_count = 10
        self.emotion_api_timer.start(2000)

    def get_emotion_once(self):
        if self.emotion_count >= 0:
            self.emotion_count -= 1
            emotion = EmotionAnalyzeService()
            emotion.trigger.connect(self.printout_data)
            emotion.start()
            self.thread_list.append(emotion)
        else:
            self.emotion_api_timer.stop()


    def get_luis(self, text="请把帮忙把灯关掉"):
        print(text)
        lalala = LanguageUnderstandingService(text)
        lalala.trigger.connect(self.printout_data)
        lalala.start()
        self.thread_list.append(lalala)

    def get_audio(self):
        self.label.movie().setPaused(False)
        speech = Speech2TextService()
        speech.trigger.connect(self.get_luis)
        speech.stop_the_cat.connect(self.label.movie().setPaused)
        speech.start()
        self.thread_list.append(speech)

    @staticmethod
    def printout_data(data):
        print(data)


