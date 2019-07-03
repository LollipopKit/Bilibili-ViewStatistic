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
def save(av, title, count):
      con = sqlite3.connect('regex/bili.db')
      cur = con.cursor()
      cur.execute('INSERT INTO view VALUES (%d,"%s",%d)'%(av, title, count))
      con.commit()
      con.close()    

def record(av):
      path4history = os.path.join('regex', 'bili-his')
      with open(path4history, 'w') as history:
           history.write(str(av))

def get():
    first = linecache.getline('regex/bili-his', 1)
    if first:
       return int(first) + 1
    else:
       return 1

start = get()

def visit(url):     
      for aid in range(start,100000):
          try:
              res = requests.get(url + str(aid) + '.html', headers = newheader())
              page = res.content
              page = page.decode('utf-8')
              re4title = r'(?<="title" content=").*(?=">\n<meta name="keywords")'
              title = re.findall(re4title, page, re.S|re.M)
              re4all = r'(?<="stat":\{"aid":).*(?=,"danmaku")'
              result = re.findall(re4all, page, re.S|re.M)
              if result:
                   record(aid)
                   re4view = r'(?<="view":).*'
                   view = re.findall(re4view, result[0], re.S|re.M)
                   if int(view[0]) >= 100000:
                          save(aid, title[0], int(view[0]))
                          print('\n\n' + 'AV:' + str(aid) + '\n' + 'Title:' + title[0] + '\n' + 'Count:' + view [0] + '\n\n')
                   else:
                          print('AV:' + str(aid) + ' is not specific.')
              else:
                    print('AV:' + str(aid) + ' has been deleted.')
              time.sleep(0.233)
          except (requests.exceptions.ChunkedEncodingError, requests.ConnectionError) as e:
              print('an error occurred.')

if __name__ == '__main__':
      visit('https://m.bilibili.com/video/av')
