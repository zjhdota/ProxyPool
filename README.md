# ProxyPool
## 概述 ##
一个简易的IP池，主要用来抓取高匿HTTP或HTTPS类型的免费代理。

## 免费代理来源 ##
+ [西刺代理](http://www.xicidaili.com/)
+ [快代理](http://www.kuaidaili.com/free/)
+ [ip181](http://www.ip181.com/)
+ [66代理](http://www.66ip.cn/nm.html)
+ [89ip](http://www.89ip.cn/)
+ [开心代理](http://www.kxdaili.com/)
+ [ip3366代理](http://www.ip3366.net/)

## 运行环境 ##
+ [Python3.x](https://www.python.org/)
+ [Redis](https://redis.io/)

## 第三方库 ##
+ [redis 2.10.6](https://pypi.python.org/pypi/redis)
+ [requests 2.18.4](https://pypi.python.org/pypi/requests)
+ [python-dateutil 2.6.1](https://pypi.python.org/pypi/python-dateutil)

## 文件说明 ##
+ [saveip.py](src/saveip.py): 用来请求网页并存储代理信息到Redis
+ [checkip.py](src/checkip.py): 用来检测Redis中的代理是否有效
+ [getip.py](src/getip.py): 用来获取Redis中可用的代理
+ [proxy_rest_api.py](src/proxy_rest_api.py): 用来获取代理的API文件
+ [testip.py](src/testip.py): 测试文件

## 使用方法 ##
+ 可以将saveip.py和checkip.py两个脚本加入到定时任务(推荐)

+ 调用getip.py中的get_ip()方法，来返回一个随机可用的代理
```
import requests
import getip
headers ={
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'
}
html = requests.get('http://www.baidu.com', proxies=getip.get_ip(), headers=headers, timeout=2)
print(html.status_code)
```

## api接口 ##
用flask写了个RESTful api用于获取代理信息

1. 返还随机一个可用的代理信息
```
GET http://127.0.0.1:5000
```
或者
```
GET http://127.0.0.1:5000/proxy
```
2. 返还随机一个可用的http代理信息
```
GET http://127.0.0.1:5000/proxy/http
```
3. 返还随机一个可用的https代理信息
```
GET http://127.0.0.1:5000/proxy/https
```
4. 返还所有可用的代理信息
```
GET http://127.0.0.1:5000/proxys
```
5. 返还所有可用的http代理信息
```
GET http://127.0.0.1:5000/proxys/http
```
6. 返还所有可用的https代理信息
```
GET http://127.0.0.1:5000/proxys/https
```
7. 随机返还num数量的可用代理信息
```
GET http://127.0.0.1:5000/proxys/<int:num>
```
8. 随机返还num数量的可用的http代理信息
```
GET http://127.0.0.1:5000/proxys/http/<int:num>
```
9. 随机返还num数量的可用的https代理信息
```
GET http://127.0.0.1:5000/proxys/https/<int:num>
```
