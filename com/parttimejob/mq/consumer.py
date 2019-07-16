# coding:UTF-8
import sys
import time

from com.parttimejob import banner
from com.parttimejob.channel import qq
from com.parttimejob.mq import dev_producer, ad_producer
from com.parttimejob.mq.listener.mq_listener import MqListener
from com.parttimejob.mq.mq_util import MqUtil
from com.parttimejob.user.qq_groups import QQGroups


def gen_atta_size(con):  # 参数可以是任意数据类型
    if con:
        size_b = sys.getsizeof(con)
        size = str(size_b) + 'B'
        size_k = size_b / 1024
        if size_k > 1:
            size = '%.1f' % size_k + 'K'
            size_m = size_k / 1024
            if size_m > 1:
                size = '%.2f' % size_m + 'M'
    else:  # "", {}, [], 都是站用空间的, 这里忽略, 主要统计文本大小
        size = "0B"
    return size

if __name__ == '__main__':
    qq_groups = QQGroups()

    while 1:
        group_list = qq.get_group_list() # 获取当前qq群
        for group in group_list:
            key = str(group['group_id'])
            if key in qq_groups.groups:
                pass
            else:
                mq = MqUtil()
                # 设置监听器
                mq.conn.set_listener(key+"mq-listener", MqListener(key))
                # 根据 key 获取 当前qq群的订阅频道
                # 目前默认订阅的为 dev 和 ad
                mq.conn.subscribe(dev_producer.topic_name)
                mq.conn.subscribe(ad_producer.topic_name)

                qq_groups.add(key, mq)
                qq.sendMes(key, banner.msg)

        time.sleep(60)  # secs





