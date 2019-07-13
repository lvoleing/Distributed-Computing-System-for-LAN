import urllib
from urllib import request, parse
import json
import base64
import time
import socket
import datetime

def submitTask():
    url = "http://127.0.0.1:9090/submitCmd"
    print (url)
    userName  = socket.gethostname()
    ip        = socket.gethostbyname(userName)
    time      = datetime.datetime.now()
    timestamp = time.strftime("%Y%m%d%H%M%S%f")
    value     ={
        "destination": "192.168.4.167",
        "timestamp"  : timestamp,
        "user"       : userName,
        "cmd"        : "SR" 
    }
    data      = json.dumps(value)
    headers   = {
        'Content-Type':'application/json'
    }
    data      = data.encode(encoding='utf-8')
    req       =urllib.request.Request(url=url,data=data,headers=headers)
    res_data  = urllib.request.urlopen(req)
    returnData= res_data.read().decode("utf-8")
    print(returnData)
    configObj = json.loads(returnData)
    
    return configObj

def getTaskResult(id,suffix,filePath2Save="./"):
    url = "http://www.51i-art.com/getTaskResult"
    headers = {
        'Content-Type':'application/json'
    }
    value={
        "task_id":id
    }
    data = json.dumps(value)
    data = data.encode(encoding='utf-8')
    req=urllib.request.Request(url=url,data=data,headers=headers)
    res_data    = urllib.request.urlopen(req)
    res_data    = res_data.read()
    res_data    = str(res_data, encoding='utf-8')
    res_json    = json.loads(res_data)
    res_url     = res_json["result_image"]
    url = "http://www.51i-art.com%s"%res_url
    imgPath=filePath2Save + "%s.%s"%(id,suffix)
    request.urlretrieve(url, imgPath,reporthook=reporFun) 

def reporFun(a,b,c):
    per=100.0*a*b/c  
    if per>100:  
        per=100  
    print('%.1f%%' % per)

def checkTask(id):
    url = "http://www.51i-art.com/checkTaskStatus"
    value={
        "task_id":id
    }
    data = json.dumps(value)
    headers = {
        'Content-Type':'application/json'
    }
    data = data.encode(encoding='utf-8')
    req=urllib.request.Request(url=url,data=data,headers=headers)
    res_data = urllib.request.urlopen(req)
    returnData = res_data.read().decode("utf-8")
    print(returnData)
    configObj = json.loads(returnData)
    status    = int(configObj["task_status"])
    if status == 1:
        return True
    else:
        return False

def getFilterList():
    url = "http://www.51i-art.com/getFilterList"
    headers = {
        'Content-Type':'application/json'
    }
    req=urllib.request.Request(url=url,headers=headers)
    res_data = urllib.request.urlopen(req)
    print(res_data.read())

def getProductType():
    url = "http://www.51i-art.com/getProductTypeList"
    headers = {
        'Content-Type':'application/json'
    }
    req=urllib.request.Request(url=url,headers=headers)
    res_data = urllib.request.urlopen(req)
    print(res_data.read())

def getTaobaoLink():
    url = "http://www.51i-art.com/getTaobaoLink"
    headers = {
        'Content-Type':'application/json'
    }
    req=urllib.request.Request(url=url,headers=headers)
    res_data = urllib.request.urlopen(req)
    print(res_data.read())
    
def createOrder():
    url = "http://www.51i-art.com/createOrder"
    value={
        "painted_art_id":"1",
        "task_id":"174",
        "product_id": ["0", "1", "2"],
        "wechat_name": "你大爷",
        "total_price": "291.0"
    }
    data = json.dumps(value)
    headers = {
        'Content-Type':'application/json'
    }
    data = data.encode(encoding='utf-8')
    req=urllib.request.Request(url=url,data=data,headers=headers)
    res_data = urllib.request.urlopen(req)
    print(res_data.read())

def getOrder(id):
    url = "http://www.51i-art.com/getOrder"
    value={
        "order_id":"%d"%id
    }
    data = json.dumps(value)
    headers = {
        'Content-Type':'application/json'
    }
    data = data.encode(encoding='utf-8')
    req=urllib.request.Request(url=url,data=data,headers=headers)
    res_data = urllib.request.urlopen(req)
    print(res_data.read())

if __name__ == '__main__':

    configObj = submitTask()
    # taskId=int(configObj["task_id"])
    # waitingTime=int(configObj["suggest_pull_interval_time"])/1000
    # flag = True
    # while flag:
    #     time.sleep(waitingTime)
    #     print("waiting...")
    #     if checkTask(taskId):
    #         flag = False
    # getTaskResult(taskId,suffix=suffix)
    # checkTask(647)
    # getFilterList()
    # getProductType()
    # createOrder()
    # getOrder(47)
    # for i in range(162):
    # checkTask(11)
    #     submitTask()
    # getFilterList()