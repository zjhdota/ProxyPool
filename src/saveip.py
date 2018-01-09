
import requests
#import pymongo
import redis
import os
import datetime
import re
import time
import subprocess
from lxml import etree
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
    def get_xici(self, source="www.xicidaili.com"):
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
            self.dit["source"] = source
            yield self.dit

    # 快代理
    def get_kuaidaili(self, source="www.kuaidaili.com"):
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
            self.dit["source"] = source
            yield self.dit

    #ip181
    def get_ip181(self, source="www.ip181.com"):
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
            self.dit["source"] = source
            yield self.dit

    #66代理
    def get_66(self, source="www.66ip.cn"):
        http_proxy_list = []
        https_proxy_list = []
        http_url = 'http://www.66ip.cn/nmtq.php?getnum=1000&isp=0&anonymoustype=0&start=&ports=&export=&ipaddress=&area=0&proxytype=0&api=66ip'
        https_url = 'http://www.66ip.cn/nmtq.php?getnum=1000&isp=0&anonymoustype=0&start=&ports=&export=&ipaddress=&area=0&proxytype=1&api=66ip'
        html = requests.get(http_url)
        selector = etree.HTML(html.text)
        http_proxys = selector.xpath('/html/body/text()')
        del http_proxys[0]
        for http_proxy in http_proxys:
            http_proxy = re.sub(r'\r\n\t ]*','',http_proxy).strip()
            http_proxy_list.append(http_proxy)
        http_proxy_list = [http for http in http_proxy_list if http != '']
        for http_proxy in http_proxy_list:
            ip = http_proxy[:http_proxy.find(':'):]
            port = http_proxy[http_proxy.find(':')+1:]
            proxy_type = 'http'
            lastcheck = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            self.ip_list.append(ip)
            self.port_list.append(port)
            self.type_list.append(proxy_type)
            self.lastcheck_list.append(lastcheck)


        time.sleep(5)
        html = requests.get(https_url)
        selector = etree.HTML(html.text)
        https_proxys = selector.xpath('/html/body/text()')
        del https_proxys[0]
        for https_proxy in https_proxys:
            https_proxy = re.sub(r'[\r\n\t ]*','',https_proxy)
            https_proxy_list.append(https_proxy)
        https_proxy_list = [https for https in https_proxy_list if https != '']
        for https_proxy in https_proxy_list:
            ip = https_proxy[:https_proxy.find(':')]
            port = https_proxy[https_proxy.find(':')+1:]
            proxy_type = 'https'
            lastcheck = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            self.ip_list.append(ip)
            self.port_list.append(port)
            self.type_list.append(proxy_type)
            self.lastcheck_list.append(lastcheck)

        for ip,port,tp,lastcheck in zip(self.ip_list, self.port_list, self.type_list, self.lastcheck_list):
            self.dit['ip'] = ip
            self.dit['port'] = port
            self.dit['type'] = tp
            self.dit['lastcheck'] = lastcheck
            self.dit["source"] = source
            yield self.dit

    #89ip
    def get_89ip(self, source="www.89ip.cn"):
        proxy_list = []
        url = 'http://www.89ip.cn/tiqv.php?sxb=&tqsl=2000&ports=&ktip=&xl=on&submit=%CC%E1++%C8%A1'
        html = requests.get(url)
        selector = etree.HTML(html.text)
        for i in range(2,2001):
            proxy = selector.xpath("/html/body/div/text()["+str(i)+"]")
            if proxy != [] and 'ip3366.net' not in proxy[0]:
                proxy = re.sub(r'[\n\r ]*','',proxy[0])
                proxy_list.append(proxy)
        proxy_list = [proxy for proxy in proxy_list if proxy != '']
        #print(proxy_list)
        for proxy in proxy_list:
            ip = proxy[:proxy.find(':')]
            port = proxy[proxy.find(':')+1:]
            proxy_type = 'http'
            lastcheck = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            self.ip_list.append(ip)
            self.port_list.append(port)
            self.type_list.append(proxy_type)
            self.lastcheck_list.append(lastcheck)

        for ip,port,tp,lastcheck in zip(self.ip_list, self.port_list, self.type_list, self.lastcheck_list):
            self.dit['ip'] = ip
            self.dit['port'] = port
            self.dit['type'] = tp
            self.dit['lastcheck'] = lastcheck
            self.dit["source"] = source
            yield self.dit

    def save(self, data):
        #db = pymongo.MongoClient(host='127.0.0.1', port='27017')
        db = redis.Redis(host='127.0.0.1', port=6379, db=0)
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
    p4 = Saveip()
    daili66_dit = p4.get_66()
    for data in daili66_dit:
        p4.save(data)
    #p5 = Saveip()
    #daili89_dit = p5.get_89ip()
    #for data in daili89_dit:
        #p5.save(data)
    #os.popen('python ./checkip.py')
    subprocess.Popen("python ./checkip.py",shell=True)
