# coding:UTF-8
import json

from com.parttimejob import qq
from com.parttimejob.mq import dev_producer, ad_producer
from com.parttimejob.mq.Job import Job


class MqListener(object):

    def __init__(self, group_no):
        self.group_no = group_no

    def on_message(self, headers, message):
        header = headers['destination']
        if header == dev_producer.topic_name:
            myClassReBuild = json.loads(message)
            job = Job()
            job.__dict__ = myClassReBuild
            message = "【平台】：" + job.web_type + "\n" \
                                               "【地址】：" + job.url + "\n" \
                                                                   "【兼职类型】：" + job.type + "\n" \
                                                                                          "【兼职标题】：" + job.title + "\n" \
                                                                                                                  "【兼职描述】：" + job.desc + "\n" \
                                                                                                                                         "【兼职发布时间】：" + job.publishtime
        else:
            pass

        qq.sendMes(self.group_no, message)
