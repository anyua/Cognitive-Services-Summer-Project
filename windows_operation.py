from PyQt5 import QtWidgets, QtCore, QtGui
from gui.mainWindow import Ui_MainWindow
import icon_rc
from service import Speech2TextService, EmotionAnalyzeService, LanguageUnderstandingService, BingWebSearchService


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)
        # 线程池
        self.thread_list = []
        # 设置表情获取计时器
        self.emotion_count = -1
        self.emotion_api_timer = QtCore.QTimer(self)
        self.emotion_api_timer.timeout.connect(self.get_emotion_once)
        # 向字体库中添加字体
        QtGui.QFontDatabase.addApplicationFont(":font/awesome")
        # 设置字体
        self.lightLabel.setFont(QtGui.QFont('FontAwesome', 34))
        self.lightLabel.setText(chr(0xf282))
        self.doorLable.setFont(QtGui.QFont('FontAwesome', 34))
        self.doorLable.setText(chr(0xf0eb))
        self.airConditionerLable.setFont(QtGui.QFont('FontAwesome', 34))
        self.airConditionerLable.setText(chr(0xf0eb))

        # 添加动图
        self.movie = None
        self.listening_gif = QtGui.QMovie(':img/speaking')
        self.waiting_gif = QtGui.QMovie(':img/speaking')
        self.thinking_gif = QtGui.QMovie(':img/speaking')
        self.happy_gif = QtGui.QMovie(':img/speaking')
        self.sad_gif = QtGui.QMovie(':img/speaking')

        # 绑定按钮
        self.cortana.clicked.connect(self.new_voice)

    def new_voice(self):
        speech = Speech2TextService()
        speech.trigger.connect(self.analyze_text)
        # speech.trigger.connect(self.analyze_cmd)
        speech.listening_complete.connect(self.cortana_is_thinking)
        speech.start()
        self.thread_list.append(speech)
        self.cortana_is_listening()

    def analyze_text(self, text):
        if text.strip() == "":
            print("语音转文字结果为空，不进行进一步分析")
            self.get_emotion()  # debug
            pass
        else:
            self.textEdit.setText(text)
            understanding = LanguageUnderstandingService(text)
            understanding.trigger.connect(self.analyze_cmd)
            understanding.start()
            self.thread_list.append(understanding)

    def analyze_cmd(self, cmd):
        if 'error' in cmd:
            search = BingWebSearchService(cmd['error'])
            search.trigger.connect(self.show_web_result)
            search.start()
            self.thread_list.append(search)
            # 进行搜索
            pass
        else:
            # 去处理图标
            pass
        self.get_emotion()

    def get_bing_web_search(self, text):
        web_result = BingWebSearchService(text)
        web_result.trigger.connect(self.show_web_result)
        web_result.start()
        self.thread_list.append(web_result)

    def show_web_result(self, web_list):
        self.webBrowser.setText(str(web_list[0]))

    def get_emotion(self):
        self.emotion_count = 20
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

    def cortana_is_waiting(self):
        pass

    def cortana_is_listening(self):
        if self.movie:
            self.movie.stop()
        self.set_cortane_move(self.listening_gif)

    def cortana_is_thinking(self):
        if self.movie:
            self.movie.stop()

    def happy_cortane(self):
        pass

    def sad_cortane(self):
        pass

    def set_cortane_move(self, gif):
        gif.frameChanged.connect(self.set_cortane_icon)
        # if gif.loopCount() != -1:
        #     gif.finished.connect(gif.start)
        self.movie = gif
        self.movie.start()

    def set_cortane_icon(self):
        self.cortana.setIcon(QtGui.QIcon(self.movie.currentPixmap()))


    @staticmethod
    def printout_data(data):
        print(data)



