# coding:UTF-8

import requests


def sendMes(group_id, msg):
    response = requests.get("http://127.0.0.1:5700/send_group_msg?group_id=" + group_id + "&message=" + msg)


def sendText(group_id):
    response = requests.get("http://127.0.0.1:5700/send_group_msg?group_id=" + group_id + "&message=世界你好 \n "
                                                                                          "hellow world！")

if __name__ == '__main__':
    sendText('827718520')
