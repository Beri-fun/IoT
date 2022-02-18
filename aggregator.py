import paho.mqtt.client as mqtt
import threading
import pycurl 
import simplejson as json
import websocket 
from flask import Flask
from flask import request, render_template
import time

crl = pycurl.Curl()


app = Flask(__name__)
app.url_map.strict_slashes = False

#--------------------------------------------------------------

class Hold_list():

    def __init__(self):
        self.file = []
        self.list_of_topics = []

    def add(self, example):
        self.file += [example]

    def add_topic(self, topic):
            if topic not in self.list_of_topics:
                self.list_of_topics += topic

    def get(self):
        return self.file

Hold_l = Hold_list()

#-------------------------------------------------------------


class Message_dict():
    def __init__(self):
        self.dict_of_messages = {}
        self.sending_time = 0
    
    def add_dict(self, new, topic):
        if topic not in self.dict_of_messages:
            self.dict_of_messages[topic] = [new]
        else:
            self.dict_of_messages[topic] += [new]

    def get_dict(self, time_time, current_time): 
        time_time = int(time_time)     
        suma = 0
        

        
        actual_sensors = Hold_l.list_of_topics
        if self.sending_time == 0:
            for one in actual_sensors:
                final_topic = topics[one]
                if final_topic in self.dict_of_messages:
                    if len(self.dict_of_messages[final_topic]) > 0:
                        suma += sum(self.dict_of_messages[final_topic])
                        self.dict_of_messages[final_topic] = []

            self.sending_time = time.time()
            return suma/len(Hold_l.list_of_topics)

        if (current_time - self.sending_time) >= time_time:
            for one in actual_sensors:
                final_topic = topics[one]
                if final_topic in self.dict_of_messages:
                    if len(self.dict_of_messages[final_topic]) > 0:
                        suma += sum(self.dict_of_messages[final_topic])
                        self.dict_of_messages[final_topic] = []
            self.sending_time = time.time()
            return suma/len(Hold_l.list_of_topics)

M_dict = Message_dict()

#--------------------------------------------------------------


def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)



def subscribe(client, topic, time_time): 
    def on_message(client, userdata, msg):
        message = json.loads(msg.payload.decode())
        
        print(message)
        ke = list(message.keys())

        M_dict.add_dict(message[field[msg.topic]], msg.topic)
        print(f"Received `{message}` from `{msg.topic}` topic, qos {msg.qos}")
        current_time = time.time()
        result = ['mean']
        result += [M_dict.get_dict(time_time, current_time)]
        if result[1] is not None :
            ws.send(json.dumps(result))

        
    client.subscribe(topic, qos=0)
    client.on_message = on_message


host = '127.0.0.1' 
port = 8000  
def run_subscribe():
    global ws
    ws = websocket.WebSocket()
    ws.connect("ws://localhost:8000/data")
    print(f"[+] Connecting to {host}:{port}")
    print("[+] Connected.") 

def clients(time_time):
    for topic in Hold_l.list_of_topics:  
        client_1 = mqtt.Client("Subscriber" + topic)
        client_1.on_connect = on_connect
        client_1.connect("test.mosquitto.org", 1883, 80)
        activate_client_1(topics[topic], client_1, time_time)


def activate_client_1(topic, client, time_time):

    def run_job():   
        subscribe(client, topic, time_time)
        client.loop_forever()

    thread = threading.Thread(target = run_job)
    thread.start()


topics = {'smog' : 'ss', 'cpu' : 'cpu', "temperature" : 'tt', "people" : 'pp', "money": 'kk'} 
field = {'ss' : 'Srednia', 'cpu' : 'Statistics', 'tt' : 'Polska', 'pp' : 'People in room', 'kk': 'Kurs sredni'}



@app.route('/', methods=['GET', 'POST', 'PUT'])
def main_page():
    if request.method == 'GET':
        return render_template('for_server.html', name = Hold_l.get())
    if request.method == 'POST':
        Hold_l.add(request.json)
        return ('', 204)
    if request.method == 'PUT':
        print('request',request.json)
        time_time = request.json[0]
        del request.json[0]

        Hold_l.add_topic(request.json[0])
        clients(time_time)
        return ('', 204)
        

if __name__ == '__main__':
    run_subscribe()
    app.run(port=8080)
    
    
