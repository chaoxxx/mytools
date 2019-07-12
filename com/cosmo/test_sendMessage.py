import win32gui
import win32con

win32gui.SetForegroundWindow(131686);

win32gui.SendMessage(131686,win32con.WM_SETTEXT, None, 'D:\\work\\pyworkspaces\\mytools\\com\\cosmo\\Test.py');
