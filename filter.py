import paho.mqtt.client as mqtt
import threading
import pycurl 
import simplejson as json
import websocket 
from flask import Flask
from flask import request, render_template


crl = pycurl.Curl()


app = Flask(__name__)
app.url_map.strict_slashes = False


#--------------------------------------------------------------

class Hold_list():

    def __init__(self):
        self.file = []
        self.list_of_topics = []


    def add_topic(self, topic):
            if topic not in self.list_of_topics:
                self.list_of_topics += [topic]

    def get(self):
        return self.file

Hold_l = Hold_list()

#-------------------------------------------------------------


class Message_dict():
    def __init__(self):
        self.dict_of_messages = {}
    
    def add_dict(self, new, topic):
        if topic not in self.dict_of_messages:
            print(type(new))
            self.dict_of_messages[topic] = [new]
        else:
            self.dict_of_messages[topic] += [new]
        print(self.dict_of_messages)

    def get_data_from_dict(self, topic, pole):
        return self.dict_of_messages[topic][-1][pole] 



M_dict = Message_dict()

#--------------------------------------------------------------


def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)



def subscribe(client, topic, pola): 
    def on_message(client, userdata, msg):
        message = json.loads(msg.payload.decode())
        M_dict.add_dict(message, msg.topic)
        print(type(message))
        print(message.keys())
        print(f"Received `{message}` from `{msg.topic}` topic, qos {msg.qos}")
        result = ['filtr']
        for field in pola:
            result += [message[field]]
        print(result)
        if result is not None:
            ws.send(json.dumps(result))

        
    client.subscribe(topic, qos=0)
    client.on_message = on_message


host = '127.0.0.1' 
port = 8000 
def run_subscribe():
    global ws
    ws = websocket.WebSocket()
    ws.connect("ws://localhost:8000/yo")
    print(f"[+] Connecting to {host}:{port}")
    print("[+] Connected.") 

def clients(pola):
    for topic in Hold_l.list_of_topics:  
        print('w clients topic i slownik')
        print(topic)     
        print(topics[topic])
        client_1 = mqtt.Client("Subscriber" + topic)
        client_1.on_connect = on_connect
        client_1.connect("test.mosquitto.org", 1883, 80)
        activate_client_1(topics[topic], client_1, pola)


def activate_client_1(topic, client, pola):

    def run_job():   
        
        subscribe(client, topic, pola)

        client.loop_forever()

    thread = threading.Thread(target = run_job)
    thread.start()


topics = {'smog' : 'ss', 'cpu' : 'cpu', "temperature" : 'tt', "people" : 'pp', "money": 'kk'} 


@app.route('/', methods=['GET', 'POST', 'PUT'])
def main_page():
    if request.method == 'GET':
        return render_template('for_server.html', name = Hold_l.get())
    if request.method == 'POST':
        Hold_l.add(request.json)
        return ('', 204)
    if request.method == 'PUT':
        print(request.json)
        topics = request.json[0].split(',')
        pola = request.json[1].split(',')
        for i in topics:

            Hold_l.add_topic(i)
        clients(pola)
        return ('', 204)
        

if __name__ == '__main__':
    run_subscribe()
    app.run(port=8880)
    
    
