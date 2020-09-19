import sys
from bs4 import BeautifulSoup
import re
import urllib.request, urllib.error
import xlwt  # 进行Excel操作
from GID import get_weibo

def main():
    Baseurl = 'https://weibo.cn/comment/'
    datalist = get_weibo.getdata('https://weibo.cn/thepapernewsapp?page=')
    # 1.爬取网页
    contentlist = getcontent(Baseurl,datalist)
    #IDlence = (len(IDlist) - 1)
    savepath = "澎湃新闻1000-1350页.xls"
    # 3.保存数据
    saveData(datalist,contentlist, savepath)



# 爬取网页
def getcontent(Baseurl,datalist):
    contentlist = []

    for i in range(0, len(datalist)-1):  # 调用获取页面信息的函数，九次
        url = Baseurl + str(datalist[i][0])
        html = askURL(url)  # 保存获取到的网页源码
        # print(html)

        # 逐一解析数据
        soup = BeautifulSoup(html, "html.parser")
        for con in soup.find_all('div', class_="c",id='M_'):  # 查找符合要求的字符串，形成列表,这里查找的有多余，待修改(已修改)
            #print(item)
            data_content = []  # 保存信息
            con = str(con)


            con = re.sub('<a href="https://weibo.cn/(.*?)>#', ' ', con)
            con = re.sub('<span class="ctt">','',con)
            content = re.sub('<div class="c" id="M_"><div> <a href="/thepapernewsapp">澎湃新闻</a><img alt="V" src="https://h5.sinaimg.cn/upload/2016/05/26/319/5337.gif"/><img alt="M" src="https://h5.sinaimg.cn/upload/2016/05/26/319/donate_btn_s.png"/> :','',con)
            data_content.append(content)


            contentlist.append(data_content)  # 把处理好的信息放入contentlist

    Y = len(contentlist)
    contentlist.append(Y)
    #print(contentlist)
    #print(contentlist[-1])

    return contentlist




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


# 保存数据
def saveData(datalist,contentlist,savepath):
    print("save...")
    book = xlwt.Workbook(encoding="utf-8", style_compression=0)  # 创建workbook对象
    sheet = book.add_sheet('sheet1', cell_overwrite_ok=True)  # 创建工作表

    col = ('微博文章账号','标题','相关链接','评论数','点赞数','转发数','内容')
    for i in range(0, 7):
        sheet.write(0, i, col[i])  # 列名
    for i in range(0, datalist[-1]):
        print('第%d条' % (i + 1))
        data = datalist[i]  # 要保存的数据
        #print(data)
        for j in range(0, 6):
            sheet.write(i + 1, j, data[j])  # 数据

    for i in range(0,contentlist[-1]):
        print('第%d条内容' % (i + 1))
        data2 = contentlist[i]
        sheet.write(i+1,6,data2)


    book.save(savepath)  # 保存数据表


if __name__ == '__main__':  # 当程序执行时
    main()
    print("爬取完毕!")

# 调用函数
