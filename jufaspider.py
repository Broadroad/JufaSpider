# -*- coding: utf-8 -*-
#from __future__ import unicode_literals
import requests
import datetime
import json
import sys
import re

reload(sys)
sys.setdefaultencoding( "utf-8" )

LOGIN_URL = "https://www.jufaanli.com/home/User/login"
SEARCH_URL = "https://www.jufaanli.com/home/search/searchJson"
s = requests.Session()
s.get("https://www.jufaanli.com/")

def Login():
    payload = {'user' : '13162502908', 'password' : PASSWORD}
    r = s.post(LOGIN_URL, data=payload)
    print r.text 

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
        print r.encode('utf-8') 

#Login()
#Search()

ids = {}
first = []
second = []
again = []
again1 = []
def handleData():
    with open('test', 'r') as f:
        lines = json.load(f)
        a = json.dumps(lines, ensure_ascii=False, indent=4)
        with open('result', 'w+') as ff:
            ff.write(a)
        #print json.dumps(lines, ensure_ascii=False)

def readData():
    with open('result', 'r') as f:
        res = json.load(f)
        #a = json.dumps(lines, ensure_ascii=False, indent=4)
        all = res['info']['searchList']['list']
        for k in all:
            ids[k['id']] = k
            #print k['id']

            labels = k['label']
            for l in labels:
                if (l == '一审'):
                    #print "一审 是 " + k['id']
                    first.append(k['id'])
                elif (l == '二审'):
                    second.append(k['id'])
                    #print "二审 是 " + k['id']
                elif (l == '再审审查与审判监督'):
                    again.append(k['id'])
                    print "再审审查 是 " + k['id']
                elif (l == "再审"):
                    again1.append(k['id'])
                    print "再审 是 " + k['id']
        print len(ids)
        print len(first)
        print len(second)
        print len(again)
        print len(again1)
readData()

ans = []
visited = {}
def analysisAgain():
    for v in again:
        if (visited.has_key(v)):
            continue
        visited[v] = True

        item = ids[v]
        result = item['tab_list']

        flag = 1 # 1 - 驳回 2 - 提审
        related_case = item['relate_case']
        for key in result:
            #print key['裁判结果']
            for kk in key:
                if (kk == '裁判结果'):
                    #print key[kk] + "end"
                    if ('提审' in key[kk]):
                        flag = 2
                    elif ('驳回' in key[kk]):
                        flag = 1
        if (flag == 1):
            pass
        elif (flag == 2):
            for case in related_case:
                visited[case['case_id']] = True
            ans.append(v)

def analysisAgain1():
    for v in again1:
        if (visited.has_key(v)):
            continue
        visited[v] = True

        item = ids[v]
        result = item['tab_list']

        flag = 1 # 1 - 驳回 2 - 提审
        related_case = item['relate_case']
        for key in result:
            #print key['裁判结果']
            for kk in key:
                if (kk == '裁判结果'):
                    #print key[kk] + "end"
                    if ('提审' in key[kk]):
                        flag = 2
                    elif ('驳回' in key[kk]):
                        flag = 1
                    elif ('准许' in key[kk]):
                        flag = 1
                    elif ('撤销' in key[kk]):
                        flag = 1
        if (flag == 1):
            pass
        elif (flag == 2):
            for case in related_case:
                visited[case['case_id']] = True
            ans.append(v)

def analysisSecond():
    cnt = 0
    print 'before second'
    print len(visited)
    for v in second:
        if (visited.has_key(v)):
            continue
        visited[v] = True

        item = ids[v]
        result = item['tab_list']

        flag = 1 # 1 - 驳回 2 - 提审
        related_case = item['relate_case']
        for key in result:
            #print key['裁判结果']
            for kk in key:
                if (kk == '裁判结果'):
                    if ('维持原判' in key[kk] or '维持原裁定' in key[kk]):
                        flag = 2
                    else:
                        #print key[kk] + "end"
                        flag = 1

        if (flag == 2):
            pass
        elif (flag == 1):
            if (len(related_case) == 0):
                handle_empty_related_case(v)
            for case in related_case:
                visited[case['case_id']] = True
            ans.append(v)
    print cnt, len(second), len(visited)

def handle_empty_related_case(v):
    item = ids[v]
    result = item['tab_list']
    pro = re.compile(u'\d{4}号')

    for key in result:
        #print key['裁判结果']
        for kk in key:
            if (kk == '裁判结果'):
                a = pro.search(key[kk])
                if (a != None):
                    for vv in ids:
                        if(a.group() in ids[vv]['num']):
                            print vv
                            visited[ids[vv]['id']] = True

def analysisFirst():
    cnt = 0
    print "first has ", len(first)
    for v in first:
        if (visited.has_key(v)):
            continue
        visited[v] = True
        item = ids[v]
        result = item['tab_list']

        flag = 1 # 1 - 驳回 2 - 提审
        related_case = item['relate_case']
        for key in result:
            #print key['裁判结果']
            for kk in key:
                if (kk == '裁判结果'):
                    #print key[kk] + "end"
                    if ('撤诉' in key[kk] or '撤回起诉' in key[kk]):
                        print key[kk] + "end"
                        flag = 2
                    else:
                        flag = 1

        if (flag == 2):
            cnt = cnt + 1
            pass
        elif (flag == 1):
            for case in related_case:
                visited[case['case_id']] = True
            ans.append(v)
    print '驳回 cnt is ', cnt
#analysisAgain()
print 'after again -----------'
print len(visited)

#analysisAgain1()
print 'after again1 -----------'
print len(visited)

#analysisSecond()
print 'after second ------------'
print len(visited)

analysisFirst()
