'''
TCP Server Version 1.0
2018.12.12
York
    js = json.dumps({
        "From": "Server",   # send information terminal
        "SendTo": contact,  # recive information terminal
        "Time": ctime()     # sending time
        "Type": "command",    # information type
        "Status": "Success" # reply status
        "Command": {
           "Kind":1,  # video 1,img 2,ppt 3,serialport 4, wel 5
           "Order":2  # open 1,play/pause 2, stop3, fullscreen 4,voiceup 5, voicelow 6, Mute 7, speed up 8,  speed low 9, speed normal 10, next 11, previous 12
          } # command 
        "Msg": server_msg,  # message
        })
'''

import selectors
import queue
import os
import threading
import socket
from tkinter import *
from time import ctime
import time
import json
import configparser
# import jsonpath  # python--- JsonPath从多层嵌套Json中解析所需要的值 jsonpath.jsonpath(dic,'$..name')   #不管有多少层，写两个.都能取到
from control import Getcontrol
import wel

BUFSIZE = 1024

# lock = threading.Lock()    # Global Lock
que = queue.Queue(4096)


class GUI(object):
    '''
    This is the top module. It interacts with users. When a button is clicked
    or Return is pressed, a corresbonding event trigered. Connect is used to 
    estanblish a TCP connection with server while Log In tells server a user
    comes. We also provide an Add button, which allows user to add contacts.
    All the contacts will be displayed in a list box, and a double click on
    each contact will direct the user's message to a specific contact.
    Note that this module is based on other modules like Send and Recv, so it
    is not concerned with send and receive details. In fact it is wisdom to
    throw this burden to others. We just do what we can and do it perfectly.
    '''

    def __init__(self):
        self.root = Tk()

        self.root.title('三棱中控系统')
        self.frame_lft = Frame(self.root)
        self.frame_rgt = Frame(self.root)
        self.frame_lft.grid(row=0, column=0)
        self.frame_rgt.grid(row=0, column=1)
        self.entry_msg = Entry(self.frame_lft, width=46)  # entry, collect input
        self.entry_msg.grid(row=1, column=0)
        self.entry_msg.bind('<Return>', self.send_method)

        self.scrollbar_txt = Scrollbar(self.frame_lft, width=1)
        self.scrollbar_txt.grid(row=0, column=2, sticky=W + N + S)

        # self.button_qit = Button(self.root, text='Quit', command=self.root.quit)
        # self.button_qit.pack()

        self.text_msg = Text(self.frame_lft, state=DISABLED, width=49, wrap=WORD)  # text, display message
        self.text_msg.config(font='Fixedsys')
        self.text_msg.grid(row=0, column=0, columnspan=2, sticky=W + N + S + E)
        self.text_msg.config(yscrollcommand=self.scrollbar_txt.set)
        self.scrollbar_txt.config(command=self.text_msg.yview)

        self.entry_IP = Entry(self.frame_rgt, width=14)  # an IP address is supposed to input here
        self.entry_IP.grid(row=0, column=0, padx=5, pady=0)
        self.entry_IP.bind('<Return>', self.connect_method)
        self.entry_IP.insert(END, IP)

        self.button_cnt = Button(self.frame_rgt, text='连接',
                                 command=self.connect_method)  # click this button to connect
        self.button_cnt.config(height=1, width=8)
        self.button_cnt.grid(row=0, column=1, padx=0, pady=0)

        self.button_snd = Button(self.frame_lft, height=1, text='发送', command=self.send_method)
        self.button_snd.config(width=8)
        self.button_snd.grid(row=1, column=1)

        # New features in version 2.2 ##
        self.entry_log = Entry(self.frame_rgt, width=14)  # log in
        self.entry_log.grid(row=1, column=0, padx=5, pady=0)
        self.entry_log.bind('<Return>', self.login_method)
        self.entry_log.insert(END, ID)

        self.entry_port = Entry(self.frame_rgt, width=14)  # log in
        self.entry_port.grid(row=2, column=0, padx=5, pady=0)
        self.entry_port.insert(END, PORT)

        self.label_cat = Label(self.frame_rgt, text=' 端口号')
        self.label_cat.grid(row=2, column=1, sticky=W)

        self.button_log = Button(self.frame_rgt, text='登录',
                                 command=self.login_method)  # first click means log in, second means log out
        self.button_log.config(width=8)
        self.button_log.grid(row=1, column=1, sticky=W)

        self.listbox_cat = Listbox(self.frame_rgt, height=15, width=24)
        self.listbox_cat.insert(END, '000000')
        self.listbox_cat.grid(row=4, column=0, columnspan=2, padx=5, sticky=N + S + E)
        self.listbox_cat.bind('<Double-1>', self.contact_method)

        self.scrollbar_cat = Scrollbar(self.frame_rgt, width=1)
        self.scrollbar_cat.grid(row=4, column=2, sticky=W + N + S)
        self.scrollbar_cat.config(command=self.listbox_cat.yview)
        self.listbox_cat.config(yscrollcommand=self.scrollbar_cat.set)

        self.entry_add = Entry(self.frame_rgt, width=14)
        self.entry_add.grid(row=5, column=0, padx=5, pady=0)
        self.entry_add.bind('<Return>', self.add_method)

        self.button_add = Button(self.frame_rgt, width=8, text='添加')
        self.button_add.config(command=self.add_method)
        self.button_add.grid(row=5, column=1)

        self.label_cat = Label(self.frame_rgt, text='联系人')
        self.label_cat.grid(row=3, column=0, sticky=W)
        self.root.attributes("-alpha", 0)
        self.root.iconbitmap('logo.ico')
        self.root.resizable(width=False, height=False)

    def connect_method(self, ev=None):
        # global IP
        # IP = self.entry_IP.get()  # 改為讀取配置文件
        self.connt = Connt(IP)  # make an instance of Connt class
        try:
            self.connt()  # establish connection
            # self.button_cnt.config(state=DISABLED)
            self.entry_IP.config(state=DISABLED)
            self.send = Send(self.connt.tcpCliSock)  # make an instance of Send class
            self.recv = Recv(self.connt.tcpCliSock)  # make an instance of Recv class
            self.recv_thread = threading.Thread(target=self.recv)  # a new thread, dealing with receiving
            self.recv_thread.daemon = True
            self.recv_thread.start()
            self.root.after(200, self.recv_method)
            self.button_cnt.config(text='断开连接', command=self.disconnect_method)
            self.entry_IP.config(state=DISABLED)
            self.login_method(None)
        except:
            print('connect server ' + IP + ' at port ' + PORT + ' erro!')
            print('disconnect to restart...')
            print('10秒后,程序将结束...')
            time.sleep(10)
            restart_program()

    def disconnect_method(self, ev=None):
        self.connt.tcpCliSock.shutdown(2)
        self.connt.tcpCliSock.close()
        self.button_cnt.config(text='连接', command=self.connect_method)
        self.entry_IP.config(state=NORMAL)

    def login_method(self, ev=None):
        global User
        User = self.entry_log.get()
        js = json.dumps({
            "From": User,
            "SendTo": "server",
            "Time": ctime(),
            "Type": "Login",
            "Status": "Success",
            "Command": "login",
            "Msg": "none"
        })
        self.send.send(js)  # this action is infalliable
        self.button_log.config(text='退出登录', command=self.logout_method)
        self.entry_log.config(state=DISABLED)

    def logout_method(self, ev=None):
        js = json.dumps({
            "From": User,
            "SendTo": "server",
            "Time": ctime(),
            "Type": "Logout",
            "Status": "Success",
            "Command": "logout",
            "Msg": "none"
        })
        self.send.send(js)
        self.button_log.config(text='登录', command=self.login_method)
        self.entry_log.config(state=NORMAL)

    def contact_method(self, ev=None):
        ID = self.listbox_cat.get(self.listbox_cat.curselection())
        js = json.dumps({
            "From": User,
            "SendTo": ID,
            "Time": ctime(),
            "Type": "Connect",
            "Status": "Success",
            "Command": "connect",
            "Msg": "none"
        })
        self.send.send(js)
        self.text_msg.delete(1.0, END)  # delete all text
        self.text_msg.config(state=NORMAL)
        self.text_msg.insert(END, '[to ' + ID + ' ' + ctime() + ']\n')
        # if this contact action fails, server will send an error message.

    def add_method(self, ev=None):
        ID = self.entry_add.get()
        if re.match(r'[0-9]{6}', ID) == None:
            pass
        else:
            self.listbox_cat.insert(END, ID)

    def send_method(self, ev=None):
        data = self.entry_msg.get()
        self.entry_msg.delete(0, END)
        if not data:
            pass
        else:
            self.text_msg.config(state=NORMAL)
            self.text_msg.insert(END, data + '\n')
            self.text_msg.config(state=DISABLED)
            self.text_msg.see(END)
            js = json.dumps({
                "From": User,
                "SendTo": "none",
                "Time": ctime(),
                "Type": "SendMsg",
                "Status": "Success",
                "Command": {"Kind": 1, "Order": 1},
                "Msg": data
            })
            self.send.send(js)

    def recv_method(self):
        try:
            data = que.get(block=False)
        except:
            pass
        else:
            self.text_msg.config(state=NORMAL)
            self.text_msg.insert(END, data + '\n')
            self.text_msg.config(state=DISABLED)
            self.text_msg.see(END)
            if re.match(r'^FROME', data):  # log in failed
                self.entry_log.config(state=NORMAL)
                self.button_log.config(text='log in', command=self.login_method)

        self.root.after(200, self.recv_method)  # runs every 200ms


class Send(object):
    '''
    This module deals with every detail in sending bytes through a socket, 
    such as lock, encode, blocking, etc, and provide a send interface for
    GUI module.
    '''

    def __init__(self, fd):
        self.fd = fd
        self.sel = selectors.DefaultSelector()
        self.sel.register(self.fd, selectors.EVENT_WRITE)

    def send(self, data):
        self.sel.select()  # wait until the socket is ready to write
        # if lock.acquire():
        self.fd.send(bytes(data, 'utf-8'))
        # lock.release()
        # else:
        #    pass


class Recv(object):
    '''
    This module deals with every detail in receiving bytes from a socket,
    and providing a friendly recv interface for GUI module.
    '''

    def __init__(self, fd):
        self.fd = fd
        self.sel = selectors.DefaultSelector()
        self.sel.register(self.fd, selectors.EVENT_READ)

    def recv(self):
        while True:
            self.sel.select()
            # if lock.acquire():
            try:
                msg = self.fd.recv(BUFSIZE).decode('utf-8')
                js = json.loads(msg)
                JsonStr = json.dumps(js)
                arr = json.loads(JsonStr)
                msgtype = js["Type"]
                if msgtype == 'Command':
                    Command = arr["Command"]
                    getcontrol = Getcontrol(Command)
                    getcontrol()
                elif msgtype == 'Wel':
                    Msg = js['Msg']
                    print(Msg)
                    tem = Msg.split(',')
                    wel.new_image(1600, 900, tem[0], tem[1], tem[2], show_image=False)
                else:
                    data = '[' + 'from ' + js["From"] + ' ' + js["Time"] + ']\n' + js["Msg"]
                    que.put(data)
                    # lock.release()
                    # else:
                    # pass
            except:
                print('disconnect to restart...')
                print('10秒后,程序将结束...')
                time.sleep(10)
                restart_program()

    def __call__(self):
        self.recv()


class Connt(object):
    '''
    This module deals with establishing a TCP connection with host.
    '''

    def __init__(self, IP):
        self.HOST = IP
        self.PORT = int(PORT)
        self.ADDR = (self.HOST, self.PORT)
        self.tcpCliSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self):
        self.tcpCliSock.connect(self.ADDR)

    def __call__(self):
        self.connect()


def main():
    global gui
    gui = GUI()
    gui.connect_method(None)
    gui.root.mainloop()


def file_name(file_dir):
    for root, dirs, files in os.walk(file_dir):
        print(root)  # 当前目录路径
        print(dirs)  # 当前路径下所有子目录
        print(files)  # 当前路径下所有非目录子文件


def restart_program():
    client = sys.executable
    os.execl(client, client, *sys.argv)


def socketstart():
    global IP, PORT, ID
    cf = configparser.ConfigParser()

    cf.read(r'.\setting.ini')
    # 获取所有section，返回值为list
    secs = cf.sections()
    print(secs)

    # 获取db中的所有属性名
    dboption = cf.options('set')
    print(dboption)

    # 获取db中的键值对
    dbitem = cf.items('set')
    print(dbitem)

    # 写配置文件
    # cf.set('set', 'id', '111111')
    # cf.write(open(r'.\PCControl\setting.ini', 'w'))

    # 获取section为set，属性名为host的值
    IP = cf.get('set', 'host')
    PORT = cf.get('set', 'port')
    ID = cf.get('set', 'id')
    print('Host:' + IP + '  Port:' + PORT + '  id:' + ID)
    # file_name('G:\img') # 获取 指定文件夹下 文件名
    main()


if __name__ == '__main__':
    socketstart()
