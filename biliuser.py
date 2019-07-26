#!/usr/bin/python
# -*- coding = utf-8 -*-

import os
import re
import time
import subprocess
import requests
import random
import sqlite3
import linecache
import json

def loadUserAgents(uafile):
    uas = []
    with open(uafile, 'rb') as uaf:
        for ua in uaf.readlines():
            if ua:
                uas.append(ua.strip()[:-1])
    random.shuffle(uas)
    return uas

uas = loadUserAgents("user_agents.txt")

def newheader():
    head = {
       'Host': 'm.bilibili.com',
       'Connection': 'close',
       'User-Agent': random.choice(uas),
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
       'Accept-Encoding': 'gzip, deflate',
       'Accept-Language': 'zh-CN,zh;q=0.8'
    }
    return head
def save(uid, name, sub, fan):
      con = sqlite3.connect('regex/bili.db')
      cur = con.cursor()
      cur.execute('INSERT INTO user VALUES (%d,"%s",%d,%d)'%(uid, name, sub, fan))
      con.commit()
      con.close()    

def record(av):
      path4history = os.path.join('regex', 'bili-user-his')
      with open(path4history, 'w') as history:
           history.write(str(av))

def convert(fanstr):
    if '万' in fanstr:
       fanstr = fanstr.replace('万', '')
       fanint = int(int(fanstr)*10000)
       return fanint
    else:
       return int(fanstr)

def get():
    first = linecache.getline('regex/bili-user-his', 1)
    if first:
       return int(first) + 1
    else:
       return 1

start = get()

def visit(url):     
      for userid in range(start,1000000):
          try:
              res = requests.get(url + str(userid), headers = newheader())
              page = res.content
              page = page.decode('utf-8')
              re4name = r'(?<=title>).*(?=的个人空间-哔哩哔哩移动版</title>)'
              name = re.findall(re4name, page, re.S|re.M)
              if name:
                   record(userid)
                   res4fan = requests.get('https://api.bilibili.com/x/relation/stat?vmid=' + str(userid) + '&jsonp=jsonp')
                   page4fan = res4fan.content.decode('utf-8')
                   jsFan = json.loads(page4fan)
                   fan = jsFan['data']['follower']
                   subscribe = jsFan['data']['following']
                   if fan >= 500000:
                          save(userid, name[0], subscribe, fan)
                          print('\n\n' + 'User:' + str(userid) + '\n' + 'Title:' + name[0] + '\n' + 'Count:' + str(fan) + '\n\n')
                   else:
                          print('User:' + str(userid) + ' is not specific.')
              else:
                    print('User:' + str(userid) + ' has been deleted.')
              time.sleep(0.233)
          except (requests.exceptions.ChunkedEncodingError, requests.ConnectionError) as e:
              print('an error occurred.')

if __name__ == '__main__':
      visit('https://m.bilibili.com/space/')
