from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import pymysql
import win_unicode_console
win_unicode_console.enable()


def geturl(auto):
    print("进入抓取帖子程序...请耐心等待，不要关闭程序...")
    db = pymysql.connect("58.87.124.5", "tieba", "Xiangni365", "tieba")
    clear = "truncate table kuolie"
    cursor = db.cursor()
    print("----正在清除旧数据----")
    cursor.execute(clear)
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--ignore-certificate-errors')
    chrome_options.add_argument('log-level=3')
    driver = webdriver.Chrome(
        executable_path='chromedriver.exe', chrome_options=chrome_options)
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
            href = link.get_attribute('href')
            if href:
                print(title)
                print(href)
                print("----开始插入----")
                insert_sql = "INSERT INTO kuolie(title, url) VALUES ('%s','%s')" % (
                    title, href)
                cursor.execute(insert_sql)
                db.commit()
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
    print("抓取完成！请重新运行程序，选择第二项更新QQ数据库吧！")
    if auto == 1:
        pass
    else:
        input('....按任意键退出程序')
        print("程序退出")
