# coding=utf-8
# 猪八戒java兼职数据抓取
import sys

import requests
from bs4 import BeautifulSoup

from com.parttimejob.db.mysqlclient import MysqlClient


def parse(demands, key_word, webtype):
    # 创建数据库链接客户端
    mysql_client = MysqlClient()

    for demand in demands:
        try:
            task_id = demand["data-taskid"]
            detail_url = "https://task.zbj.com/" + task_id
            detail_html = requests.get(detail_url)
            soup = BeautifulSoup(detail_html.text, 'lxml')
            content = soup.find("div", attrs={"class": "demand-content J-show-hide hide-more"})
            # 发布人和时间
            user_and_publishtime = content.find("div", attrs={"class": "order-attr"}).get_text()
            amt = content.find("span", attrs={"class": "orange-color"}).get_text()
            amt = str(amt).replace('元', '')
            els = content.find_all("p", attrs={"class": "clearfix"})
            details = [el.find("span", attrs={"class": "description"}).get_text() for el in els]
            result = mysql_client.insert(detail_url, amt, user_and_publishtime, details, key_word, webtype,"zbj-"+task_id)
            if result == -1:
                return result
        except Exception as e:
            print(str(e))
            print("error:https://task.zbj.com/" + demand["data-taskid"])

    mysql_client.destory()


if __name__ == '__main__':

    keyword = ''
    webtype = '猪八戒'

    if not sys.argv[1] is None:
        keyword = sys.argv[1]

    print('查询关键字为：' + keyword)
    currentpage = 1

    url = "https://task.zbj.com/page" + str(currentpage) + ".html?k=" + keyword
    strhtml = requests.get(url)
    soup = BeautifulSoup(strhtml.text, 'lxml')
    totalpage = soup.find("input", attrs={"name": "total"})["value"]

    while int(currentpage) <= int(totalpage):
        url = "https://task.zbj.com/page" + str(currentpage) + ".html?k=" + keyword
        strhtml = requests.get(url)
        soup = BeautifulSoup(strhtml.text, 'lxml')
        demands = soup.find(id="utopia_widget_6").find_all("a", attrs={"class": "link-detail j-link-detail"})
        if parse(demands, keyword, webtype) == -1:
            break
            
        currentpage += 1
