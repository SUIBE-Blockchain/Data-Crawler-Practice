import requests
import json
import pymysql

class Spider:
    def __init__(self):
        self.flag = True
        self.url = 'https://m.weibo.cn/api/container/getIndex?is_all[]=1%3Fis_all%3D1&is_all[]=1&jumpfrom=weibocom&type=uid&value=3604378011&containerid=1076033604378011'
        self.headers = {
             "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Mobile Safari/537.36"
            }

    def parse_url(self, url): 
        response = requests.get(url,self.headers)
        html_str = response.content.decode()
        return html_str

    def get_content_list(self, html_str):
        res_dict = json.loads(html_str)
        if res_dict['ok'] != 1:
            self.flag = False
        since_id = res_dict['data']['cardlistInfo']['since_id']
        cards = res_dict['data']['cards']
        content_list = []
        for card in cards:
            if card['card_type'] == 9:
                text = card['mblog']['text']
                content_list.append(text)

        next_url = "https://m.weibo.cn/api/container/getIndex?is_all[]=1%3Fis_all%3D1&is_all[]=1&jumpfrom=weibocom&type=uid&value=3604378011&containerid=1076033604378011&since_id={}".format(since_id)
        return content_list,next_url

    def run(self):
        content = []
        while self.flag:
            html_str = self.parse_url(self.url)
            content_list,next_url = self.get_content_list(html_str)
            self.url = next_url
            content.extend(content_list)
            print(content,'\n')
           



if __name__ == "__main__":
    weibo = Spider()
    weibo.run()
