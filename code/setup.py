from selenium import webdriver
import time
import re
import os
import win_unicode_console
import json
import urllib.request
import requests
from selenium.webdriver.chrome.options import Options
import emoji
import webbrowser


def pictureocr():
    win_unicode_console.enable()
    apikey = '57byQin2TjXUeCi1iAj0GcMF'
    secretkey = '5CjTgAsRmVppfxbjkznrVPeVPE2tjcGe'
    get_token = requests.get(
        'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=%s&client_secret=%s'
        % (apikey, secretkey)).text
    token = json.loads(get_token)['access_token']
    accessUrl = 'https://aip.baidubce.com/rest/2.0/ocr/v1/general_basic?access_token=%s' % (
        token)
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36'
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--ignore-certificate-errors')
    chrome_options.add_argument('log-level=3')
    chrome_options.add_argument(
        'user-agent="Mozilla/5.0 (iPod; U; CPU iPhone OS 2_1 like Mac OS X; ja-jp) AppleWebKit/525.18.1 (KHTML, like Gecko) Version/3.1.1 Mobile/5F137 Safari/525.20"'
    )
    driver = webdriver.Chrome(
        executable_path='chromedriver.exe', options=chrome_options)
    start = open('url.ini', encoding='utf-8').readlines()
    for line in start:
        line = line.replace('\n', '')
        line = line.split(',')
        title = line[0]
        url = line[1]
        driver.maximize_window()
        driver.get(url)
        print(url)
        picture = driver.find_elements_by_class_name("BDE_Image")
        picture2 = driver.find_elements_by_tag_name("div")
        for picture in picture:
            url = picture.get_attribute('src')
            print(url)
            values = {
                'access_token': token,
                'url': '%s' % (url),
                'probability': 'true'
            }
            data = urllib.parse.urlencode(values).encode(encoding='UTF8')
            req = urllib.request.Request(accessUrl, data)
            req.add_header('Content-Type', 'application/x-www-form-urlencoded')
            response = urllib.request.urlopen(req)
            the_page = response.read()
            if (the_page):
                try:
                    amount1 = json.loads(
                        the_page.decode("utf-8"))['words_result_num']
                except KeyError:
                    break
                print("识别到文字%d处" % (amount1))
                q = 0
                while q < amount1:
                    currentResult = json.loads(
                        the_page.decode("utf-8"))['words_result'][q]["words"]
                    print(currentResult)
                    format = re.sub("\D", "", currentResult)
                    if len(format) >= 8 and len(format) <= 12:
                        if int(format[0]) == 0:
                            print('----自动修正----')
                            temp = list(format)
                            del temp[0]
                            format = "".join(temp)
                        print("识别到qq号%s" % (format))
                        qq = open('qq.ini', 'a+')
                        qq.write('%s ' % (format))
                        qq.close()
                    q = q + 1
        for picture in picture2:
            url2 = picture.get_attribute('data-url')
            if url2 is not None:
                print("发现图片资源！地址：%s" % (url2))
                print("----开始分析图片%s----" % (url2))
                values = {
                    'access_token': token,
                    'url': '%s' % (url2),
                    'probability': 'true'
                }
                data = urllib.parse.urlencode(values).encode(encoding='UTF8')
                req = urllib.request.Request(accessUrl, data)
                req.add_header('Content-Type',
                               'application/x-www-form-urlencoded')
                response = urllib.request.urlopen(req)
                the_page = response.read()
                if (the_page):
                    try:
                        amount1 = json.loads(
                            the_page.decode("utf-8"))['words_result_num']
                    except KeyError:
                        break
                    print("识别到文字%d处" % (amount1))
                    q = 0
                    while q < amount1:
                        currentResult = json.loads(the_page.decode(
                            "utf-8"))['words_result'][q]["words"]
                        print(currentResult)
                        format = re.sub("\D", "", currentResult)
                        if len(format) >= 8 and len(format) <= 12:
                            print(currentResult)
                            if int(format[0]) == 0:
                                print('----自动修正----')
                                temp = list(format)
                                del temp[0]
                                format = "".join(temp)
                            print("识别到qq号%s" % (format))
                            qq = open('qq.ini', 'a+')
                            qq.write('%s ' % (format))
                            qq.close()
                        q = q + 1


def hell():
    qq = open('qq.ini').readline()
    qq = qq.split(' ')
    amount = len(qq)
    print("数据库中有%d个qq号" % (amount))
    wish = input("请输入你想加的QQ号数目或输入0代表全部,请注意，软件不会保留你的进度，下次使用依然是从头开始。")
    if wish == '0':
        pass
    else:
        amount = int(wish)
        print("你这次打算添加%d个号码。" % (amount))
    sleep = 10
    fuin = input("请输入你当前登录的qq号")
    print("在加好友之前，你应该知道，软件抓取的qq号不一定完全正确，正确率大概有九成")
    print("所以试图添加一些本不存在的qq号也是正常的，所以你应该自己筛选决定是否添加")
    print("出于软件效率考虑考虑，自动进程很快，可能导致头像加载不出来")
    print("软件默认延时10秒，如果你希望更改这个延时可以现在输入数字(单位：秒)来更改或者输入10保持延时不变")
    sleep = input("注意，更短的延迟可能导致冻结！，请谨慎。更改延迟为(秒)：")
    print("我们相信你按照我们的要求输入了，但是如果你不小心输入错了，可能导致程序错误或者死机。")
    print("你的输入为：" + sleep + ",如果它不是一个正数，请退出程序重新操作。")
    input("或者输入一个y来开始进程")
    i = 0
    while i < amount:
        webbrowser.open(
            "tencent://AddContact/?fromId=1&fromSubId=1&subcmd=all&uin=%s&fuin=%s&website=www.oicqzone.com"
            % (qq[i], fuin))
        time.sleep(int(sleep))
        i = i + 1
    input('程序结束！可以关闭程序了')
    print("程序退出")


def geturl(auto):
    print("进入抓取帖子程序...请耐心等待，不要关闭程序...")
    print("----正在初始化----")
    start = open("url.ini", "w", encoding='utf-8')
    start.close()
    print("----正在清除旧数据----")
    os.remove('url.ini')
    tiezi = open("url.ini", "w", encoding='utf-8')
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--ignore-certificate-errors')
    chrome_options.add_argument('log-level=3')
    driver = webdriver.Chrome(
        executable_path='chromedriver.exe', options=chrome_options)
    # driver = webdriver.PhantomJS(executable_path="phantomjs.exe")
    driver.maximize_window()
    # if has Chinese, apply decode()
    driver.get("https://tieba.baidu.com/")
    time.sleep(1)
    ipt = driver.find_element_by_id("wd1")
    ipt.send_keys('扩列')
    btn = driver.find_element_by_class_name("search_btn")
    btn.click()
    time.sleep(1)
    i = 1
    while i <= 10:
        for link in driver.find_elements_by_class_name("j_th_tit"):
            title = link.get_attribute('title')
            title = emoji.demojize(title)
            href = link.get_attribute('href')
            if href:
                print(title)
                print(href)
                print("----开始插入----")
                tiezi.write("%s,%s\n" % (title, href))
        print("第%d页插入完成，准备翻页" % (i))
        nextPage = driver.find_element_by_class_name("next")
        nextUrl = nextPage.get_attribute('href')
        print('下一页链接已被识别，链接为:')
        print(nextUrl)
        print('开始翻页')
        nextPage.click()
        print("等待网页加载中")
        time.sleep(5)
        i = i + 1
    driver.close()
    tiezi.close()
    print("抓取完成！请重新运行程序，选择第二项更新QQ数据库吧！")
    if auto == 1:
        pass
    else:
        input('....按任意键退出程序')
        print("程序退出")


def getqq():
    win_unicode_console.enable()
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--ignore-certificate-errors')
    chrome_options.add_argument('log-level=3')
    chrome_options.add_argument(
        'user-agent="Mozilla/5.0 (iPod; U; CPU iPhone OS 2_1 like Mac OS X; ja-jp) AppleWebKit/525.18.1 (KHTML, like Gecko) Version/3.1.1 Mobile/5F137 Safari/525.20"'
    )
    driver = webdriver.Chrome(
        executable_path='chromedriver.exe', options=chrome_options)
    start = open('url.ini', encoding='utf-8').readlines()
    try:
        os.remove('qq.ini')
    except FileNotFoundError:
        qq = open('qq.ini', 'w')
    else:
        qq = open('qq.ini', 'w')
    qq.close()
    for line in start:
        line = line.replace('\n', '')
        line = line.split(',')
        title = line[0]
        url = line[1]
        driver.maximize_window()
        driver.get(url)
        time.sleep(3)
        text = driver.find_elements_by_class_name("content")
        for content in text:
            pureNumber = re.sub("\D", "", content.text)
            if len(pureNumber) <= 12 and len(pureNumber) >= 8:
                qq = open('qq.ini', 'a+')
                print(pureNumber)
                qq.write('%s ' % (pureNumber))
                qq.close()


print("---------欢迎使用扩列吧QQ号获取器V1.0版---------")
print("作者QQ：2253757310  请合法使用！")
print("1:抓取最新的十页帖子")
print("2:抓取数据库里帖子中的文字QQ号（需要数据库中有数据）")
print("3:抓取数据库里帖子中的图片QQ号（需要数据库中有数据，扩列成功率大）")
print("4:全自动抓取！静静等待吧！")
print("5:开始暴风骤雨式的自动加好友！")
select = input("请输入你的选项：")
print(select)
if select == '1':
    geturl(0)
else:
    if select == '2':
        getqq()
    else:
        if select == '3':
            pictureocr()
        else:
            if select == '4':
                geturl(1)
                getqq()
            else:
                if select == '5':
                    hell()
                else:
                    print('非法输入！')