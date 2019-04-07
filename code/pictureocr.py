# coding:utf-8
import json
from selenium import webdriver
import re
import urllib.request
import win_unicode_console
import requests
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
