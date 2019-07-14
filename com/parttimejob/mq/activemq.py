# coding:UTF-8
import json

import stomp
import time

from com.parttimejob import qq
from com.parttimejob.mq.Job import Job

queue_name = '/queue/javaqueue'
topic_name = '/topic/javatopic'
listener_name = 'javaListener'

ip = '127.0.0.1'
port = 61613


class javaListener(object):
    def on_message(self, headers, message):
        myClassReBuild = json.loads(message)
        print(myClassReBuild)
        job = Job()
        job.__dict__ = myClassReBuild

        msg = "【平台】：" + job.web_type + "\n" \
                                       "【地址】：" + job.url + "\n" \
                                                           "【兼职类型】：" + job.type + "\n" \
                                                                                  "【兼职标题】：" + job.title + "\n" \
                                                                                                          "【兼职描述】：" + job.desc + "\n" \
                                                                                                                                 "【兼职发布时间】：" + job.publishtime

        qq.sendMes("827718520", msg)


# 推送到队列queue
def send_to_queue(msg):
    conn = stomp.Connection10([(ip, port)])
    conn.start()
    conn.connect()
    conn.send(queue_name, msg)
    conn.disconnect()


# 推送到主题
def send_to_topic(msg):
    conn = stomp.Connection10([(ip, port)])
    conn.start()
    conn.connect()
    conn.send(topic_name, msg)
    print(msg, "消息推送成功！")
    conn.disconnect()


##从队列接收消息
def receive_from_queue():
    conn = stomp.Connection10([(ip, port)])
    conn.set_listener(listener_name, javaListener())
    conn.start()
    conn.connect()
    conn.subscribe(queue_name)
    time.sleep(1)  # secs
    conn.disconnect()


##从主题接收消息
def receive_from_topic():
    conn = stomp.Connection10([(ip, port)])
    conn.set_listener(listener_name, javaListener())
    conn.start()
    conn.connect()
    conn.subscribe(topic_name)
    while 1:
        time.sleep(60)  # secs

    conn.disconnect()


if __name__ == '__main__':
    receive_from_topic()
