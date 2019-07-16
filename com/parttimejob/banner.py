# coding:UTF-8
from com.parttimejob import qq

if __name__ == '__main__':
    group_list = qq.get_group_list()
    for group in group_list:
        key = str(group['group_id'])
        msg = "本号的功能是将全网的发包情况第一时间通知给群里的小伙伴。\n目前接入的平台有：\n1、猪八戒\n2、一品威客\n3、码市\n4、码易\n5、开源众包\n6、智城\n本号[3531939695]为自动程序。将本号邀请进入qq群后将会自动提供服务。本号提供的一切服务均为免费。"
        qq.sendMes(key,msg)
