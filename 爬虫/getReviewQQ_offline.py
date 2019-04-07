from selenium import webdriver
import time
import re
import os
import win_unicode_console
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
    executable_path='chromedriver.exe', chrome_options=chrome_options)
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
