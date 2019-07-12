import json

from com.parttimejob.mq import Job

job = Job("猪八戒","JAVA","测试","0","asdfasdf()()、","2019-01-32 23:23","https://www.baidu.com")
s = json.dumps(job)
print(s)