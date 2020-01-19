# coding=utf-8
# 一品威客兼职数据抓取
import json
import sys
import time

import jsonpath
import requests

from com.parttimejob.db.mysqlclient import MysqlClient


def parse(demands, key_word, webtype):
    # 创建数据库链接客户端
    mysql_client = MysqlClient()

    for demand in demands:
        detail_url = "https://codemart.com/project/" + str(demand["id"])
        try:
            # 发包人
            publish_user = "未知用户"

            # 金额
            amt = demand['price']

            # 任务名
            title = demand['name']

            # 任务信息
            content = demand['description']

            # 任务发布时间
            publish_time = demand['pubTime']
            timeStamp = float(int(publish_time) / 1000)

            timeArray = time.localtime(timeStamp)
            otherStyleTime = time.strftime("%Y-%m-%d %H:%M", timeArray)

            details = [title, '0', content]

            result = mysql_client.insert(detail_url, amt, publish_user + "发布于" + otherStyleTime,
                                         details,
                                         key_word, webtype, "codemart-" + str(demand["id"]))

            if result == -1:
                return result

        except Exception as e:
            print(str(e))
            print("error:" + detail_url)

    mysql_client.destory()


if __name__ == '__main__':

    keyword = ''
    webtype = '码市'

    try:
        if not sys.argv[1] is None:
            keyword = sys.argv[1]
    except:
        pass

    print('查询关键字为：' + keyword)

    currentpage = 1

    url = "https://codemart.com/api/project?name=" + keyword + "&page=" + str(currentpage)

    headers = {'Accept': 'application/json',
               'Accept-Encoding': 'gzip,deflate,br',
               'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
               'Connection': 'keep-alive',
               'Host': 'codemart.com',
               'Referer': 'https://codemart.com/projects',
               'User-Agent': 'Mozilla/5.0(WindowsNT10.0;Win64;x64)AppleWebKit/537.36(KHTML,likeGecko)Chrome/75.0.3770.100Safari/537.36'}

    strhtml = requests.get(url, params=keyword, headers=headers, timeout=3)
    c = strhtml.content
    unicodestr = json.loads(c)

    res = jsonpath.jsonpath(unicodestr, '$.pager.totalPage')
    total = res[0]

    while int(currentpage) <= int(total):
        url = "https://codemart.com/api/project?name=" + keyword + "&page=" + str(currentpage)

        strhtml = requests.get(url, params=keyword, headers=headers, timeout=3)
        c = strhtml.content
        unicodestr = json.loads(c)

        res = jsonpath.jsonpath(unicodestr, '$.rewards')[0]
        if parse(res, keyword, webtype) == -1:
            break

        currentpage += 1
