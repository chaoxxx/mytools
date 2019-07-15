# coding:UTF-8
import json
import time
import urllib

import jsonpath
import requests


def sendMes(group_id, msg):
    msg = urllib.parse.quote(msg)

    url = "http://127.0.0.1:5700/send_group_msg?group_id=" + group_id + "&message=" +msg
    response = requests.get(url)
    if response.status_code != 200:
        print("消息推送失败")


def sendText(group_id):
    response = requests.get("http://127.0.0.1:5700/send_group_msg?group_id=" + group_id + "&message=世界你好 \n "
                                                                                          "hellow world！")

def get_group_list():
    url = "http://127.0.0.1:5700/get_group_list"
    response = requests.get(url)
    dict = json.loads(response.text)
    data = jsonpath.jsonpath(dict, "$.data")[0]
    return data


if __name__ == '__main__':
    # sendMes('827718520','你好啊')

    print(get_group_list())