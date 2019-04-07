from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver import ActionChains
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
import time, json,sys
import pymysql
import re
import os
from bs4 import BeautifulSoup
from urllib.request import urlopen
import win_unicode_console
win_unicode_console.enable()


def revqq():
    print("进入抓取QQ程序...,此步骤较长，请耐心等待，一定不要关闭程序...")
    db = pymysql.connect("58.87.124.5", "tieba", "Xiangni365", "tieba")
    clear = "truncate table qq"
    cursor = db.cursor()
    print("----正在清除旧数据----")
    cursor.execute(clear)
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
    #driver = webdriver.PhantomJS(executable_path="phantomjs.exe")
    # driver.set_page_load_timeout(15)
    sql = "SELECT URL FROM kuolie"
    cursor.execute(sql)
    result = cursor.fetchall()
    amount = len(result)
    print("当前数据库中有%d条帖子。" % (amount))
    time.sleep(1)
    i = 0
    while i < amount:
        current = result[i][0]
        print("现在尝试从%s获取QQ号......" % (current))
        checkTitle = "SELECT title FROM kuolie WHERE url='%s'" % (current)
        cursor.execute(checkTitle)
        title = cursor.fetchone()
        print("此帖子的标题为：%s" % (title))
        driver.maximize_window()
        # try:
        #     driver.get(current)
        # except TimeoutException:
        #     print ('！！！！！！time out after 10 seconds when loading page ! ! ! ! ! ! ')
        #     # 当页面加载时间超过设定时间，通过js来stop，即可执行后续动作
        #     driver.execute_script("window.stop()")
        driver.get(current)
        time.sleep(5)
        driver.save_screenshot("demo.png")
        text = driver.find_elements_by_class_name("content")
        length = len(text)
        u = 0
        while u < length:
            pureNumber = re.sub("\D", "", text[u].text)
            if len(pureNumber) <= 12 and len(pureNumber) >= 8:
                print(pureNumber)
                checkQQ = "SELECT * FROM qq WHERE qq='%d'" % (int(pureNumber))
                cursor.execute(checkQQ)
                checkQQResult = cursor.fetchone()
                if not checkQQResult:
                    insert = "INSERT INTO qq VALUES (%d)" % (int(pureNumber))
                    cursor.execute(insert)
                    print("----开始插入----")
            u = u + 1
        i = i + 1
    print("抓取完毕！请访问http://58.87.124.5/开始愉♂快的加好友吧！")
    input('....按任意键退出程序')
    print("程序退出")