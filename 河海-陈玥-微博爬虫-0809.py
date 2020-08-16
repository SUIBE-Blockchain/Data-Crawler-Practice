Python 3.8.3 (tags/v3.8.3:6f8c832, May 13 2020, 22:20:19) [MSC v.1925 32 bit (Intel)] on win32
Type "help", "copyright", "credits" or "license()" for more information.
>>> import requests
import json
url="https://m.weibo.cn/api/container/getIndex?type=uid&value=2656274875&containerid=1076032656274875"
content_list=[]
response=requests.get(url)       
content=json.loads(response.text)
cards=content['data']['cards']
since_id=content['data']['cardlistInfo']['since_id']
for c in cards:
    if c['card_type']==9:
        temp={}
        temp['created_at']=c['mblog']['created_at']
        temp['raw_text']=c['mblog']['raw_text']
        content_list.append(temp)
        

next_url="https://m.weibo.cn/api/container/getIndex?type=uid&value=2656274875&containerid=1076032656274875&since_id={}".format(since_id)
for i in range(10): 
    if i<10:
        response=requests.get(next_url)       
        content=json.loads(response.text)
        cards=content['data']['cards']
        since_id=content['data']['cardlistInfo']['since_id']
        for c in cards:
            if c['card_type']==9:
                temp={}
                temp['created_at']=c['mblog']['created_at']
                temp['raw_text']=c['mblog']['raw_text']
                next_url="https://m.weibo.cn/api/container/getIndex?type=uid&value=2656274875&containerid=1076032656274875&since_id={}".format(since_id)
                content_list.append(temp)
                i=i+1
print(content_list)