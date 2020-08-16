import requests
import json

class Spider:
    def __init__(self):
        self.flag=True
        self.url=('https://m.weibo.cn/api/container/getIndex?sudaref=login.sina.com.cn&display=0&retcode=6102&type=uid&value=1784473157&containerid=1076031784473157')
        self.headers={
'User-Agent':'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Mobile Safari/537.36'
}

    def parse_url(self,url):
        response = requests.get(url, self.headers)
        html_str = response.content.decode()
        return html_str





    def get_content_list(self,html_str):
        contents = json.loads(html_str)
        if contents['ok'] != 1:
            self.flag=False

        since_id = contents['data']['cardlistInfo']['since_id']
        cards = contents['data']['cards']
        content_list = []
        for c in cards:
            if c['card_type']==9:
                #记录时间
                temp={}
                temp['created_at']=c['mblog']['created_at']
                content_list.append(temp)
                #记录文件内容
                if c['mblog']['isLongText'] == 'true':

                    t=requests.get('https://m.weibo.cn/statuses/extend?id={}'.format(c['mblog']['id']),self.headers)
                    text=json.loads(t.content.decode())
                    temp['longTextContent']=text['data']['longTextContent']
                    content_list.append(temp)
                else:
                    text = c['mblog']['text']
                    content_list.append(text)


        next_url=requests.get('https://m.weibo.cn/api/container/getIndex?sudaref=login.sina.com.cn&display=0&retcode=6102&type=uid&value=1784473157&containerid=1076031784473157&since_id={}'.format(since_id))
        return content_list,next_url

    def run(self):
        content=[]
        while self.flag:
            html_str=self.parse_url(self.url)
            content_list,next_url=self.get_content_list(html_str)
            self.url=next_url
            content.extend(content_list)
            print(content,'\n')






if __name__=='__main__':
    weibo=Spider()
    weibo.run()



