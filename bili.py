#!/usr/bin/python
# -*- coding = utf-8 -*-

import os
import re
import time
import subprocess
import requests
import random

def LoadUserAgents(uafile):
    uas = []
    with open(uafile, 'rb') as uaf:
        for ua in uaf.readlines():
            if ua:
                uas.append(ua.strip()[:-1])
    random.shuffle(uas)
    return uas

uas = LoadUserAgents("user_agents.txt")

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
def save(text):
      path = os.path.join('regex', 'bili-view')
      with open(path, 'a+') as f:
           f.write(text)       

def record(av):
      path4history = os.path.join('regex', 'bili-his')
      with open(path4history, 'a+') as history:
           history.write(str(av))

def visit(url):
      ID = 0
      for aid in range(10058254,11000000):
          try:
              res = requests.get(url + str(aid) + '.html', headers = newheader())
              page = res.content
              re4title = r'(?<="title" content=").*(?=">\n<meta name="keywords")'
              title = re.findall(re4title, page, re.S|re.M)
              re4all = r'(?<="stat":\{"aid":).*(?=,"danmaku")'
              result = re.findall(re4all, page, re.S|re.M)
              if result:
                   re4view = r'(?<="view":).*'
                   view = re.findall(re4view, result[0], re.S|re.M)
                   if int(view[0]) >= 100000:
                          string = 'Video ID:' + str(aid) + '\n' + 'Title:' + title[0] +'\n' + 'View:' + view[0] + '\n\n'
                          save(string)
                          if(aid - ID > 100):
                             record(aid)
                             ID = aid
                          print '\n\nNew Specific Video Found!'
                          print string
                   else:
                          print 'Video ID:' + str(aid) + ' is not specific.'
              else:
                    print 'Video ID:' + str(aid) + ' has been deleted.'
              time.sleep(0.233)
          except (requests.exceptions.ChunkedEncodingError, requests.ConnectionError) as e:
              print 'an error occurred.'

if __name__ == '__main__':
      visit('https://m.bilibili.com/video/av')
