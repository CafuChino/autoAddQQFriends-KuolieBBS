# coding:utf-8
import urllib
import json
import pymysql
from selenium import webdriver
import time
import re
import urllib.request
import win_unicode_console
from settings import host, user, password, database, apikey, secretkey
win_unicode_console.enable()


def ocr():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--ignore-certificate-errors')
    chrome_options.add_argument('log-level=3')
    chrome_options.add_argument(
        'user-agent="Mozilla/5.0 (iPod; U; CPU iPhone OS 2_1 like Mac OS X; ja-jp) AppleWebKit/525.18.1 (KHTML, like Gecko) Version/3.1.1 Mobile/5F137 Safari/525.20"'
    )
    driver = webdriver.Chrome(executable_path='chromedriver.exe', chrome_options=chrome_options)
    requesthost = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=%s&client_secret=%s' % (
        apikey, secretkey)
    request = urllib.request.Request(requesthost)
    request.add_header('Content-Type', 'application/json; charset=UTF-8')
    response = urllib.request.urlopen(request)
    content = response.read()
    if (content):
        token = json.loads(content)["access_token"]
        remain = json.loads(content)["expires_in"]
        print("已经获取到token，为%s,剩余可用期限为%.1f天。" % (token, remain / 86400))
    accessUrl = 'https://aip.baidubce.com/rest/2.0/ocr/v1/general_basic?access_token=%s' % (
        token)
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36'
    # print(accessUrl)
    db = pymysql.connect(host, user, password, database)
    cursor = db.cursor()
    sql = "SELECT URL FROM kuolie"
    cursor.execute(sql)
    result = cursor.fetchall()
    amount = len(result)
    print("当前数据库中有%d条帖子。" % (amount))
    time.sleep(1)
    i = 0
    while i < amount:
        current = result[i][0]
        print("现在尝试从%s获取图片QQ号......" % (current))
        checkTitle = "SELECT title FROM kuolie WHERE url='%s'" % (current)
        cursor.execute(checkTitle)
        title = cursor.fetchone()
        print("此帖子的标题为：%s" % (title))
        driver.maximize_window()
        driver.get(current)
        time.sleep(2.5)
        picture = driver.find_elements_by_class_name("BDE_Image")
        picture2 = driver.find_elements_by_tag_name("div")
        v = 0
        if len(picture) != 0:
            print("传统方法找到图片%d张" % (len(picture)))
            while v < len(picture):
                url = picture[v].get_attribute('src')
                print("----开始分析图片%s----" % (url))
                values = {
                    'access_token': token,
                    'url': '%s' % (url),
                    'probability': 'true'
                }
                data = urllib.parse.urlencode(values).encode(encoding='UTF8')
                print('----请求接口----')
                req = urllib.request.Request(accessUrl, data)
                req.add_header('Content-Type',
                               'application/x-www-form-urlencoded')
                response = urllib.request.urlopen(req)
                the_page = response.read()
                if (the_page):
                    amount1 = json.loads(
                        the_page.decode("utf-8"))['words_result_num']
                    print("识别到文字%d处" % (amount1))
                    q = 0
                    while q < amount1:
                        currentResult = json.loads(the_page.decode(
                            "utf-8"))['words_result'][q]["words"]
                        format = re.sub("\D", "", currentResult)
                        if len(format) >= 8 and len(format) <= 12:
                            print(currentResult)
                            if int(format[0]) == 0:
                                print('----自动修正----')
                                temp = list(format)
                                del temp[0]
                                format = "".join(temp)
                            print("识别到qq号%s" % (format))
                            insert = "INSERT INTO qq_special VALUE (%d)" % (
                                int(format))
                            print("----插入数据库----")
                            cursor.execute(insert)
                        else:
                            print("不含qq号")
                        q = q + 1
                v = v + 1
        else:
            print("传统方法未发现疑似图片...")
        u = 0
        if len(picture2) != 0:
            w = 0
            print("特殊方法找到疑似图片信息%d条..." % (len(picture2)))
            while u < len(picture2):
                url2 = picture2[u].get_attribute('data-url')
                if url2 is not None:
                    print("发现图片资源！地址：%s" % (url2))
                    print("----开始分析图片%s----" % (url2))
                    values = {
                        'access_token':
                        '24.26b764bc2743fa4489acd9950812ca65.2592000.1554533447.282335-15698863',
                        'url': '%s' % (url2),
                        'probability': 'true'
                    }
                    data = urllib.parse.urlencode(values).encode(
                        encoding='UTF8')
                    print('----请求接口----')
                    req = urllib.request.Request(accessUrl, data)
                    req.add_header('Content-Type',
                                   'application/x-www-form-urlencoded')
                    response = urllib.request.urlopen(req)
                    the_page = response.read()
                    if (the_page):
                        try:
                            amount2 = json.loads(
                                the_page.decode("utf-8"))['words_result_num']
                        except KeyError:
                            print("出错，跳过")
                        else:
                            print("识别到文字%d处" % (amount2))
                        q = 0
                        while q < amount2:
                            currentResult = json.loads(
                                the_page.decode(
                                    "utf-8"))['words_result'][q]["words"]
                            format = re.sub("\D", "", currentResult)
                            if len(format) >= 8 and len(format) <= 12:
                                print(currentResult)
                                if int(format[0]) == 0:
                                    print('----自动修正----')
                                    temp = list(format)
                                    del temp[0]
                                    format = "".join(temp)
                                print("识别到qq号%s" % (format))
                                insert = "INSERT INTO qq_special VALUE (%d)" % (
                                    int(format))
                                print("----插入数据库----")
                                cursor.execute(insert)
                            else:
                                print("不含qq号")
                            q = q + 1
                    w = w + 1
                u = u + 1
            if w == 0:
                print("特殊方法未侦测到图片信息...")
        print("----分析完毕，下一条------")
        i = i + 1
    input('....按任意键退出程序')
    # # 二进制方式打开图文件
    # f = open(r'########本地文件#######', 'rb')
    # # 参数image：图像base64编码
    # img = base64.b64encode(f.read())
    # params = {"image": img}
    # params = urllib.urlencode(params)
    # request = urllib2.Request(url, params)
    # request.add_header('Content-Type', 'application/x-www-form-urlencoded')
    # response = urllib2.urlopen(request)
    # content = response.read()
    # if (content):
    #     print(content)
ocr()