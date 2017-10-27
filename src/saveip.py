from lxml import etree
import requests
#import pymongo
import redis
import os

class Saveip(object):
    def __init__(self,):
        self.session = requests.Session()
        self.session.headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.91 Safari/537.36',
        }
        self.dit = {
            "ip": '',
            "port": '',
            "type": '',
            "lastcheck": '',
            "tag": 1,
        }
        self.url = []
        self.ip_list = []
        self.port_list = []
        self.type_list = []
        self.lastcheck_list = []
        self.crawl_queue = []

    # 西刺代理
    def get_xici(self):
        for n in range(1,3):
            url = 'http://www.xicidaili.com/nn/' + str(n)
            self.url.append(url)
        self.crawl_queue.extend(self.url)
        while self.crawl_queue:
            url = self.crawl_queue.pop()
            try:
                html = self.session.get(url)
            except:
                #self.crawl_queue.append(url)
                print('西刺代理: {}网址暂时不可用'.format(url))
            else:
                selector = etree.HTML(html.text)
                for i in range(2, 102):
                    ip = selector.xpath('//*[@id="ip_list"]/tr['+str(i)+']/td[2]/text()')[0]
                    self.ip_list.append(ip)
                    port = selector.xpath('//*[@id="ip_list"]/tr['+str(i)+']/td[3]/text()')[0]
                    self.port_list.append(port)
                    tp = selector.xpath('//*[@id="ip_list"]/tr['+str(i)+']/td[6]/text()')[0]
                    self.type_list.append(tp)
                    lastcheck = selector.xpath('//*[@id="ip_list"]/tr['+str(i)+']/td[10]/text()')[0]
                    self.lastcheck_list.append(lastcheck)

        for ip,port,tp,lastcheck in zip(self.ip_list, self.port_list, self.type_list, self.lastcheck_list):
            self.dit["ip"] = ip
            self.dit["port"] = port
            self.dit["type"] = tp
            self.dit["lastcheck"] = '20' + lastcheck
            yield self.dit

    # 快代理
    def get_kuaidaili(self):
        for n in range(1, 3):
            self.url.append('http://www.kuaidaili.com/free/inha/'+str(n)+'/')
        self.crawl_queue.extend(self.url)
        while self.crawl_queue:
            url = self.crawl_queue.pop()
            try:
                html = self.session.get(url)
                if html.status_code == 503:
                    continue
            except:
                #self.crawl_queue.append(url)
                print('快代理: {}网址暂时不可用'.format(url))
            else:
                selector = etree.HTML(html.text)
                for i in range(1, 16):
                    ip = selector.xpath('//*[@id="list"]/table/tbody/tr['+str(i)+']/td[1]/text()')[0]
                    #print(ip)
                    self.ip_list.append(ip)
                    port = selector.xpath('//*[@id="list"]/table/tbody/tr['+str(i)+']/td[2]/text()')[0]
                    self.port_list.append(port)
                    tp = selector.xpath('//*[@id="list"]/table/tbody/tr['+str(i)+']/td[4]/text()')[0]
                    self.type_list.append(tp)
                    lastcheck = selector.xpath('//*[@id="list"]/table/tbody/tr['+str(i)+']/td[7]/text()')[0]
                    self.lastcheck_list.append(lastcheck)

        for ip,port,tp,lastcheck in zip(self.ip_list, self.port_list, self.type_list, self.lastcheck_list):
            self.dit['ip'] = ip
            self.dit['port'] = port
            self.dit['type'] = tp
            self.dit['lastcheck'] = lastcheck
            yield self.dit

    #ip181
    def get_ip181(self):
        for n in range(1, 3):
            self.url.append('http://www.ip181.com/daili/'+str(n)+'.html')
        self.crawl_queue.extend(self.url)
        while self.crawl_queue:
            url = self.crawl_queue.pop()
            try:
                html = self.session.get(url)
                html.encoding = 'gb2312'
            except:
                #self.crawl_queue.append(url)
                print('ip181: {}网址暂时不可用'.format(url))
            else:
                selector = etree.HTML(html.text)
                for i in range(2, 102):
                    level = selector.xpath('/html/body/div[2]/div/div[2]/div/div[3]/table/tbody/tr['+str(i)+']/td[3]/text()')[0]
                    if level != '高匿':
                        continue
                    ip = selector.xpath('/html/body/div[2]/div/div[2]/div/div[3]/table/tbody/tr['+str(i)+']/td[1]/text()')[0]
                    #print(ip)
                    self.ip_list.append(ip)
                    port = selector.xpath('/html/body/div[2]/div/div[2]/div/div[3]/table/tbody/tr['+str(i)+']/td[2]/text()')[0]
                    self.port_list.append(port)
                    tp = selector.xpath('/html/body/div[2]/div/div[2]/div/div[3]/table/tbody/tr['+str(i)+']/td[4]/text()')[0]
                    if tp.find('HTPPS'):
                        tp = tp[tp.find(',')+1:]
                    self.type_list.append(tp)
                    lastcheck = selector.xpath('/html/body/div[2]/div/div[2]/div/div[3]/table/tbody/tr['+str(i)+']/td[7]/text()')[0]
                    self.lastcheck_list.append(lastcheck)

        for ip,port,tp,lastcheck in zip(self.ip_list, self.port_list, self.type_list, self.lastcheck_list):
            self.dit['ip'] = ip
            self.dit['port'] = port
            self.dit['type'] = tp
            self.dit['lastcheck'] = lastcheck
            yield self.dit

    def save(self, data):
        #db = pymongo.MongoClient(host='127.0.0.1', port='27017')
        db = redis.Redis(host='127.0.0.1', port='6379', db=0)
        #for k,v in self.dit.items():
        db.hmset(data['ip'], data)

if __name__ == '__main__':
    p = Saveip()
    xici_dit = p.get_xici()
    for data in xici_dit:
        p.save(data)
    p2 = Saveip()
    kuai_dit = p2.get_kuaidaili()
    for data in kuai_dit:
        p2.save(data)
    p3 = Saveip()
    ip181_dit = p3.get_ip181()
    for data in ip181_dit:
        p3.save(data)

    os.popen('python ./checkip.py')
