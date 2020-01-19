# coding=utf-8
# 开源中国兼职数据抓取
import json
import sys

import jsonpath
import requests
from bs4 import BeautifulSoup

from .mysqlclient import MysqlClient


def parse(demands, key_word, webtype):
    # 创建数据库链接客户端
    mysql_client = MysqlClient()

    for demand in demands:
        detail_url = "https://zb.oschina.net/project/detail?id=" + str(demand["id"])
        urla = 'https://zb.oschina.net/project/detail.html?id=' + str(demand["id"])
        # print(detail_url)

        headers = {'Accept': 'application/json',
                   'Accept-Encoding': 'gzip,deflate,br',
                   'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
                   'Connection': 'keep-alive',
                   'Host': 'zb.oschina.net',
                   'Referer': 'https://zb.oschina.net/projects/list.html',
                   'User-Agent': 'Mozilla/5.0(WindowsNT10.0;Win64;x64)AppleWebKit/537.36(KHTML,likeGecko)Chrome/75.0.3770.100Safari/537.36'}

        strhtml = requests.get(detail_url, params=keyword, headers=headers, timeout=3)

        c = strhtml.content
        unicodestr = json.loads(c)

        res = jsonpath.jsonpath(unicodestr, '$.data')[0]

        try:
            # 发包人
            publish_user = "未知用户"
            # 项目编号
            projectNo = res['projectNo']

            # 金额
            amt_min = res['budgetMinByYuan']
            amt_max = res['budgetMaxByYuan']
            if amt_max != str(0):
                amt = str(amt_min) + "-" + str(amt_max)
            else:
                amt = "价格面议"

            # 任务名
            title = res['name']

            print(title)

            # 任务信息
            content = res['prd']

            soup = BeautifulSoup(str(content), 'lxml')
            content = soup.get_text().strip()

            # 任务发布时间
            publish_time = res['publishTime']

            details = [title, '0', content]

            result = mysql_client.insert(urla, amt, publish_user + "发布于" + publish_time,
                                         details,
                                         key_word, webtype, "oschina-" + projectNo)

            if result == -1:
                print("过期数据不处理", urla)
                continue

        except Exception as e:
            print(str(e))
            # print("error:" + detail_url)
            pass
    mysql_client.destory()


if __name__ == '__main__':

    keyword = ''
    webtype = '开源中国'

    try:
        if not sys.argv[1] is None:
            keyword = sys.argv[1]
    except:
        pass

    print('查询关键字为：' + keyword)

    currentpage = 1

    url = "https://zb.oschina.net/project/contractor-browse-project-and-reward?keyword=" + keyword + "&applicationAreas=&sortBy=30&currentTime=&pageSize=500&currentPage=" + str(
        currentpage)

    headers = {'Accept': '*/*',
               'Accept-Encoding': 'gzip, deflate, br',
               'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
               'Connection': 'keep-alive',
               'Host': 'zb.oschina.net',
               'Referer': 'https://zb.oschina.net/projects/list.html',
               'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
               'X-Requested-With': 'XMLHttpRequest'}

    strhtml = requests.get(url, params=keyword, headers=headers, timeout=3)
    c = strhtml.content
    unicodestr = json.loads(c)

    res = jsonpath.jsonpath(unicodestr, '$.data.totalPage')
    total = res[0]

    while int(currentpage) <= int(total):
        url = "https://zb.oschina.net/project/contractor-browse-project-and-reward?keyword=" + keyword + "&applicationAreas=&sortBy=30&currentTime=&pageSize=500&currentPage=" + str(
            currentpage)

        strhtml = requests.get(url, params=keyword, headers=headers, timeout=3)
        c = strhtml.content
        unicodestr = json.loads(c)

        res = jsonpath.jsonpath(unicodestr, '$.data.data')[0]
        if parse(res, keyword, webtype) == -1:
            break

        currentpage += 1
