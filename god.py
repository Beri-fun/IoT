from flask import Flask
from flask import request, render_template
import os
import json
import requests

app = Flask(__name__)
app.url_map.strict_slashes = False

uploads_dir = os.path.join(app.instance_path, 'uploads')
list_of_data = []


class Hold_list():

    def __init__(self):
        self.dict_of_sensors = {}
        

    def add(self, example):

        self.dict_of_sensors[example['name']] = example
        

    def get(self):
        return self.dict_of_sensors
    
    

Hold_l = Hold_list()


@app.route('/', methods=['GET', 'POST'])
def main_page():
    if request.method == 'GET':
        return render_template('main.html', data=Hold_l.get())
    if request.method == 'POST':
        print(request.json)
        Hold_l.add(request.json)
        return ('', 204)

@app.route('/post', methods = ['GET', 'POST'])
def page2():
    if request.method == 'POST':       
        url = 'http://127.0.0.1:' + str(Hold_l.dict_of_sensors[request.form['names']]['port'])
        data = {'parameter': request.form['param'], 'value': request.form['warto']}
        r = requests.put(url, data=data).text
        print(r)
        return render_template('post.html')

@app.route('/active', methods = ['GET', 'POST'])
def active():
    if request.method == 'POST':
        url = 'http://127.0.0.1:' + str(Hold_l.dict_of_sensors[request.form['aaa']]['port'])
        print(Hold_l.dict_of_sensors[request.form['aaa']]['port'])
        data = {'parameter': 'frequency', 'value': '2'}
        r = requests.put(url, data=data).text
        print(r)
        return render_template('post.html')


@app.route('/super_sub', methods = ['GET', 'POST'])
def subsciber():
    if request.method == 'POST':    
        url = 'http://127.0.0.1:8080'
        
        temp = request.form['zz']
        temp = temp.split(', ')
        send = [request.form['czas']]
        send += [temp]
        print(send)

        headers = {'Content-type': 'application/json'}
        r = requests.put(url, data=json.dumps(send), headers=headers)
        print(r)
        return render_template('post.html')

@app.route('/filtr', methods = ['GET', 'POST'])
def filter():
    if request.method == 'POST':       
        url = 'http://127.0.0.1:8880'        
        send = [request.form['ff'], request.form['xx']]
        print(send)
        headers = {'Content-type': 'application/json'}
        r = requests.put(url, data=json.dumps(send), headers=headers)
        print(r)
        return render_template('post.html')

@app.route('/visual', methods = ['GET', 'POST'])
def graph():
    if request.method == 'GET':
        return render_template('index3.html')
    if request.method == 'POST':
        url = 'http://127.0.0.1:8000//visualize' 
        send = request.form['vv']
        print(send)
        headers = {'Content-type': 'application/json', 'Access-Control-Allow-Origin': '*'}
        r = requests.post(url, data=json.dumps(send), headers=headers)
        print(r)
        return render_template('post.html')





if __name__ == '__main__':
    app.run(port=8088)
