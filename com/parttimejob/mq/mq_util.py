# coding:UTF-8

import stomp


class MqUtil(object):
    def __init__(self):
        self.ip = '127.0.0.1'
        self.port = 61613
        self.conn = stomp.Connection10([(self.ip, self.port)])
        self.conn.start()
        self.conn.connect()

    # 推送到队列queue
    def send_to_queue(self, queue_name, msg):
        self.conn.send(queue_name, msg)

    # 推送到主题
    def send_to_topic(self, topic_name, msg):
        self.conn.send(topic_name, msg)
        print(msg, "消息推送成功！")

    # 断开链接
    def distory(self):
        self.conn.disconnect()
