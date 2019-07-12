# coding=utf-8

import time
import pymysql
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver

# 打开数据库连接
db = pymysql.connect("127.0.0.1", "ride_master", "ride_master", "less_credit")

browser = webdriver.Firefox()
browser.get("http:\\www.baidu.com/")

elem = browser.find_element_by_name('wd')
elem.send_keys("全国法院被执行人信息查询 - 被执行人查询")
browser.find_element_by_xpath('//*[@id="su"]').click()

# initlize
data = pd.DataFrame()
print("正在爬取...")

time.sleep(1.5)

# 使用cursor()方法获取操作游标
cursor = db.cursor()


def insert(name, card_no, rights):
    size = len(rights)
    if size > 7:
        c0 = str(rights[0]).strip()
        c1 = str(rights[1]).strip()
        c2 = str(rights[2]).strip()
        c3 = str(rights[3]).strip()
        c4 = str(rights[4]).strip()
        c5 = str(rights[5]).strip()
        c6 = str(rights[6]).strip()
        c7 = str(rights[7]).strip()
    else:
        # SQL 插入语句
        c0 = ""
        c1 = str(rights[0]).strip()
        c2 = str(rights[1]).strip()
        c3 = str(rights[2]).strip()
        c4 = str(rights[3]).strip()
        c5 = str(rights[4]).strip()
        c6 = str(rights[5]).strip()
        c7 = str(rights[6]).strip()

    sql = "INSERT INTO less_credit.credit_info(`name`,card_no,c0, c1, c2, c3,c4,c5,c6,c7) VALUES ('%s','%s', '%s',  '%s',  '%s',  '%s',  '%s',  '%s',  '%s',  '%s')" % (
        name, card_no,
        c0,
        c1,
        c2,
        c3,
        c4,
        c5,
        c6,
        c7)

    print(sql)
    try:
        # 执行sql语句
        cursor.execute(sql)
        # 执行sql语句
        db.commit()
    except:
        # 发生错误时回滚
        db.rollback()


def scrapef():
    time.sleep(1)
    soup = BeautifulSoup(browser.page_source, "lxml")
    items = soup.find_all("li", attrs={"class": "op_trust_item OP_LOG_BTN"})

    for li in items:
        name = li.find("span", attrs={"class": "op_trust_name"}).get_text()
        id_card = li.find("span", attrs={"class": "op_trust_fl op_trust_papers"}).get_text()

        leftEl = li.find_all("td", attrs={"class": "op_trust_tdLeft"})
        rightEl = li.find_all("td", attrs={"class": "op_trust_tdRight"})
        lefts = [x.get_text() for x in leftEl]
        rights = [x.get_text() for x in rightEl]
        insert(name, id_card, rights)
    # netx  page
    browser.find_element_by_xpath('//p/span[@class="op_trust_page_next OP_LOG_BTN"]').click()


while (True):
    try:
        scrapef()
    except:
        print("warning! 处理失败")
# 关闭数据库连接
db.close()
