# -*- encoding=utf-8 -*-
import redis
import json
from numpy import random
from flask import Flask,jsonify,abort,make_response
from flask_httpauth import HTTPBasicAuth

app = Flask(__name__)
auth = HTTPBasicAuth()

def getproxys(proxys = []):
     db = redis.Redis(host='127.0.0.1', port=6379, db=0)
     hash_name_list = [num.decode('ascii') for num in db.keys('*')]
     for ip in hash_name_list:
         tag = db.hget(ip, 'tag').decode('ascii')
         if tag == '0':
             continue
         port = db.hget(ip,'port').decode('ascii')
         tp = db.hget(ip,'type').decode('ascii').lower()
         lastcheck = db.hget(ip,'lastcheck').decode('ascii')
         source  = db.hget(ip,'source').decode('ascii')
         proxy = tp+'://'+ip+':'+port
         proxy = {
             'ip':ip,
             'port':port,
             'type':tp,
             'lastcheck':lastcheck,
             'proxy': proxy,
             'tag':tag,
             'source':source
         }
         proxys.append(proxy)

'''
@auth.get_password
def get_password(username):
    if username == 'zjh':
        return 'zjhzjh'
    return None

@auth.error_handler
def unauthorized():
    return make_response(jsonify({'error': 'Unauthorized Access'}),401)
'''
@app.route('/', methods=['GET'])
def get_proxy():
    getproxys()
    proxy = list(random.choice(proxys, 1))
    return jsonify({'proxys':proxy})

@app.route('/proxy', methods=['GET'])
def get_proxy2():
    getproxys()
    proxy = list(random.choice(proxys, 1))
    return jsonify({'proxys':proxy})


@app.route('/proxys', methods=['GET'])
def get_proxys():
    getproxys()
    return jsonify({'proxys':proxys})

@app.route('/proxys/<int:num>', methods=['GET'])
def get_proxys_num(num):
    getproxys()
    if len(proxys) < num:
        abort(404)
    proxy_num = list(random.choice(proxys, num))
    return jsonify({'proxys':proxy_num})

@app.errorhandler(404)
def not_found(error):
    getproxys()
    return make_response(jsonify({'error':'No more proxy !'}), 404)

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5000)
