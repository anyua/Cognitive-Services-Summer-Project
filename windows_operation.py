from PyQt5 import QtWidgets, QtCore, QtGui
from gui.mainWindow import Ui_MainWindow
import icon_rc
import time
from service import Speech2TextService, EmotionAnalyzeService, LanguageUnderstandingService, BingWebSearchService

OPEN_BUTTON = chr(0xf205)
CLOSE_BUTTON = chr(0xf204)
WHITE_QSS = "color: rgb(255, 255, 255);"
GREY_QSS = "color: rgb(74, 74, 74);"


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
        self.lightLabel.setFont(QtGui.QFont('FontAwesome', 26))
        self.lightLabel.setText(chr(0xf0eb))
        self.lightLabel.setStyleSheet("color: rgb(255, 255, 255);")
        self.doorLable.setFont(QtGui.QFont('FontAwesome', 25))
        self.doorLable.setText(chr(0xf13e))
        self.doorLable.setStyleSheet("color: rgb(74, 74, 74);")
        self.airConditionerLable.setFont(QtGui.QFont('FontAwesome', 24))
        self.airConditionerLable.setText(chr(0xf2dc))
        self.airConditionerLable.setStyleSheet("color: rgb(74, 74, 74);")

        self.lightRadioButton.setFont(QtGui.QFont('FontAwesome', 12))
        self.lightRadioButton.setText(OPEN_BUTTON)
        self.lightRadioButton.setStyleSheet("color: rgb(255, 255, 255);")
        self.doorRadioButton.setFont(QtGui.QFont('FontAwesome', 12))
        self.doorRadioButton.setText(CLOSE_BUTTON)
        self.doorRadioButton.setStyleSheet("color: rgb(74, 74, 74);")
        self.airConditionerRadioButton.setFont(QtGui.QFont('FontAwesome', 12))
        self.airConditionerRadioButton.setText(CLOSE_BUTTON)
        self.airConditionerRadioButton.setStyleSheet("color: rgb(74, 74, 74);")

        # 添加动图
        self.movie = None
        self.listening_gif = QtGui.QMovie(':img/listening')
        self.waiting_gif = QtGui.QMovie(':img/waiting')
        self.thinking_gif = QtGui.QMovie(':img/thinking')
        self.happy_gif = QtGui.QMovie(':img/happy')
        self.sad_gif = QtGui.QMovie(':img/sad')
        self.cortana_is_waiting()
        self.sad_flag = 0
        self.happy_flag = 0

        # 绑定按钮
        self.cortana.clicked.connect(self.new_voice)
        self.littleCortana.clicked.connect(self.new_voice)

        # 情感分析
        self.emotion_list = list()
        self.result_once = 0
        self.emotion_effective_flag = False
        # 样式
        self.textEdit.setDisabled(True)
        self.toolBox.setStyleSheet("QToolBox::tab{border-top-style:solid;border-top-color:grey;border-top-width:1px;}")
        self.feedBackBrowser.setStyleSheet("border:none")

    def new_voice(self):
        self.textEdit.setText(". . . . . .")
        self.emotion_effective_flag = False
        self.result_once = 0
        speech = Speech2TextService()
        speech.trigger.connect(self.analyze_text)
        speech.listening_complete.connect(self.cortana_is_thinking)
        speech.start()
        self.thread_list.append(speech)
        self.cortana_is_listening()

    def analyze_text(self, text):
        if text.strip() == "":
            print("语音转文字结果为空，不进行进一步分析,回到监听状态")
            self.textEdit.setText("没有识别到语音信号....")
            # self.get_emotion()  # debug
            self.cortana_is_waiting()
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
            self.toolBox.setCurrentIndex(1)
        else:
            # 去处理图标
            self.toolBox.setCurrentIndex(0)
            if '灯' in cmd:
                if cmd['灯'] == '开':
                    self.lightRadioButton.setText(OPEN_BUTTON)
                    self.lightRadioButton.setStyleSheet(WHITE_QSS)
                    self.lightLabel.setStyleSheet(WHITE_QSS)
                elif cmd['灯'] == '关':
                    self.lightRadioButton.setText(CLOSE_BUTTON)
                    self.lightRadioButton.setStyleSheet(GREY_QSS)
                    self.lightLabel.setStyleSheet(GREY_QSS)
            elif '空调' in cmd:
                if cmd['空调'] == '开':
                    self.airConditionerRadioButton.setText(OPEN_BUTTON)
                    self.airConditionerRadioButton.setStyleSheet(WHITE_QSS)
                    self.airConditionerLable.setStyleSheet(WHITE_QSS)
                elif cmd['空调'] == '关':
                    self.airConditionerRadioButton.setText(CLOSE_BUTTON)
                    self.airConditionerRadioButton.setStyleSheet(GREY_QSS)
                    self.airConditionerLable.setStyleSheet(GREY_QSS)
            elif '门' in cmd:
                if cmd['门'] == '开':
                    self.doorRadioButton.setText(OPEN_BUTTON)
                    self.doorRadioButton.setStyleSheet(WHITE_QSS)
                    self.doorLable.setStyleSheet(WHITE_QSS)
                elif cmd['门'] == '关':
                    self.doorRadioButton.setText(CLOSE_BUTTON)
                    self.doorRadioButton.setStyleSheet(GREY_QSS)
                    self.doorLable.setStyleSheet(GREY_QSS)
        self.doorRadioButton.setStyleSheet(GREY_QSS)
        self.get_emotion()

    def show_web_result(self, web_list):
        for item in web_list:
            title = item.get('name')
            url = item.get('url')
            display_url = item.get('displayUrl')
            snippet = item.get('snippet')
            self.webBrowser.append("<b><font color=DarkOliveGreen size = 3 >%s</font></b>"%title)
            self.webBrowser.append("<a href=%s><font color=blue >%s</font></a>"%(url,display_url))
            self.webBrowser.append("%s"%snippet)
            self.webBrowser.append("\n")
        self.webBrowser.moveCursor(QtGui.QTextCursor.Start)

    def get_emotion(self):
        self.emotion_effective_flag = True
        self.result_once = 1
        self.emotion_count = 5
        self.emotion_api_timer.start(3000)

    def get_emotion_once(self):
        if self.emotion_count >= 0:
            self.emotion_count -= 1
            emotion = EmotionAnalyzeService()
            emotion.trigger.connect(self.analyze_emotion)
            emotion.start()
            self.thread_list.append(emotion)
        else:
            self.emotion_api_timer.stop()

    def analyze_emotion(self, emotions):
        if not self.emotion_effective_flag:
            return
        if 'error' not in emotions:
            min_emotion = -100
            result_emotion = ''
            print(emotions)
            for (k, v) in emotions.items():
                if v > min_emotion:
                    min_emotion = v
                    result_emotion = k
            self.emotion_list.append(result_emotion)
            if 'happiness' in self.emotion_list or \
                    'surprise' in self.emotion_list:
                self.happy_result()
            elif 'sadness' in self.emotion_list or \
                    'disgust' in self.emotion_list or \
                    'anger' in self.emotion_list:
                self.sad_result()
            elif 'neutral' in self.emotion_list:
                self.normal_result()
            else:
                self.normal_result()
        else:
            print("分析失败，空的返回数据：" + str(emotions))

    def happy_result(self):
        if self.result_once > 0:
            self.result_once -= 1
            self.happy_cortane()
            self.feedBackBrowser.setHtml("<center>对啦！</center>")
            self.happy_flag = 800
            self.happy_gif.frameChanged.connect(self.happy_twice)

    def sad_result(self):
        if self.result_once > 0:
            self.result_once -= 1
            self.sad_cortane()
            self.feedBackBrowser.setText("<center>对不起，听错啦</center>")
            self.sad_flag = 800
            self.sad_gif.frameChanged.connect(self.sad_twice)

    def normal_result(self):
        if self.result_once > 0:
            # self.result_once -= 1
            self.cortana_is_waiting()

    def sad_twice(self):
        if self.sad_flag < 0:
            self.cortana.click()
        else:
            self.sad_flag -= 1

    def happy_twice(self):
        if self.happy_flag < 0:
            self.cortana_is_waiting()
        else:
            self.happy_flag -= 1

    def cortana_is_waiting(self):
        if self.movie:
            self.movie.stop()
        self.set_cortane_move(self.waiting_gif)

    def cortana_is_listening(self):
        if self.movie:
            self.movie.stop()
        self.set_cortane_move(self.listening_gif)

    def cortana_is_thinking(self):
        if self.movie:
            self.movie.stop()
        self.set_cortane_move(self.thinking_gif)

    def happy_cortane(self):
        if self.movie:
            self.movie.stop()
        self.set_cortane_move(self.happy_gif)

    def sad_cortane(self):
        if self.movie:
            self.movie.stop()
        self.set_cortane_move(self.sad_gif)

    def set_cortane_move(self, gif):
        gif.frameChanged.connect(self.set_cortane_icon)
        self.movie = gif
        self.movie.start()

    def set_cortane_icon(self):
        self.cortana.setIcon(QtGui.QIcon(self.movie.currentPixmap()))
        self.littleCortana.setIcon(QtGui.QIcon(self.movie.currentPixmap()))

    @staticmethod
    def printout_data(data):
        print(data)
