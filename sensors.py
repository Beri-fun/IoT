import numpy as np
import pandas as pd 
import paho.mqtt.client as mqtt
import json
import time
import pycurl
from flask import Flask, request
from flask_restful import Resource, Api
import requests
import threading

sensor_dict = {
    'money' : ("money.csv", 'mqtt','test.mosquitto.org', 2, 'kk'),
    'smog' : ("smog.csv", 'mqtt','test.mosquitto.org', 2, 'ss'),
    'temperature' : ("temperature.csv", 'mqtt','test.mosquitto.org', 2, 'tt'),
    'cpu' : ("cpu_statistics.csv", 'mqtt','test.mosquitto.org', 2, 'cpu'),
    'people' : ("people.csv", 'mqtt','test.mosquitto.org', 2, 'pp'),
}


class Sensor():
    def __init__(self, filename, server_type, server_name, k, topic = None):
        
        self.k = k
        self.server_type = server_type
        self.server_name = server_name
        self.topic = topic
        self.number = '8080'
        self.crl = pycurl.Curl()
        self.client = mqtt.Client("Generator_mqtt"+topic)
        self.url = "http://localhost:" 
        if self.server_type == 'mqtt': 
            self.server_name = 'test.mosquitto.org'
            self.client.connect(self.server_name)
            print('Connected to MQTT')

        if self.server_type == 'http':      
            print(self.url+self.number)  
            url_1 = self.url+self.number
            self.crl.setopt(self.crl.URL, url_1)
            print("Connected to your server")

        self.list = []
        self.list_of_all_data = []
        data = pd.read_csv(filename)
        for i in data:
            self.list += [i]

        self.counter = 0
        for i in range(data.shape[0]):
            temp = {}
            for head in self.list:
                if isinstance(data[head][i], np.float64):
                    temp[head] = float(data[head][i])
                elif isinstance(data[head][i], np.int64):
                    temp[head] = int(data[head][i])
                else:
                    temp[head] = data[head][i]

            self.list_of_all_data += [temp]


    def publish_mqtt(self):
        print(self.topic)
        if self.counter <= len(self.list_of_all_data):
            result = self.client.publish(self.topic, json.dumps(self.list_of_all_data[self.counter]), qos=0, retain=True)
            self.counter += 1

            status = result[0]
            print(result)
            if status == 0:
                print('Send data')
            else:
                print("Failed to send data")

    def publish_http(self, url):
        if self.counter <= len(self.list):
            headers = {'Content-type': 'application/json'}
            r = requests.post(url, data=json.dumps(self.list[self.counter]), headers=headers)
            
            print(self.list[self.counter])
            self.counter += 1
            print(r)

    def runrun(self):
        while True:
            time.sleep(self.k)
            self.run_publish()

    
    def run_publish(self):
        if self.server_type == 'mqtt':
            self.publish_mqtt()

        if self.server_type == 'http':
            self.publish_http(self.url+self.number)
    
    def change_k(self, k_new):
        self.k = k_new

    def change_server_type(self, server_new):
        self.server_type = server_new
        if server_new == 'http':
            url_1 = self.url+self.number 
            self.crl.setopt(self.crl.URL, url_1)
        if server_new == 'mqtt':
            self.client.connect(self.server_name, 1883, 80)

    def change_server_name(self, name_new):
        self.server_name = name_new
        self.client.connect(self.server_name, 1883, 80)
        print('success change')

    def change_number(self, number_new):
        self.number = number_new
        print('success change')

    def change_topic(self, topic_new):
        self.topic = topic_new
        print('success change')



app = Flask(__name__)
api = Api(app)


class TodoSimple(Resource):

    def put(self):
        slowniczek_temp = {}
        for k in request.form: 
            slowniczek_temp[k] = request.form[k]
        for key in slowniczek_temp:

            if slowniczek_temp[key] == 'typ of server':
               slowniczek_temp[key] = 'server_type'
            if request.form[key] == 'frequency':
               slowniczek_temp[key] = 'change_time'


            if slowniczek_temp[key] == 'change_time':
                sensor.change_k(int(slowniczek_temp['value']))
                message['frequency'] = sensor.k
                if message['state'] == 'not sending':
                    message['state'] = 'sending'
                headers = {'Content-type': 'application/json'}
                r = requests.post("http://localhost:8088", data=json.dumps(message), headers=headers)
                print(r)
                return 'ok'
            if slowniczek_temp[key] == 'server_type':
                sensor.change_server_type(slowniczek_temp['value'])
                message['typ of servera'] = sensor.server_type
                if message['state'] == 'not sending':
                    message['state'] = 'sending'
                headers = {'Content-type': 'application/json'}
                r = requests.post("http://localhost:8088", data=json.dumps(message), headers=headers)
                print(r)
                return 'ok'
            if slowniczek_temp[key] == 'server_name':
                sensor.change_server_name(slowniczek_temp['value'])
                if message['state'] == 'not sending':
                    message['state'] = 'sending'
                headers = {'Content-type': 'application/json'}
                r = requests.post("http://localhost:8088", data=json.dumps(message), headers=headers)
                print(r)
                return 'ok'
            if slowniczek_temp[key] == 'server_number':
                sensor.change_number(slowniczek_temp['value']) 
                if message['state'] == 'not sending':
                    message['state'] = 'sending'
                headers = {'Content-type': 'application/json'}
                r = requests.post("http://localhost:8088", data=json.dumps(message), headers=headers)
                print(r)  
                return 'ok'
            if slowniczek_temp[key] == 'topic':
                sensor.change_topic(str(slowniczek_temp['value'])) 
                message['topic'] = sensor.topic
                if message['state'] == 'not sending':
                    message['state'] = 'sending'
                headers = {'Content-type': 'application/json'}
                r = requests.post("http://localhost:8088", data=json.dumps(message), headers=headers)
                print(r)  
                return 'ok'



api.add_resource(TodoSimple, '/')


@app.before_first_request
def activate_job():
    def run_job():
        sensor.runrun()

    thread = threading.Thread(target=run_job)
    thread.start()


def create_app(sensor_name=None, port=None):
    global sensor

    app.config["sensor"] = sensor_name
    global message
    message = {
        'name' : app.config["sensor"],
        'state' : 'not sending',
        'typ of server' : sensor_dict[app.config["sensor"]][1],
        'frequency' : sensor_dict[app.config["sensor"]][3],
        'topic' : sensor_dict[app.config["sensor"]][4],
        'port' : port
    }

    print(sensor_name)
    sensor = Sensor(*(sensor_dict[sensor_name]))
    crl = pycurl.Curl()
    crl.setopt(crl.URL, "http://localhost:8088")
    print('sensor connected to GOD')
    headers = {'Content-type': 'application/json'}
    r = requests.post("http://localhost:8088", data=json.dumps(message), headers=headers)
    print(r)
    return app

