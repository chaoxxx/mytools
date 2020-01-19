# coding=utf-8
# 软件交易数据抓取
import datetime
import sys

import requests
from bs4 import BeautifulSoup

from com.parttimejob.mysqlclient import MysqlClient

reload(sys);
sys.setdefaultencoding('utf-8')
def parse(demands, key_word, webtype):
    # 创建数据库链接客户端
    mysql_client = MysqlClient()

    for demand in demands:
        try:
            demand = demand.find("a")
            detail_url = demand["href"]
            task_id = str(detail_url).replace("/project/show/", "", 1)

            headers = {
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
                'Accept-Encoding': 'gzip, deflate, br',
                'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
                'Cache-Control': 'max-age=0',
                'Connection': 'keep-alive',
                'Host': 'www.sxsoft.com',
                'Referer': 'https://www.sxsoft.com/page/project',
                'Upgrade-Insecure-Requests': '1',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'}

            detail_url = "https://www.sxsoft.com" + detail_url
            detail_html = requests.get(detail_url, params=keyword, headers=headers, timeout=3)
            # detail_html = requests.get(url)
            soup = BeautifulSoup(detail_html.text, 'lxml')

            con = soup.find("div", attrs={"class": "bg-color-f5 clearfix"}).find("div", attrs={"class": "container"})

            # 发包人
            publish_user = con.find("div", attrs={"class": "owner clearfix"}).find("span", attrs={
                "class": "green"}).get_text().strip()

            project_msgs = con.find("div", attrs={"class": "project-msg clearfix"}).find_all("div", attrs={
                "class": "col-sm-3"})

            # 项目类型
            key_word = project_msgs[0].find("p", attrs={"class": "cat-name"}).get_text().strip()

            # 金额
            amt = project_msgs[1].find("p", attrs={"class": "cat-name"}).get_text().strip()

            # 任务名
            title = con.find("h1", attrs={"class": "project-title"})["title"]

            # 任务信息
            content = con.find("div", attrs={"class": "project-content clearfix"}).get_text().strip()

            # 任务发布时间
            user_info_action = con.find("div", attrs={"class": "owner clearfix"}).find_all("span")

            publish_time = user_info_action[1].get_text().strip()

            details = [title, '0', content]

            nowTime_str = datetime.datetime.now().strftime('%H:%M')

            result = mysql_client.insert(detail_url, amt, publish_user + "发布于" + publish_time + " " + nowTime_str,
                                         details,
                                         key_word, webtype, "sxsoft-" + task_id)

            if result == -1:
                return result

        except Exception as e:
            print(str(e))
            print("error:" + demand["href"])

    mysql_client.destory()


if __name__ == '__main__':

    keyword = ''
    webtype = '软件项目交易'

    try:
        if not sys.argv[1] is None:
            keyword = sys.argv[1]
    except:
        pass

    url = "https://www.sxsoft.com/page/project"
    strhtml = requests.get(url)
    soup = BeautifulSoup(strhtml.text, 'lxml')
    demands = soup.find("div", attrs={"class": "col-md-9 col-lg-9 list"}).find("ul", attrs={
        "class": "list-unstyled"}).find_all("h4")

    parse(demands, keyword, webtype)
