# coding=utf-8
# 一品威客兼职数据抓取
import json
import sys

import jsonpath
import requests

from com.parttimejob.db.mysqlclient import MysqlClient


def parse(demands, key_word, webtype):
    # 创建数据库链接客户端
    mysql_client = MysqlClient()

    for demand in demands:
        detail_url = "https://www.mayigeek.com/tab/projectDetail?id="+str(demand["id"])
        try:
            # 发包人
            publish_user = "未知用户"

            # 金额
            amt = str(demand['min_price'])

            # 任务名
            title = demand['name']

            # 任务信息
            content = demand['desc']

            # 任务发布时间
            publish_time = demand['create_date']

            key_word= ",".join(demand['typeStr'])


            details = [title, '0', content]

            result = mysql_client.insert(detail_url, amt, publish_user + "发布于" + publish_time,
                                         details,
                                         key_word, webtype,"mayigeek-"+str(demand["id"]))

            if result == -1:
                return result

        except Exception as e:
            print(str(e))
            print("error:" + detail_url)

    mysql_client.destory()


if __name__ == '__main__':

    keyword = ''
    webtype = '码易'

    try:
        if not sys.argv[1] is None:
            keyword = sys.argv[1]
    except:
        pass


    url="https://www.mayigeek.com/api/public/searchProjects?page=1&perpage=50&statusStr=&price=&teriminal=&bid_end=&order_by=id"
    headers = {'Accept': 'application/json, text/plain, */*',
               'Authorization': '',
               'Referer': 'https://www.mayigeek.com/tab/taskList?type=&price=&bidEnd=',
               'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'}

    res = requests.get(url, params=keyword, headers=headers, timeout=3)
    c = res.content
    unicodestr = json.loads(c)

    res = jsonpath.jsonpath(unicodestr, '$.info.info.list')[0]
    parse(res, keyword, webtype)
