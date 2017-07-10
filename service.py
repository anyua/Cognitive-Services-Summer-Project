from PyQt5 import QtWidgets, QtCore, QtGui
from device import Camera, Microphone
from cognitive_services import EmotionAPI, SpeechAPI


class Speech2TextService(QtCore.QThread):
    trigger = QtCore.pyqtSignal(str)

    def __init__(self):
        super(Speech2TextService, self).__init__()
        self.my_microphone = Microphone()
        self.api = SpeechAPI()

    def run(self):
        self.my_microphone.read_audio()
        self.my_microphone.save_wav()
        data = self.api.get_speech_service()
        if 'RecognitionStatus' in data and 'DisplayText' in data and data['RecognitionStatus'] == 'Success':
            self.trigger.emit(data['DisplayText'])
        else:
            print(data)
            self.trigger.emit("something error...")


class EmotionAnalyzeService(QtCore.QThread):
    trigger = QtCore.pyqtSignal(dict)

    def __init__(self):
        super(EmotionAnalyzeService, self).__init__()
        self.my_camera = Camera()
        self.api = EmotionAPI()

    def run(self):
        data = self.api.get_emotions()
        if data:
            self.trigger.emit(data)
        else:
            self.trigger.emit({'error': ''})


class LanguageUnderstandingService(QtCore.QThread):
    trigger = QtCore.pyqtSignal()

    def __init__(self):
        super(LanguageUnderstandingService, self).__init__()

    def run(self):
        pass
