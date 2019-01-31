"""附个键位码表：
字母和数字键     数字小键盘的键       功能键         其它键 
      键   键码   键   键码     键   键码    键      键码 
      A   65       0   96        F1   112     Backspace    8 
      B   66       1   97        F2   113     Tab       9 
      C   67       2   98        F3   114     Clear      12 
      D   68       3   99        F4   115     Enter      13 
      E   69       4   100       F5   116     Shift      16 
      F   70       5   101       F6   117     Control     17 
      G   71       6   102       F7   118      Alt       18 
      H   72       7   103       F8   119     Caps Lock    20 
      I   73       8   104       F9   120     Esc       27 
      J   74       9   105       F10  121     Spacebar    32 
      K   75       *   106       F11  122     Page Up     33 
      L   76       +   107       F12  123     Page Down    34 
      M   77       Enter 108       --   --      End       35 
      N   78       -   109       --   --       Home      36 
      O   79       .   110       --   --      Left Arrow   37 
      P   80       /   111       --   --      Up Arrow    38 
      Q   81       --   --       --   --      Right Arrow   39 
      R   82       --   --       --   --      Down Arrow    40 
      S   83       --   --       --   --      Insert      45 
      T   84       --   --       --   --      Delete      46 
      U   85       --   --       --   --      Help       47 
      V   86       --   --       --   --      Num Lock     144 
      W   87          
      X   88      
      Y   89      
      Z   90      
      0   48      
      1   49      
      2   50       
      3   51       
      4   52       
      5   53       
      6   54       
      7   55       
      8   56       
      9   57"""
# import win32gui  # 导入包
# import win32con
import time
import os
import win32api
import configparser
import serial  # 导入serial包


class Getcontrol(object):

    def __init__(self, js):
        self.Command = js

    def __call__(self):
        self.control()

    def control(self):
        kind = self.Command["Kind"]
        order = self.Command["Order"]
        if (kind == 1):
            self.function('mv' + str(order))
        elif (kind == 2):
            self.function('img' + str(order))
        elif (kind == 3):
            self.function('ppt' + str(order))
        elif (kind == 4):
            self.function('com' + str(order))
        elif (kind == 5):
            self.function('wel' + str(order))

    # 自己定义的用来实现switch-case的方法

    def function(self, x):
        swicher = {  # 定义一个map，相当于定义case：func()
            'mv1': self.funmv1,
            'mv2': self.funmv2,
            'mv3': self.funmv3,
            'mv4': self.funmv4,
            'mv5': self.funmv5,
            'mv6': self.funmv6,
            'mv7': self.funmv7,
            'mv8': self.funmv8,
            'mv9': self.funmv9,
            'mv10': self.funmv10,
            'mv11': self.funmv11,
            'mv12': self.funmv12,
            'img1': self.funimg1,
            'img2': self.funimg2,
            'img3': self.funimg3,
            'img4': self.funimg4,
            'img5': self.funimg5,
            'img6': self.funimg6,
            'img7': self.funimg7,
            'ppt1': self.funppt1,
            'ppt2': self.funppt2,
            'ppt3': self.funppt3,
            'ppt4': self.funppt4,
            'ppt5': self.funppt5,
            'ppt6': self.funppt6,
            'com1': self.funcom1,
            'wel1': self.funwel1,
            'wel2': self.funwel2,
            '13': lambda: print('default function')
        }
        func = swicher.get(x, '12')  # 从map中取出方法
        return func()  # 执行

    def funmv1(self):

        os.startfile(pathMV)
        time.sleep(1)
        win32api.keybd_event(32, 0, 0, 0)  # space 播放
        win32api.keybd_event(13, 0, 0, 0)  # enter 全屏

    def funmv2(self):
        win32api.keybd_event(32, 0, 0, 0)  # space 播放/暂停

    def funmv3(self):
        win32api.keybd_event(115, 0, 0, 0)  # F4 关闭播放

    def funmv4(self):
        win32api.keybd_event(13, 0, 0, 0)  # enter 全屏切换

    def funmv5(self):
        win32api.keybd_event(38, 0, 0, 0)  # up Arrow  音量+

    def funmv6(self):
        win32api.keybd_event(40, 0, 0, 0)  # up Arrow  音量-

    def funmv7(self):
        win32api.keybd_event(77, 0, 0, 0)  # m  静音

    def funmv8(self):
        win32api.keybd_event(67, 0, 0, 0)  # c  加速

    def funmv9(self):
        win32api.keybd_event(88, 0, 0, 0)  # x  减速

    def funmv10(self):
        win32api.keybd_event(90, 0, 0, 0)  # z  正常速度

    def funmv11(self):
        win32api.keybd_event(33, 0, 0, 0)  # pgup  下一个

    def funmv12(self):
        win32api.keybd_event(34, 0, 0, 0)  # pgdn  上一个

    def funimg1(self):
        os.startfile(pathIMG)
        time.sleep(1)
        win32api.keybd_event(117, 0, 0, 0)  # F5 幻灯片

    def funimg2(self):
        win32api.keybd_event(107, 0, 0, 0)  # + 放大

    def funimg3(self):
        win32api.keybd_event(109, 0, 0, 0)  # - 缩小

    def funimg4(self):
        win32api.keybd_event(37, 0, 0, 0)  # pgdn  上一张

    def funimg5(self):
        win32api.keybd_event(39, 0, 0, 0)  # pgup  下一张

    def funimg6(self):
        win32api.keybd_event(27, 0, 0, 0)  # esc  退出

    def funimg7(self):
        win32api.keybd_event(117, 0, 0, 0)  # enter  全屏

    def funppt1(self):
        os.startfile(pathPPT)
        time.sleep(1)
        win32api.keybd_event(116, 0, 0, 0)  # F5 幻灯片

    def funppt2(self):
        win32api.keybd_event(33, 0, 0, 0)  # pgdn  上一张

    def funppt3(self):
        win32api.keybd_event(34, 0, 0, 0)  # pgup  下一张

    def funppt4(self):
        win32api.keybd_event(36, 0, 0, 0)  # home  第一张

    def funppt5(self):
        win32api.keybd_event(35, 0, 0, 0)  # end  最后一张

    def funppt6(self):
        win32api.keybd_event(27, 0, 0, 0)  # e  退出

    def funwel1(self):
        os.startfile(pathWel)
        time.sleep(1)
        win32api.keybd_event(117, 0, 0, 0)  # F5 幻灯片

    def funwel2(self):
        win32api.keybd_event(27, 0, 0, 0)  # esc  退出

    def funcom1(self):
        try:
            s.isOpen()
            s.write(('test:from com3' + '\n').encode())
        except:
            print('fail in send, check com')


cf = configparser.ConfigParser()

cf.read(r'.\setting.ini')
# 获取所有section，返回值为list
secs = cf.sections()
print(secs)

# 获取db中的所有属性名
dboption = cf.options('source')
print(dboption)

# 获取db中的键值对
dbitem = cf.items('source')
print(dbitem)

# 获取section为set，属性名为host的值
pathMV = cf.get('source', 'pathMV')
pathIMG = cf.get('source', 'pathIMG')
pathPPT = cf.get('source', 'pathPPT')
pathWel = cf.get('source', 'pathWel')

com = cf.get('serial', 'com')

try:
    s = serial.Serial(com, 9600, timeout=2)  # 打开串口，配置串口
except:
    print(com + ' Open failure')

# print(u'窗口句柄')
# hwnd_title = dict()
#
#
# def get_all_hwnd(hwnd, mouse):
#     if win32gui.IsWindow(hwnd) and win32gui.IsWindowEnabled(hwnd) and win32gui.IsWindowVisible(hwnd):
#         hwnd_title.update({hwnd: win32gui.GetWindowText(hwnd)})
#
#
# win32gui.EnumWindows(get_all_hwnd, 0)
#
# for h, t in hwnd_title.items():
#     if t is not "":
#         print(h, t)
# os.startfile(u"D:\\PotPlayer\\PotPlayerMini64.exe")   # 打开文件  获取焦点

# while True:
#     os.startfile(u"D:\\PotPlayer\\PotPlayerMini64.exe")
#     wnd = win32gui.FindWindow(None, "智慧家庭.mov - PotPlayer")   # 一打开qq 就获取句柄

#     win32gui.ShowWindow(wnd, win32con.SW_SHOW)  # 显示 获取焦点
#     time.sleep(1)

#     win32api.keybd_event(32, 0, 0, 0)  # space 播放
#     time.sleep(1)

#     win32api.keybd_event(13, 0, 0, 0)  # enter 全屏
#     time.sleep(1)

#     win32api.keybd_event(13, 0, 0, 0)  # enter 缩小画面
#     time.sleep(1)

#     win32gui.ShowWindow(wnd, win32con.SW_HIDE)  # 隐藏
#     time.sleep(1)   # 持续时间
#     win32gui.SendMessage(wnd, win32con.WM_CLOSE)   # 关闭窗口
