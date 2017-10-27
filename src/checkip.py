# -*- encoding: utf-8 -*-
import threading
from queue import Queue
import redis
import requests
import time
import logging
import datetime
from dateutil import rrule
from dateutil import parser

class MyThread(threading.Thread):
    def __init__(self, queue):
        threading.Thread.__init__(self)
        self.queue = queue

    def run(self):
        checking(self.queue)

def checking(queue):
    while True:
        try:
            hash_name = queue.get(block=True, timeout=1)
        except:
            break
        tag = db.hget(hash_name, 'tag').decode('ascii')
        ip = db.hget(hash_name, 'ip').decode('ascii')
        port = db.hget(hash_name, 'port').decode('ascii')
        tp = db.hget(hash_name, 'type').decode('ascii').lower()
        lastcheck = db.hget(hash_name, 'lastcheck').decode('ascii')
        logging.info('start checking {}://{}:{} ...'.format(tp, ip, port))
        headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'
        }
        proxies = {
            tp: tp+'://'+ip+':'+port,
        }
        try:
            html = requests.get('http://www.baidu.com/', proxies=proxies, headers=headers, timeout=2)
        except Exception as e:
            logging.info("{}://{}:{},{}".format(tp, ip, port, e))
            db.hset(hash_name, 'tag', 0)
            if rrule.rrule(rrule.DAILY, dtstart=parser.parse(lastcheck), until=datetime.datetime.now()).count() > 7:
                db.delete(hash_name)
        else:
            db.hset(hash_name, 'tag', 1)
            logging.info('{}://{}:{} , HTTP state code: {}'.format(tp, ip, port, html.status_code))
        time.sleep(5)
        queue.task_done()

logging.basicConfig(level=logging.INFO,
                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                datefmt='%a, %d %b %Y %H:%M:%S',
                filename='checkip.log',
                filemode='a+')

console = logging.StreamHandler()
console.setLevel(logging.INFO)
formatter = logging.Formatter('%(name)-8s: %(levelname)-8s %(message)s')
console.setFormatter(formatter)
logging.getLogger('').addHandler(console)

db = redis.Redis(host='127.0.0.1', port=6379, db=0)
hash_name_list = [num.decode('ascii') for num in db.keys('*')]
queue = Queue(len(hash_name_list))
#print(len(hash_name_list))
threads = []
for i in range(5):
    t = MyThread(queue)
    threads.append(t)
    t.setDaemon(True)
    t.start()
if hash_name_list:
    for hash_name in hash_name_list:
        queue.put(hash_name)
    queue.join()

for t in threads:
    t.join()

logging.info('checking complete...')
