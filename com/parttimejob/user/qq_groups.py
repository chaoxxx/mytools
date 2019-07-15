# coding=utf-8


class QQGroups(object):

    def __init__(self):
        self.groups = {}

    # 新增
    def add(self, group_no, mq):
        self.groups[group_no] = mq

    # 删除
    def del_it(self, group_no):
        self.groups.pop(group_no)
