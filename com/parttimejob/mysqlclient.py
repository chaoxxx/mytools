# coding=utf-8
# 数据库操作
import datetime
import re
import time

import pymysql


class MysqlClient(object):

    def __init__(self):
        self.db = pymysql.connect("cosmozhu.fun", "cosmo", "cosmo123456", "cosmo")
        # self.db = pymysql.connect("127.0.0.1", "ride_master", "ride_master", "less_credit")
        # 使用cursor()方法获取操作游标
        self.cursor = self.db.cursor()

    def destory(self):
        self.cursor.close()
        self.db.close()

    def get_partjob_list(self, start_time, end_time):
        sql = "select job_no,web_type,job_type,job_title,job_amt,publish_time,job_url from parttimejobinfo where publish_time between '" + start_time + "' and '" + end_time + "' order by job_no"
        self.cursor.execute(sql)

        return self.cursor.fetchall()

    def insert(self, url, amt, ser_and_publishtime, details, keyword, webtype, job_no):
        mat = re.search(r"(\d{4}-\d{1,2}-\d{1,2} \d{1,2}:\d{1,2})", ser_and_publishtime)
        publish_time = str(mat.group(0))
        s_time = time.mktime(time.strptime(publish_time, '%Y-%m-%d %H:%M'))

        nowTime_str = datetime.datetime.now().strftime('%Y-%m-%d')
        e_time = time.mktime(time.strptime(nowTime_str, "%Y-%m-%d"))
        diff = e_time - s_time

        if diff > 1 * 24 * 60 * 60:
            return -1

        # 执行sql语句
        sql = "insert into parttimejobinfo (web_type,job_type,job_url,publish_info,job_title,job_amt,job_desc,publish_time,job_no) values('%s','%s','%s','%s','%s','%s','%s','%s','%s')" % (
            webtype,
            keyword,
            url.strip(),
            ser_and_publishtime.strip(),
            str(details[0]).strip(),  # 任务名称
            amt.strip(),
            str(details[2]).strip()[:500],  # 任务描述
            publish_time,
            job_no
        )

        try:
            self.cursor.execute(sql)
            # 执行sql语句
            self.db.commit()
        except Exception as e:
            # 发生错误时回滚
            print(str(e))
            print("error 数据回滚")
            self.db.rollback()

        return 0
