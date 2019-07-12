#windows下用python3.0操作windows api向记事本里面写入字符--发送汉字--正确的方式
import win32gui, win32con,time
import binascii #导入python的进制转换模块

astring = u'Hello World! 你好！'
astrToint = [ord(c) for c in astring]  #将字符串转换为整数型列表
#先手动打开一个记事本
#获取记事本中编辑控件的句柄
#hWndText = win32gui.FindWindow("#32769",u'张真')
hWndEdit = win32gui.FindWindowEx(8918386,None,"发送",None)
#获取窗口焦点
win32gui.SetForegroundWindow(8918386);
#给系统0.5s的响应时间
time.sleep(0.5)

#发送消息
for x in astrToint: #依次发送列表中的每个数字所代表的的字符
	win32gui.SendMessage(8918386,win32con.WM_CHAR,x, 0)






