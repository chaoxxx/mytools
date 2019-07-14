# coding:UTF-8

from com.parttimejob.mq.mq_util import MqUtil

# 广告
topic_name = '/topic/ad/topic'
header = 'ad'
mq_util = MqUtil()


# 推送到主题
def send_to_topic(msg):
    mq_util.send_to_topic(topic_name, msg)


if __name__ == '__main__':
    msg = '范品社 github 章鱼猫 开源程序员程序猿编程极客GEEK纯棉短袖T恤 \n【在售价】59.90元\n【下单链接】https://m.tb.cn/h.ehimzdV \n----------------- \n复制这条信息，￥zLOFYhRQvau￥，到【手机淘宝】即可查看'
    send_to_topic(msg)
