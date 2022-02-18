from flask import Flask
from flask import request, render_template
import os
from flask_sock import Sock
import json


app = Flask(__name__)
app.url_map.strict_slashes = False

uploads_dir = os.path.join(app.instance_path, 'uploads')
list_of_data = []
global already_send 
already_send = []


sock=Sock(app)

class Hold_list():

    def __init__(self):
        self.source = None
        self.list_of_files = []
        self.dict_of_files = {}

    def add_to_list(self, example):
        example = example.split(', ')
        self.list_of_files += [float(example[1])]
        print('list_of_list', self.list_of_files)

    def add(self, example):

        example = example.split(', ')

        if example[0][1:-1] not in self.dict_of_files:
            self.dict_of_files[example[0][1:-1]] = [example[1:]]
        else:
            self.dict_of_files[example[0][1:-1]] += [example[1:]]
        print(self.dict_of_files)

    def get(self):
        return self.dict_of_files
        

Hold_l = Hold_list()

@sock.route('/yo')
def echo_socket(ws):
    while True:
        message = ws.receive()
        Hold_l.add(message[1:-1])
        Hold_l.add_to_list(message[1:-1])

@sock.route('/data')
def echo_socket_1(ws):
    while True:
        message = ws.receive()
        Hold_l.add(message[1:-1])
        Hold_l.add_to_list(message[1:-1])
        
        


@app.route('/show', methods=['GET', 'POST'])
def main_page():
    if request.method == 'GET':
        return render_template('for_server.html', name=Hold_l.get())
    if request.method == 'POST':
        Hold_l.add(request.json[0], request.json[1:])
        return ('', 204)

@app.route('/visualize', methods=['GET', 'POST'])
def page2():
    if request.method == 'POST':
        Hold_l.source = request.json
        return ('', 204)

@app.route('/json', methods=['GET', 'POST'])
def biera_jasona():
    if request.method == 'GET':
        if Hold_l.source is not None:
            if len(Hold_l.dict_of_files[Hold_l.source]) > 0:
                to_send = Hold_l.dict_of_files[Hold_l.source][0]
                del Hold_l.dict_of_files[Hold_l.source][0]
                return json.dumps(to_send)
            else:
                return json.dumps(None)
        else:
            return json.dumps(None)


if __name__ == '__main__':
    app.run(port=8000)

