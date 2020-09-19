import sys
from bs4 import BeautifulSoup
import re
import urllib.request, urllib.error
import xlwt  # 进行Excel操作
import time


def main():
    Baseurl = 'https://weibo.cn/thepapernewsapp?page='
    # 1.爬取网页
    datalist = getdata(Baseurl)
    #IDlence = (len(datalist) - 1)
    savepath = "澎湃新闻.xls"
    # 3.保存数据
    saveData(datalist, savepath)



# 创建正则表达式对象，表示规则（字符串的模式）
ID = re.compile(r'M_(.*?)')

#每一条微博ID号
findID = re.compile(r'M_(.*?)">')
# 微博标题
findTitle = re.compile(r'">#(.*?)#</a>|【(.*?)】')
#标题链接
findlink = re.compile(r'<a href=(.*?)>#')
# 评论数
findComment = re.compile(r'>评论(.*?)<')
# 点赞数
findlike = re.compile(r'>赞(.*?)<')
# 转发数
#findForward = re.compile(r'>转发[(\d*)]<')  # 未解决，这样子没法匹配到转发数
findForward = re.compile(r'>转发(.*?)<')
#替换链接
#replacelink = re.compile(r'[a-zA-z]+://[^\s]*')



#判断所给的字符串是否只包含中文
def check_contain_chinese(check_str):
    flag = True
    for ch in check_str :
        if u'\u4e00' >= ch or ch >= u'\u9fff':
            flag = False
    return flag


# 爬取网页
def getdata(Baseurl):
    datalist = []
    #ID = re.compile(r'M_(.*?)')
    #findID = re.compile(r'M_(.*?)">')
    for i in range(1000, 1350):  # 调用获取页面信息的函数，九次
        url = Baseurl + str(i)
        time.sleep(2)
        html = askURL(url)  # 保存获取到的网页源码
        # print(html)

        # 逐一解析数据
        soup = BeautifulSoup(html, "html.parser")
        for item in soup.find_all('div', class_="c", id=ID):  # 查找符合要求的字符串，形成列表,这里查找的有多余，待修改(已修改)
            #print(item)
            data = []  # 保存信息
            item = str(item)

            IDnumber = re.findall(findID, item)
            if len(IDnumber) != 0:
                IDnumber = IDnumber[0]
                data.append(IDnumber)
            else:
                data.append("")  # 留空


            title = re.findall(findTitle, item)
            if len(title) != 0:
                if check_contain_chinese(str(title)) == True:
                    title = title[0]
                    data.append(title)
                else:
                    title = str(title[0])
                    title = re.sub('<a href="https://weibo.cn/(.*?)>#',' ',title)
                    data.append(title)
            else:
                data.append("")  # 留空

            link = re.findall(findlink, item)
            if len(link) != 0:
                link = link[0]
                data.append(link)
            else:
                data.append("")  # 留空

            comment = re.findall(findComment, item)
            if len(comment) != 0:
                comment = comment[0]
                #comment = re.sub('"["|"]"','',comment)
                data.append(comment)
            else:
                data.append("")  # 留空

            like = re.findall(findlike, item)
            if len(like) != 0:
                like = like[0]
                data.append(like)
            else:
                data.append("")  # 留空

            forword = re.findall(findForward, item)
            if len(forword) != 0:
                forword = forword[0]
                data.append(forword)
            else:
                data.append("")  # 留空

            datalist.append(data)  # 把处理好的信息放入datalist

    X = len(datalist)
    datalist.append(X)
    print(datalist)
    print(datalist[-1])

    return datalist




# 得到指定一个url的网页内容
def askURL(url):
    head = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36",

        "cookie": "_T_WM=35741482901; SCF=AmvmEtdgbVNBLmY81b6nBUc87xPm36q8vSZjcyCgj68x-aG008yAR0L9y3r7Rr1F_50rLdr2o2BSdFmsblIMMIU.; SUB=_2A25yVyFBDeRhGeNM71oS8ifKzz6IHXVRuE8JrDV6PUJbktANLVmskW1NTgP5MCDkG4SdvMaBAF7itwAoudOB9Xw9; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WWT3P_xWuc.x6bc01FVbD_G5JpX5KzhUgL.Fo-EShn0eo.cShz2dJLoIEBLxKMLBKzLBKMLxKML12-L1h.LxKnL12qLBozLxKML1hBLBoqt; SUHB=08J7XCqOJpiTJ1; ALF=1601887761"
    }
    request = urllib.request.Request(url, headers=head)
    html = ""
    try:
        response = urllib.request.urlopen(request)
        html = response.read().decode("utf-8")
        # print(html)
    except urllib.error.URLError as e:
        if hasattr(e, "code"):
            print(e.code)
        if hasattr(e, "reason"):
            print(e.reason)

    return html


if __name__ == '__main__':  # 当程序执行时
    main()
    print("爬取完毕!")
