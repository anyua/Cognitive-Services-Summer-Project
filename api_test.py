import requests
import sys
import http.client,urllib.request,requests,wave

myHeaders = {'Ocp-Apim-Subscription-Key': '481f85de65d94ecf9c660d3a715a1521'
             }
url = 'https://api.cognitive.microsoft.com/sts/v1.0/issueToken'

response = requests.post(url, headers=myHeaders)
response.raise_for_status()
token = response.text
print(token)


def read_in_block():
    BLOCK_SIZE = 1024
    with open('temp/temp.wav', 'rb') as f:
        while True:
            block = f.read(BLOCK_SIZE)  # 每次读取固定长度到内存缓冲区
            if block:
                yield block
            else:
                return
url = 'https://speech.platform.bing.com/speech/recognition/interactive/cognitiveservices/v1?language=zh-CN'
headers = {'Content-type': 'audio/wav; codec="audio/pcm"; samplerate=16000',
           'Transfer-Encoding': 'chunked',
           'Authorization': 'Bearer ' + token
           }
r = requests.post(url, headers=headers, data=read_in_block())


print(r.text)
print(r.status_code)
