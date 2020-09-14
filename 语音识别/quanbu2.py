# coding: utf-8
import urllib2
import json
import base64
import os
import urllib
import time
import datetime
import serial
ser = serial.Serial('/dev/rfcomm0',9600,timeout=1)
baidu_server = "https://openapi.baidu.com/oauth/2.0/token?"
grant_type = "client_credentials"
client_id = "WUPlWzkwF5KbG1typ8EOGglh"
client_secret = "ZAs8igGeEOF2plKP9kGmIXgXKeeXdoGN" #填写Secret Key

#合成请求token的URL
url = baidu_server+"grant_type="+grant_type+"&client_id="+client_id+"&client_secret="+client_secret

#获取token
res = urllib2.urlopen(url).read()
data = json.loads(res)
token = data["access_token"]
#print token

print ('正在录音')
os.system('arecord -d 5 -r 8000 -c 1 -t wav -f S16_LE -D plughw:1,0  ddd.wav')
#设置音频属性，根据百度的要求，采样率必须为8000，压缩格式支持pcm（不压缩）、wav、opus、speex、amr
VOICE_RATE = 8000
WAVE_FILE = "ddd.wav" #音频文件的路径
USER_ID = "zhp-fw" #用于标识的ID，可以随意设置
WAVE_TYPE = "wav"
print ('录音结束,正在识别')

#打开音频文件，并进行编码
f = open(WAVE_FILE, "r")
speech = base64.b64encode(f.read())
size = os.path.getsize(WAVE_FILE)
update = json.dumps({"format":WAVE_TYPE, "rate":VOICE_RATE, 'channel':1,'cuid':USER_ID,'token':token,'speech':speech,'len':size})
headers = { 'Content-Type' : 'application/json' } 
url = "http://vop.baidu.com/server_api"
req = urllib2.Request(url, update, headers)

r = urllib2.urlopen(req)

#语音识别
t = r.read()
result = json.loads(t)
#print result
if result['err_msg']=='success.':
    word = result['result'][0].encode('utf-8')
    #word = result['result'].encode('utf-8')
    if word!='':
        #if word[len(word)-3:len(word)]==',':
            #print word[0:len(word)-3]
        #else:
        #串口发送
        t1 = word
        t2 = t1.decode("utf-8")  #转换成 unicode 编码
        #print(t2,type(t2))
        t3 = t2.encode("gbk")   #解码成 gbk 中文
        #print(t3,type(t3))
        t4 = t1[:-1]
        t5 = t4[:-1]
        t6 = t3[:-1]
        t7 = t6[:-1]
        s = ser.write(t7)
        ser.close()
        print t5   
    else:
        print "音频文件不存在或格式错误"
else:
    print "错误"
    
#串口发送
'''
t1 = word
t2 = t1.decode("utf-8")  #转换成 unicode 编码
#print(t2,type(t2))
t3 = t2.encode("gbk")   #解码成 gbk 中文
#print(t3,type(t3))
t4 = t1[:-1]
t5 = t4[:-1]
s = ser.write(t5)
ser.close()
'''
#s = ser.write("word sys")    
#s = ser.write('\r\n')
#图灵
print('稍等，正在回答你的问题：')
time.sleep(2)
'''
def getHtml(url):  
    page = urllib.urlopen(url)  
    html = page.read()  
    return html
key = '4e348190e92547fe85efc3fb137345e7'  
api = 'http://www.tuling123.com/openapi/api?key=' + key + '&info='  
#        info = raw_input('我: ')  
request = api + word  
response = getHtml(request)  
dic_json = json.loads(response)  
print '答: '.decode('utf-8') + dic_json['text']
'''


#-*- coding: utf-8 -*-
import requests
import re
import time
import hashlib
import base64
import struct
import json
import urllib2
import urllib
import os
import sys
reload(sys) 
sys.setdefaultencoding('utf-8') 

API_KEY_tuling = '4e348190e92547fe85efc3fb137345e7'
raw_TULINURL = "http://www.tuling123.com/openapi/api?key=%s&info=" % API_KEY_tuling

def result():
    for i in range(1,100):
        #queryStr = raw_input("我:".decode('utf-8'))
        queryStr = word
        
        TULINURL = "%s%s" % (raw_TULINURL,urllib2.quote(queryStr))
        req = urllib2.Request(url=TULINURL)
        result = urllib2.urlopen(req).read()
        hjson=json.loads(result)
        length=len(hjson.keys())
        content=hjson['text']

        if length==3: 
            #return 'robots:' +content+hjson['url']
            return  content+hjson['url']
        elif length==2:           
            #return 'robots:' +content
            return content

#print "你好，请输入内容:".decode('utf-8')
contents=result()
print contents        

#from urlparse import urlparse        #  python2
#import urllib.parse                  #  python3

# 讯飞语音合成
# API请求地址、API KEY、APP ID等参数，提前填好备用
api_url = "http://api.xfyun.cn/v1/service/v1/tts"
API_KEY = "66a9f4678e37d1e4216e3905080dfa93"
APP_ID = "5ae6bb87"
#OUTPUT_FILE = "/home/pi/chat/output.mp3"    # 输出音频的保存路径，请根据自己的情况替换
OUTPUT_FILE = "output.mp3" 
#TEXT = "苟利国家生死以，岂因祸福避趋之"
#TEXT = "你好，我叫天猫，有什么吩咐"
TEXT = contents

# 构造输出音频配置参数
Param = {
    "auf": "audio/L16;rate=16000",    #音频采样率
    "aue": "lame",    #音频编码，raw(生成wav)或lame(生成mp3)
    "voice_name": "xiaoyan",
    #"voice_name": "xiaoru",
    "speed": "50",    #语速[0,100]
    "volume": "77",    #音量[0,100]
    "pitch": "50",    #音高[0,100]
    "engine_type": "aisound"    #引擎类型。aisound（普通效果），intp65（中文），intp65_en（英文）
}
# 配置参数编码为base64字符串，过程：字典→明文字符串→utf8编码→base64(bytes)→base64字符串
Param_str = json.dumps(Param)    #得到明文字符串
Param_utf8 = Param_str.encode('utf8')    #得到utf8编码(bytes类型)
Param_b64 = base64.b64encode(Param_utf8)    #得到base64编码(bytes类型)
Param_b64str = Param_b64.decode('utf8')    #得到base64字符串

# 构造HTTP请求的头部
time_now = str(int(time.time()))
checksum = (API_KEY + time_now + Param_b64str).encode('utf8')
checksum_md5 = hashlib.md5(checksum).hexdigest()
header = {
    "X-Appid": APP_ID,
    "X-CurTime": time_now,
    "X-Param": Param_b64str,
    "X-CheckSum": checksum_md5
}

# 构造HTTP请求Body
body = {
    "text": TEXT
}
#body_urlencode = urllib.parse.urlencode(body)    #python3
body_urlencode = urllib.urlencode(body)     #python2

body_utf8 = body_urlencode.encode('utf8')

# 发送HTTP POST请求
req = urllib2.Request(api_url, data=body_utf8, headers=header)
response = urllib2.urlopen(req)

# 读取结果
response_head = response.headers['Content-Type']
if(response_head == "audio/mpeg"):
    out_file = open(OUTPUT_FILE, 'wb')
    data = response.read() # a 'bytes' object
    out_file.write(data)
    out_file.close()
    print('输出文件: ' + OUTPUT_FILE)
else:
    print(response.read().decode('utf8'))
os.system('mplayer output.mp3')    


