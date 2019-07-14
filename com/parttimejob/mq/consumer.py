# coding:UTF-8

import time

from com.parttimejob.mq import dev_producer, ad_producer
from com.parttimejob.mq.listener.mq_listener import MqListener
from com.parttimejob.user.qq_groups import QQGroups

if __name__ == '__main__':
    qq_groups = QQGroups()

    for key, value in qq_groups.groups.items():
        # 设置监听器
        value.conn.set_listener("mq-listener", MqListener(key))

        # 根据 key 获取 当前qq群的订阅频道
        # 目前默认订阅的为 dev 和 ad
        value.conn.subscribe(dev_producer.topic_name)
        value.conn.subscribe(ad_producer.topic_name)

    while 1:
        time.sleep(60)  # secs
