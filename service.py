from PyQt5 import QtWidgets, QtCore, QtGui
from device import Camera, Microphone
from cognitive_services import EmotionAPI, SpeechAPI, luisAPI, BingWebSearchAPI


class Speech2TextService(QtCore.QThread):
    trigger = QtCore.pyqtSignal(str)
    listening_complete = QtCore.pyqtSignal()

    def __init__(self):
        super(Speech2TextService, self).__init__()
        self.my_microphone = Microphone()
        self.api = SpeechAPI()

    def run(self):
        try:
            self.my_microphone.read_audio()
            self.my_microphone.save_wav()
        except Exception as e:
            print("something error of the microphone........")
            print(e)
            self.trigger.emit('')
            return
        self.listening_complete.emit()
        data = self.api.get_speech_service()
        if 'RecognitionStatus' in data and 'DisplayText' in data and data['RecognitionStatus'] == 'Success':
            self.trigger.emit(data['DisplayText'])
        else:
            print("语音转文字失败："+ str(data))
            self.trigger.emit('')


class EmotionAnalyzeService(QtCore.QThread):
    trigger = QtCore.pyqtSignal(dict)

    def __init__(self):
        super(EmotionAnalyzeService, self).__init__()
        self.my_camera = Camera()
        self.api = EmotionAPI()

    def run(self):
        data = self.api.get_emotions(self.currentThreadId())
        if data:
            self.trigger.emit(data)
        else:
            self.trigger.emit({'error': ''})


class LanguageUnderstandingService(QtCore.QThread):
    trigger = QtCore.pyqtSignal(dict)

    def __init__(self, text):
        super(LanguageUnderstandingService, self).__init__()
        self.text = text
        self.api = luisAPI(text)

    def run(self):
        data = self.api.get_luis_response()
        if data != {}:
            self.trigger.emit(data)
        else:
            self.trigger.emit({'error': self.text})


class BingWebSearchService(QtCore.QThread):
    trigger = QtCore.pyqtSignal(list)

    def __init__(self, text):
        super(BingWebSearchService, self).__init__()
        self.text = text
        self.api = BingWebSearchAPI(self.text)

    def run(self):
        data = self.api.get_web_search()
        if data:
            self.trigger.emit(data)
        else:
            self.trigger.emit(['error'])
