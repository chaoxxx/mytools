# coding=utf-8
# 一品威客兼职数据抓取
import datetime
import sys

import requests
from bs4 import BeautifulSoup

from com.parttimejob.db.mysqlclient import MysqlClient


def parse(demands, key_word, webtype):
    # 创建数据库链接客户端
    mysql_client = MysqlClient()

    for demand in demands:
        try:
            detail_url = demand["href"]
            task_id = str(detail_url).replace("http://www.epwk.com/task/", "", 1).replace("/", "", 1)
            detail_html = requests.get(detail_url)
            soup = BeautifulSoup(detail_html.text, 'lxml')

            con = soup.find("div", attrs={"class": "tasktopdet"})

            # 发包人
            publish_user = con.find("div", attrs={"class": "task-user-header"}).find("span").get_text()

            # 金额
            amt = con.find("div", attrs={"class": "task_user_info"}).find("span", attrs={"class": "nummoney f_l"}).find(
                "span").get_text()

            # 任务名
            title = con.find("div", attrs={"class": "task_user_info"}).find("h1").get_text()

            # 任务信息
            content = con.find("div", attrs={"class": "task-info-content"}).get_text()

            # 任务发布时间
            user_info_action = con.find("div", attrs={"class": "task-user-info-action"}).find_all("span", attrs={
                "class": "dib_vm"})
            publish_time = user_info_action[0].get_text()

            details = [title, '0', content]

            nowTime_str = datetime.datetime.now().strftime('%H:%M')

            result = mysql_client.insert(detail_url, amt, publish_user + "发布于" + publish_time + " " + nowTime_str,
                                         details,
                                         key_word, webtype,"epwk-"+task_id)

            if result == -1:
                return result

        except Exception as e:
            print(str(e))
            print("error:" + demand["href"])

    mysql_client.destory()


if __name__ == '__main__':

    keyword = ''
    webtype = '一品威客'

    try:
        if not sys.argv[1] is None:
            keyword = sys.argv[1]
    except:
        pass

    print('查询关键字为：' + keyword)

    currentpage = 1
    url = "http://www.epwk.com/task/o7/page" + str(currentpage) + ".html?k=" + keyword  # o7 为按时间倒序
    strhtml = requests.get(url)
    soup = BeautifulSoup(strhtml.text, 'lxml')
    total_pages = soup.find("div", attrs={"class": "page pt_15 pb_15"}).find("span").get_text()
    x = total_pages.split("/", 1)
    total = x[1].replace("页", "").strip()

    while int(currentpage) <= int(total):
        url = "http://www.epwk.com/task/o7/page" + str(currentpage) + ".html?k=" + keyword
        strhtml = requests.get(url)
        soup = BeautifulSoup(strhtml.text, 'lxml')
        demands = soup.find("div", attrs={"class": "task_class_list_li"}).find_all("a", attrs={"class": "font14"})
        if parse(demands, keyword, webtype) == -1:
            break

        currentpage += 1
