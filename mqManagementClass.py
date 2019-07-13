import pika
import sys
import json
import logging

class mqManagement:
    def __init__(self,configFilePath = "../config/config.json"):
        
        with open(configFilePath, "r", encoding='utf-8') as f:
            configObj = json.load(f)
        self.__db__         = configObj['database']
        self.__dbName__     = self.__db__['database_name']
        self.__dbUserName__ = self.__db__['user_name']
        self.__dbPasswd__   = self.__db__['passwd']
        self.__dbHost__     = self.__db__['database_host']
        self.__logFile__    = configObj['logs_file']
        self.__ip__         = configObj['webserver_host']
        self.__masterNode__ = configObj['master_node']
        self.__host__       = self.__masterNode__['host']
        self.__rabbitMQ__   = configObj['rabbitMQ']
        self.__mqUsername__ = self.__rabbitMQ__["username"]
        self.__mqPassword__ = self.__rabbitMQ__["password"]
        self.__mqVHost__    = self.__rabbitMQ__["virtual_host"]
        self.__nodeList__   = ["192.168.4.8","192.168.4.164","192.168.4.167"]

        self.__logger__ = logging.getLogger("GPUserver_logger")
        self.__logger__.setLevel(logging.DEBUG)
        __handler__ = logging.FileHandler(self.__logFile__, encoding='UTF-8')
        __loggingFormat__ = logging.Formatter(
        '%(asctime)s-%(levelname)s-%(filename)s-%(funcName)s-%(lineno)s-%(message)s')
        __handler__.setFormatter(__loggingFormat__)
        self.__logger__.addHandler(__handler__)

        #建立消息队列连接
        credentials = pika.PlainCredentials(username= self.__mqUsername__, password=self.__mqPassword__)
        self.__connection__ = pika.BlockingConnection(
            pika.ConnectionParameters(host=self.__host__,virtual_host=self.__mqVHost__, credentials=credentials))
        self.__channel__ = self.__connection__.channel()
        #声明路由
        self.__channel__.exchange_declare(exchange='direct_logs', exchange_type='direct')

    def readNodesInfo(self):

        
        return self.__nodeList__

    def sentCmdToNode(self,nodeIP,cmdBody):
        if nodeIP in self.__nodeList__:
            routingKey = nodeIP
            cmd = json.dumps(cmdBody)
            self.__channel__.basic_publish(exchange='direct_logs', routing_key=routingKey, body=cmd)
            self.__logger__.info("successfully Sent %r to %r" % (cmd,routingKey))
            self.__connection__.close()
            ifSuccess = True
        else: 
            ifSuccess = False
            self.__logger__.warning("%r don't exist" % (nodeIP))
        return ifSuccess

    def sentMessageToNode(self,nodeIP,infoBody):
        if nodeIP in self.__nodeList__:
            routingKey = nodeIP
            message = json.dumps(infoBody)
            self.__channel__.basic_publish(exchange='direct_logs', routing_key=routingKey, body=message)
            self.__logger__.info("successfully Sent %r to %r" % (message,routingKey))
            self.__connection__.close()
            ifSuccess = True
        else: 
            ifSuccess = False
            self.__logger__.info("%r don't exist" % (nodeIP))
            return ifSuccess




