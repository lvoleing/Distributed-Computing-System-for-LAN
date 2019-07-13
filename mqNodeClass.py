import pika
import sys
import json
import socket
import logging

class mqNodeClass:
    def __init__(self,configFilePath = "../config/config.json"):
        
        with open(configFilePath, "r", encoding='utf-8') as f:
            configObj = json.load(f)
        self.__logFile__    = configObj['logs_file']
        self.__masterNode__ = configObj['master_node']
        self.__host__       = self.__masterNode__['host']
        self.__rabbitMQ__   = configObj['rabbitMQ']
        self.__mqUsername__ = self.__rabbitMQ__["username"]
        self.__mqPassword__ = self.__rabbitMQ__["password"]
        self.__mqVHost__    = self.__rabbitMQ__["virtual_host"]

        self.__logger__ = logging.getLogger("GPUserver_logger")
        self.__logger__.setLevel(logging.DEBUG)
        __handler__ = logging.FileHandler(self.__logFile__, encoding='UTF-8')
        __logging_format = logging.Formatter(
        '%(asctime)s-%(levelname)s-%(filename)s-%(funcName)s-%(lineno)s-%(message)s')
        __handler__.setFormatter(__logging_format)
        self.__logger__.addHandler(__handler__)

        #建立消息队列连接
        credentials = pika.PlainCredentials(username= self.__mqUsername__, password=self.__mqPassword__)
        self.__connection__ = pika.BlockingConnection(
            pika.ConnectionParameters(host=self.__host__,virtual_host=self.__mqVHost__, credentials=credentials))
        self.__channel__ = self.__connection__.channel()
        #声明路由
        self.__channel__.exchange_declare(exchange='direct_logs', exchange_type='direct')

        #声明队列
        result = self.__channel__.queue_declare('', exclusive=True,durable=True)
        self.queue_name = result.method.queue

        #获得路由键
        host = socket.gethostbyname(socket.gethostname())
        bindingKey = host
        self.__channel__.queue_bind(exchange='direct_logs', queue=self.queue_name, routing_key=bindingKey)
        print(' [*] Waiting for logs. To exit press CTRL+C')

    def __queryMessage__(self):

        self.__channel__.basic_consume(queue=self.queue_name, on_message_callback=self.__messageParse__, auto_ack=True)
        self.__channel__.start_consuming()

    def __messageParse__(self,ch,method,properties,body):
        print(" [x] %r:%r" % (method.routing_key, body))

    


if __name__ == "__main__":
    test = mqNodeClass()
    test.__queryMessage__()

