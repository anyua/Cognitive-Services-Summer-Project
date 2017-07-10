import json
import http.client
import urllib.request
import urllib.parse
import urllib.error
from device import Camera
import requests
import time


class EmotionAPI(object):
    def __init__(self, camera=Camera()):
        self.headers = {
            # Request headers. Replace the placeholder key below with your subscription key.
            'Content-Type': 'application/octet-stream',
            'Ocp-Apim-Subscription-Key': 'a3a8071ffed142c0b194c38c6cdbb104',
        }
        self.params = urllib.parse.urlencode({
        })
        self.camera = camera
        self.conn = None
        self.body = []
        self.response = None
        self.data = None
        self.emotion = {}

    def get_response(self):
        try:
            self.body = self.camera.get_jpg()
            # NOTE: You must use the same region in your REST call as you used to obtain your subscription keys.
            #   For example, if you obtained your subscription keys from westcentralus, replace "westus" in the
            #   URL below with "westcentralus".
            self.conn = http.client.HTTPSConnection('westus.api.cognitive.microsoft.com')
            self.conn.request("POST", "/emotion/v1.0/recognize?%s" % self.params, self.body, self.headers)
            self.response = self.conn.getresponse()
            self.data = json.loads(self.response.read())
            # print(self.data)
            self.conn.close()
            return self.data
        except Exception as e:
            print(e.args)
            return None

    def get_emotions(self):
        if self.get_response():
            print(self.data)
            self.emotion = self.data[0]["scores"]
            return self.emotion
        else:
            return None


class SpeechAPI(object):
    def __init__(self):
        self.token_url = 'https://api.cognitive.microsoft.com' \
                         '/sts/v1.0/issueToken'
        self.token_headers = {'Ocp-Apim-Subscription-Key': '481f85de65d94ecf9c660d3a715a1521'}

        self.api_url = 'https://speech.platform.bing.com' \
                       '/speech/recognition/interactive/cognitiveservices/v1?language=zh-CN'
        self.api_headers = {'Content-type': 'audio/wav; codec="audio/pcm"; samplerate=16000',
                            'Transfer-Encoding': 'chunked',
                            'Authorization': 'Bearer '}
        self.token = ""
        self.speeech = ""
        self.token_time = None

    @staticmethod
    def read_in_block(filename):
        block_size = 1024
        with open(filename, 'rb') as f:
            while True:
                block = f.read(block_size)  # 每次读取固定长度到内存缓冲区
                if block:
                    yield block
                else:
                    return

    def access_token(self):
        response = requests.post(self.token_url, headers=self.token_headers)
        self.token = response.text
        self.token_time = time.time()
        # print(self.token)

    def get_speech_service(self, filename='temp/temp.wav'):
        now_time = time.time()
        if (not self.token_time) or (now_time - self.token_time)/60 < 8:
            self.access_token()
        self.api_headers['Authorization'] += self.token
        r = requests.post(self.api_url, headers=self.api_headers, data=self.read_in_block(filename))
        # print(r.text)
        # print(r.status_code)
        return json.loads(r.text)


if __name__ == "__main__":
    lalal = EmotionAPI()
    print(lalal.get_emotions())


