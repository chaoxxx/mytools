# coding:utf-8
import datetime
import os

from xlwt import Workbook

from com.parttimejob.mysqlclient import MysqlClient

mysql = MysqlClient()


def create_yesterday_excle():
    yesterday = (datetime.datetime.now() - datetime.timedelta(days=1)).strftime('%Y-%m-%d')
    today = datetime.datetime.now().strftime('%Y-%m-%d')

    res = mysql.get_partjob_list(yesterday, today)

    w = Workbook()  # 创建一个工作簿
    ws = w.add_sheet('1')  # 创建一个工作表

    col = 0

    ws.write(col, 0, '任务编号')
    ws.write(col, 1, '平台')
    ws.write(col, 2, '工作类型')
    ws.write(col, 3, '任务名')
    ws.write(col, 4, '报酬')
    ws.write(col, 5, '发布时间')
    ws.write(col, 6, '任务链接')

    for s in res:
        col += 1
        ws.write(col, 0, s[0])
        ws.write(col, 1, s[1])
        ws.write(col, 2, s[2])
        ws.write(col, 3, s[3])
        ws.write(col, 4, s[4])
        ws.write(col, 5, s[5])
        ws.write(col, 6, s[6])

    rootpath = '/root/jianzhixinxitongji/软件类信息汇总/' + yesterday

    if not os.path.exists(rootpath):
        os.makedirs(rootpath)

    w.save(rootpath + "/昨日全网发包.xlsx")


def create_seven_day_excle():
    seven_day = (datetime.datetime.now() - datetime.timedelta(days=7)).strftime('%Y-%m-%d')
    today = datetime.datetime.now().strftime('%Y-%m-%d')

    res = mysql.get_partjob_list(seven_day, today)

    w = Workbook()  # 创建一个工作簿
    ws = w.add_sheet('1')  # 创建一个工作表

    col = 0

    ws.write(col, 0, '包名')
    ws.write(col, 1, '报酬')
    ws.write(col, 2, '任务链接')

    for s in res:
        col += 1
        ws.write(col, 0, s[3])
        ws.write(col, 1, s[4])
        ws.write(col, 2, s[6])

    w.save('/tmp/' + "近7天全网发包.xlsx")


if __name__ == '__main__':
    create_yesterday_excle()
    # create_seven_day_excle()
