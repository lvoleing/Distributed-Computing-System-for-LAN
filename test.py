from flask import Flask, render_template, request, redirect, url_for, make_response, jsonify, Response, send_from_directory, current_app
import os
import json
import base64
import pymysql
from io import BytesIO
import datetime
import logging
import mqManagementClass

class Website(object):

    def __init__(self, name=None, configFile = "../config/config.json"):

        with open(configFile, "r", encoding='utf-8') as f:
            configObj = json.load(f)
        self.db         = configObj['database']
        self.dbName     = self.db['database_name']
        self.dbUserName = self.db['user_name']
        self.dbPasswd   = self.db['passwd']
        self.dbHost     = self.db['database_host']
        self.logFile    = configObj['logs_file']
        self.ip         = configObj['webserver_host']
        self.port       = configObj['webserver_port']
        self.app        = Flask(name)
        self.logger     = logging.getLogger("Webserver_logger")
        handler         = logging.FileHandler(self.logFile)
        handler.setLevel(logging.DEBUG)
        logging_format = logging.Formatter(
                '%(asctime)s - %(levelname)s - %(filename)s - %(funcName)s - %(message)s')
        handler.setFormatter(logging_format)
        self.logger.addHandler(handler)
        self.logger.info("Webserver starts")

        # self.Usr_imgs   = "./Usr_imgs"
        # self.Transfer_Results = "./Transfer_Results"
        # self.biggest_task_num = 0
        # self.__in_file_path = configObj['in_file_path']
        # self.__out_file_path = configObj['out_file_path']
        

        # self.db=pymysql.connect(host = self.mysql_host, user = self.user,password = self.dbPasswd, db= self.dbName)
        # self.cur = self.db.cursor()

        @self.app.route("/submitCmd", methods=["POST"])
        def submitCmd():
            if request.method == 'POST':
                inputJson = request.json
                nodeIP    = inputJson['destination']
                mqMaster  = mqManagementClass.mqManagement()
                ifSuccess = mqMaster.sentCmdToNode(nodeIP , inputJson)
                outJson = {
                "success": ifSuccess
                }
                return json.dumps(outJson)
            
        @self.app.route("/submitInfo", methods=["POST"])
        def submitInfo():
            if request.method == 'POST':
                inputJson = request.json
                nodeIP    = inputJson['destination']
                mqMaster  = mqManagementClass.mqManagement()
                ifSuccess = mqMaster.sentMessageToNode(nodeIP , inputJson)
                outJson = {
                "success": ifSuccess
                }
                return json.dumps(outJson)

        

    def run(self, debug = False):
        self.app.run(host=self.ip, port=self.port, debug= debug)
    
if __name__ == '__main__':
    website = Website("style transfer")

    website.run(True)