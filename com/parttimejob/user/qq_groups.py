# coding=utf-8
from com.parttimejob.mq.mq_util import MqUtil


class QQGroups(object):

    def __init__(self):
        self.groups = {}
        array = ['827718520']
        for x in array:
            mq = MqUtil()
            self.add(x, mq)

    # 新增
    def add(self, group_no, mq):
        self.groups[group_no] = mq

    # 删除
    def del_it(self, group_no):
        self.groups.pop(group_no)
