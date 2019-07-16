# coding:utf-8
import datetime

from xlwt import Workbook

from com.parttimejob.db.mysqlclient import MysqlClient

mysql = MysqlClient()


def create_yesterday_excle():
    yesterday = (datetime.datetime.now() + datetime.timedelta(days=1)).strftime('%Y-%m-%d')
    today = datetime.datetime.now().strftime('%Y-%m-%d')

    res = mysql.get_partjob_list(yesterday, today)

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

    w.save('/tmp/' + yesterday + "全网发包.xlsx")


def create_seven_day_excle():
    seven_day = (datetime.datetime.now() + datetime.timedelta(days=7)).strftime('%Y-%m-%d')
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
    create_seven_day_excle()
