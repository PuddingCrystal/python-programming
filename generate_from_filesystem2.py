from jinja2 import Environment, FileSystemLoader
import os
import requests
import html
from urllib import parse
import webbrowser
import json
from collections import defaultdict

root = os.path.dirname(os.path.abspath(__file__))
path = root +'\\templates'
path2 = root +'\\html'
if not os.path.isdir(path):
  os.mkdir(path)
if not os.path.isdir(path2):
  os.mkdir(path2)

templates_dir = os.path.join(root, 'templates')
env = Environment( loader = FileSystemLoader(templates_dir) )

GEN_HTML =  os.path.join(root, 'templates', 'index.html')  #命名生成的html
f = open(GEN_HTML,'w',encoding="utf-8")

message = """
<html>
<head></head>
<body>
<style>
    body{
        font-size:18px;
       margin-block-start: 0.93em;
        margin-block-end: 0.93em;
        color:#423d3df7;
        font-family:"PingFang TC","Noto Sans TC","sans-serif","STHeitiTC-Light",Arial,sans-serif
    }
    span{
        font-size:12px;
        color:#423d3df7;
    }
    h4 {
        display: block;
        margin-block-start: 0.93em;
        margin-block-end: 0.93em;
        margin-inline-start: 0px;
        margin-inline-end: 0px;
        font-weight: normal;
    }
</style>
<p>https://www.fetnet.net/content/cbu/tw/promotion.html</p>
<p></p>
    <ol>
    {% for result in results %}  
        <li> <a href="{{ result.link }}">{{ result.title }}</a> | Tag:<span>{{ result.tagID }}</span></li>
    {% endfor %}
    </ol>
</body>
</html>"""
f.write(message)
f.close()

https_proxy = "http://username:password@fetfw.fareastone.com.tw:8080"
proxyDict = {"https" : https_proxy}

tag_sources = "https://www.fetnet.net/bin/promotion/getTagList?tagPath=%2Fcontent%2Fcq%3Atags%2Fcbu%2Fpromotions"
tag_list = []
payload = requests.get(tag_sources,  proxies = proxyDict).json()['result']['content']
#payload[2].setdefault('content')

print(len(payload))

i=0
for i in  range(len(payload)):
  payload[i].setdefault('content', None)

print(payload)

#payload = payload.setdefault('content')
#payload = json.loads(obj)
for activity in payload:
   # payload[activity].setdefault('content')
    tag_id = activity["id"]
    #a  = payload.setdefault(activity['content'])
    #print(tag_id)
    if activity["content"] is not None:
      contents  = activity["content"]
      for content in contents:
          content_id = content['id']
          tag_list.append("https://www.fetnet.net/bin/promotion/promotionDetail?tagId="+content_id+"&limit=1000&offset=0") 
          print('got response from in {}'.format(content_id)) 
    print('got response from out {}'.format(tag_id)) 
    tag_list.append("https://www.fetnet.net/bin/promotion/promotionDetail?tagId="+tag_id+"&limit=1000&offset=0") 

result = []
tagIDA = []
my_responses = [] 
for link in tag_list: 
    payload = requests.get(link,  proxies = proxyDict).json()["result"] 
    for activity in payload:
        title = html.unescape(activity["title"])  #解碼 html.unescape('str')
        link = activity["link"]
        tagID = activity["tagId"]
        result.append(dict(title=title, link=link, tagID=tagID))


template = env.get_template('index.html')
filename = os.path.join(root, 'html', 'index.html')
with open(filename, 'w',encoding="utf-8") as fh:
    fh.write(template.render(
        results    =  result
    ))
fh.close()

webbrowser.open(filename,new = 1)