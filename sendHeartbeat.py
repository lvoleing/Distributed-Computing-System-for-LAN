from flask import Flask, request
from flask_apscheduler import APScheduler
import json
import socket
import datetime
import mqManagementClass

class Config(object): 
    # 任务列表
    JOBS = [  
        { 
            'id': 'heratbeat',
            'func': '__main__:sendHeartbeat', #执行函数
            'args': None,
            'trigger': 'interval', 
            'seconds': 10,  #间隔时间(S)
        }
    ]

app = Flask(__name__)
app.config.from_object(Config())

@app.route("/sendHeartbeat", methods=["POST"])
def sendHeartbeat():
    userName  = socket.gethostname()
    time      = datetime.datetime.now()
    timestamp = time.strftime("%Y%m%d%H%M%S%f")
    inputJson ={
        "destination": "192.168.4.16",
        "timestamp"  : timestamp,
        "user"       : userName,
        "cmd"        : None
    }
    nodeIP    = inputJson["destination"]
    mqMaster  = mqManagementClass.mqManagement()
    ifSuccess = mqMaster.sentCmdToNode(nodeIP , inputJson)
    print(ifSuccess)
    outJson = {
    "success": ifSuccess
    }
    return json.dumps(outJson)
 
if __name__ == '__main__':
    scheduler=APScheduler()
    scheduler.init_app(app)
    scheduler.start()
    app.run(debug=False)
