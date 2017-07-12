from PyQt5 import QtWidgets, QtCore, QtGui
from gui.mainWindow import Ui_MainWindow
import icon_rc
import time
from service import Speech2TextService, EmotionAnalyzeService, LanguageUnderstandingService, BingWebSearchService

OPEN_BUTTON = chr(0xf205)
CLOSE_BUTTON = chr(0xf204)

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
        self.doorLable.setFont(QtGui.QFont('FontAwesome', 25))
        self.doorLable.setText(chr(0xf13e))
        self.airConditionerLable.setFont(QtGui.QFont('FontAwesome', 24))
        self.airConditionerLable.setText(chr(0xf2dc))
        self.lightRadioButton.setFont(QtGui.QFont('FontAwesome', 12))
        self.lightRadioButton.setText(OPEN_BUTTON)
        self.doorRadioButton.setFont(QtGui.QFont('FontAwesome', 12))
        self.doorRadioButton.setText(CLOSE_BUTTON)
        self.airConditionerRadioButton.setFont(QtGui.QFont('FontAwesome', 12))
        self.airConditionerRadioButton.setText(CLOSE_BUTTON)

        # 添加动图
        self.movie = None
        self.listening_gif = QtGui.QMovie(':img/listening')
        self.waiting_gif = QtGui.QMovie(':img/waiting')
        self.thinking_gif = QtGui.QMovie(':img/thinking')
        self.happy_gif = QtGui.QMovie(':img/happy')
        self.sad_gif = QtGui.QMovie(':img/sad')
        self.cortana_is_waiting()

        # 绑定按钮
        self.cortana.clicked.connect(self.new_voice)
        self.littleCortana.clicked.connect(self.new_voice)
        # 情感分析
        self.emotion_list = list()
        self.result_once = 0

    def new_voice(self):
        speech = Speech2TextService()
        speech.trigger.connect(self.analyze_text)
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
            self.toolBox.setCurrentIndex(1)
        else:
            # 去处理图标
            if '灯' in cmd:
                if cmd['灯'] == '开':
                    self.lightRadioButton.setText(OPEN_BUTTON)
                elif cmd['灯'] == '关':
                    self.lightRadioButton.setText(CLOSE_BUTTON)
            elif '空调' in cmd:
                if cmd['空调'] == '开':
                    self.airConditionerRadioButton.setText(OPEN_BUTTON)
                elif cmd['空调'] == '关':
                    self.airConditionerRadioButton.setText(CLOSE_BUTTON)
            elif '门' in cmd:
                if cmd['门'] == '开':
                    self.doorRadioButton.setText(OPEN_BUTTON)
                elif cmd['门'] == '关':
                    self.doorRadioButton.setText(CLOSE_BUTTON)
        self.get_emotion()

    def show_web_result(self, web_list):
        for item in web_list:
            title = item.get('name')
            url = item.get('url')
            display_url = item.get('displayUrl')
            snippet = item.get('snippet')
            self.webBrowser.append("<font color=blue>%s</font>"%title)
            self.webBrowser.append("%s"%display_url)
            self.webBrowser.append("%s"%snippet)

    def get_emotion(self):
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
        if 'error' not in emotions:
            min_emotion = -100
            result_emotion = ''
            for (k, v) in emotions.items():
                if v > min_emotion:
                    min_emotion = v
                    result_emotion = k
                print((k, v))
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
            print("分析失败，空的返回数据：" + str(emotions))

    def happy_result(self):
        if self.result_once > 0:
            self.result_once -= 1
            self.happy_cortane()
            self.feedBackBrowser.setText("对啦")

    def sad_result(self):
        if self.result_once > 0:
            self.result_once -= 1
            self.sad_cortane()
            self.feedBackBrowser.setText("听错了")
            # time.sleep(1000)
            # self.sad_gif.frameChanged.connect(lambda :if self.sad_gif.loopCount()>2 return self.new_voice())

    def normal_result(self):
        if self.result_once > 0:
            self.result_once -= 1
            self.cortana_is_waiting()

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



