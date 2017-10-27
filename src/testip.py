# -*- encoding: utf-8 -*-

import requests
import getip
headers ={
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'
}
html = requests.get('http://www.baidu.com', proxies=getip.get_ip(), headers=headers, timeout=2)
print(html.status_code)
