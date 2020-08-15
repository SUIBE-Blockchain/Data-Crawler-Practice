import requests
import json#通过json获取具体的信息
from w3lib.html import remove_tags#去除标签
base_url='https://m.weibo.cn/api/container/getIndex?type=uid&value=1938208221&containerid=1076031938208221&since_id=4535018657424704'
for i in range(2805):
    url=base_url.format(i+1)
    print(url)
    response = requests.get(url)
    res_dict = json.loads(response.text)
    cards = res_dict['data']['cards']
    for card in cards:
        if 'mblog' in card:
            text =remove_tags( card['mblog']['text'])
            print(text)
            print('-' * 50)
