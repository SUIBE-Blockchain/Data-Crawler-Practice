import requests
import json

class Spider:
    def __init__(self):
        self.flag=True
        self.url_temp=('https://m.weibo.cn/api/container/getIndex?sudaref=login.sina.com.cn&display=0&retcode=6102&type=uid&value=1784473157&containerid=1076031784473157')
        self.headers={
'User-Agent':'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Mobile Safari/537.36'
}

    def parse_url(self,url):
        response = requests.get(url, self.headers)
        html_str = response.content
        return html_str





    def get_content_list(self,html_str):
        content = json.loads(html_str)
        if content['ok'] != 1:
            self.flag=False

        since_id = content['data']['cardlistInfo']['since_id']
        content_list = []
        cards = content['data']['cards']
        for c in cards:
            if c['card_type']==9:
                #记录时间
                temp={}
                temp['created_at']=c['mblog']['created_at']
                #记录文件内容
                t=requests.get('https://m.weibo.cn/statuses/extend?id={}'.format(c['mblog']['id']),self.headers)
                text=json.loads(t.content.decode())
                temp['longTextContent']=text['data']['longTextContent']
                content_list.append(temp)


        next_url=requests.get('https://m.weibo.cn/api/container/getIndex?sudaref=login.sina.com.cn&display=0&retcode=6102&type=uid&value=1784473157&containerid=1076031784473157&since_id={}'.format(since_id))
        return content_list,next_url

    def run(self):
        content=[]
        while self.flag:
            html_str=self.parse_url(self.url_temp)
            content_list,next_url=self.get_content_list(html_str)
            self.url_temp=next_url

            content.extend(content)

            print(content_list)






if __name__=='__main__':
    weibo=Spider()
    weibo.run()






