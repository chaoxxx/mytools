# coding=utf-8
# 一品威客兼职数据抓取
import datetime
import re
import sys

import requests
from bs4 import BeautifulSoup

from com.parttimejob.db.mysqlclient import MysqlClient


def parse(demands, key_word, webtype):
    # 创建数据库链接客户端
    mysql_client = MysqlClient()

    for demand in demands:
        try:
            key_word = demand.find("span",attrs={"class":"skill"}).get_text().strip()
            demand = demand.find("h4",attrs={"class":"media-heading"}).find("a")
            detail_url = demand['href']
            task_id = str(detail_url).replace("/projects/", "", 1)


            detail_url= "http://www.taskcity.com/projects/"+task_id
            detail_html = requests.get(detail_url)
            soup = BeautifulSoup(detail_html.text, 'lxml')

            con = soup.find("div", attrs={"class": "col-sm-7"})

            # 发包人
            publish_user = "未知用户"

            left = con.find("div", attrs={"class": "pull-left space-right-30"}).find_all("div")

            # 金额
            amt = left[1].find("b").get_text().strip()

            # 任务名
            title = soup.find(id="project_title_name").get_text().strip()

            # 任务信息

            pattern = re.compile("描述")
            element = soup.find('h3', text=pattern).parent

            content = element.find_all("div",recursive=False)[3].get_text().strip()

            # 任务发布时间
            pattern = re.compile("发布日期")
            user_info_action = soup.find('div', text=pattern).get_text()

            mat = re.search(r"(\d{4}-\d{1,2}-\d{1,2})", user_info_action)
            publish_time = str(mat.group(0))
            details = [title, '0', content]

            nowTime_str = datetime.datetime.now().strftime('%H:%M')

            result = mysql_client.insert(detail_url, amt, publish_user + "发布于" + publish_time + " " + nowTime_str,
                                         details,
                                         key_word, webtype,"taskcity-"+task_id)

            if result == -1:
                return result

        except Exception as e:
            print(str(e))
            print("error:" + demand["href"])

    mysql_client.destory()


if __name__ == '__main__':

    keyword = ''
    webtype = '智城'

    try:
        if not sys.argv[1] is None:
            keyword = sys.argv[1]
    except:
        pass


    url = "http://www.taskcity.com/projects"
    strhtml = requests.get(url)
    soup = BeautifulSoup(strhtml.text, 'lxml')
    demands = soup.find_all("div", attrs={"class": "panel panel-default"})[1].find_all("div", attrs={"class": "media"})
    parse(demands, keyword, webtype)



