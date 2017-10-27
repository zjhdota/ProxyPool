# -*- encoding: utf-8 -*-
import redis
import requests
import random

db = redis.Redis(host='127.0.0.1', port=6379, db=0)
hash_name_list = [num.decode('ascii') for num in db.keys('*')]
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'
}
def get_proxy():
    for hash_name in hash_name_list:
        ip = db.hget(hash_name, 'ip').decode('ascii')
        port = db.hget(hash_name, 'port').decode('ascii')
        tp = db.hget(hash_name, 'type').decode('ascii').lower()
        tag = db.hget(hash_name, 'tag').decode('ascii')
        if tag == '1':
            proxy = {
                tp: tp+'://'+ip+':'+port,
            }
            yield proxy

def check_ip():
    proxy_list = []
    for proxy in get_proxy():
        #print([value for value in proxy.values()][0])
        ip = [value for value in proxy.values()][0]
        ip = ip[ip.find('//')+2:ip.rfind(':')]
        #print(ip)
        try:
            html = requests.get('http://www.baidu.com', headers=headers, proxies=proxy, timeout=2)
        except:
            db.hset(ip, 'tag', 0)
        else:
            proxy_list.append(proxy)
    return proxy_list

def get_ip():
    proxy_list = check_ip()
    proxy = random.choice(proxy_list)
    return proxy

