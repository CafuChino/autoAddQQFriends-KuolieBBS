import webbrowser
import pymysql
import time


def hell():
    db = pymysql.connect("58.87.124.5", "tieba", "Xiangni365", "tieba")
    cursor = db.cursor()
    sql = "SELECT qq FROM qq"
    cursor.execute(sql)
    result = cursor.fetchall()
    result = list(result)
    amount = len(result)
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
            % (result[i][0],fuin))
        time.sleep(int(sleep))
        i = i + 1
    input('程序结束！可以关闭程序了')
    print("程序退出")
