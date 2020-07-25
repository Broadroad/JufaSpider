# -*- coding: utf-8 -*-
#from __future__ import unicode_literals
import requests
import datetime
import json

import sys
import importlib

import sys
import io
sys.stdout = io.TextIOWrapper(buffer=sys.stdout.buffer,encoding='utf8')

dict = {'Title': '这是标题'}
dic = json.dumps(dict, ensure_ascii = False)
print(dic)
#print(json.dumps(dict))
print("哈哈")
print(u'哈哈'.encode('utf-8'))

type = sys.stdout.encoding
print(type)
print('你好'.encode('utf-8').decode(type))

LOGIN_URL = "https://www.jufaanli.com/home/User/login"
SEARCH_URL = "https://www.jufaanli.com/home/search/searchJson"
PASSWORD = "zxcvbnm123"
s = requests.Session()
s.get("https://www.jufaanli.com/")

def Login():
    payload = {'user' : '13162502908', 'password' : PASSWORD}
    r = s.post(LOGIN_URL, data=payload)
    print(r.text)

def Search():
    payload = {'page' : 1, 'searchTime' : datetime.datetime.now(), 
                'searchNum' : 20, 'nowReason' : 0, 
                'sortType' : 'caseWeight', 
                'keyword' : '机构：南京市第十建筑工程有限公司',
                'TypeKey' : '1:机构：南京市第十建筑工程有限公司',
                'focus_name': '案例搜索：机构：南京市第十建筑工程有限公司', 'signType' : 2}
    r = s.post(SEARCH_URL, data=payload).text
    with open('test','w',encoding='utf-8') as f:
        f.write(r)
        print(r.encode('utf-8'))

#Login()
#Search()
print(json.dumps({'text':'你好'}))

with open('test', 'r', encoding='utf-8') as f:
    lines = json.load(f)
    #print(json.dumps(lines, ensure_ascii=False, indent=4))

