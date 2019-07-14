# coding=utf-8
import random

import xlrd as xlrd

from com.parttimejob.mq import ad_producer


class PostAD(object):
    def __init__(self):
        self.path = 'ad.xlsx'

    def get_a_ad(self):
        book = xlrd.open_workbook(self.path)  # 打开一个excel
        sheet = book.sheet_by_index(0)  # 根据顺序获取sheet
        return sheet.cell(random.randint(0, int(sheet.nrows)-1), 0).value


if __name__ == '__main__':
    postad = PostAD()
    ad_producer.send_to_topic(postad.get_a_ad())
