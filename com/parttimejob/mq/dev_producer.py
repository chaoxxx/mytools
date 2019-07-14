# coding:UTF-8

from com.parttimejob.mq.mq_util import MqUtil

topic_name = '/topic/dev/topic'
header = 'dev'

mq_util = MqUtil()


# 推送到主题
def send_to_topic(msg):
    mq_util.send_to_topic(topic_name, msg)


if __name__ == '__main__':
    send_to_topic("你好世界！")
