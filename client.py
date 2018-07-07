# -*- coding: utf-8 -*-
import socket, time, thread, Queue,tkFont,threading
from Tkinter import *
from tkSimpleDialog import askstring

class ClientUI():

    flag = 0
    flag_exit = 0
    lock = threading.Lock()

    host = 'localhost'
    port1 = 10001
    port2 = 20000
    client_sock1 = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    client_sock2 = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

    petname = '' #存放昵称

    #client_sock.setblocking(0)
    queue = Queue.Queue()
    queue2 = Queue.Queue()
    def __init__(self):

        # 创建昵称窗口
        self.root2 = Tk()
        self.label_root2 = Label(self.root2, text='\n欢迎使用SimpleChat聊天室\n').pack()
        self.bm = PhotoImage(file='chat.gif')
        self.label_img = Label(self.root2, imag=self.bm).pack()
        self.button_sendname = Button(self.root2, text='进入', command=self.pet_name_send).pack()

        # 创建字体
        ft1 = tkFont.Font(size = 20, weight = tkFont.BOLD)
        ft2 = tkFont.Font(size = 15, weight = tkFont.BOLD)
        ft3 = tkFont.Font(size = 10, weight = tkFont.BOLD)
        ft4 = tkFont.Font(size = 40, weight = tkFont.BOLD)

        #创建聊天窗口
        self.root = Tk()
        self.title = 'SimplCha'
        self.root.title(self.title)
        self.root.rowconfigure(0,weight = 1)
        self.root.columnconfigure(0,weight = 1)

        #self.root.rowconfigure(1, weight = 1)
        #self.root.columnconfigure(1, weight = 1)
        #创建几个窗口框架
        '''self.frame_top = Frame(bg='white')
        self.frame_mid = Frame(bg='white')
        self.frame_bottom = Frame(bg='gray')
        self.frame_right = Frame(bg = 'white')'''
        #创建消息显示框并绑定滚动条
        self.label1 = Label(self.root, text = '消息列表')
        self.text_msglist = Text(self.root, width=50, height=15, font = ft2)
        self.text_scrollbar = Scrollbar(self.root)
        self.text_msglist.focus_set()
        self.text_msglist['yscrollcommand'] = self.text_scrollbar.set
        self.text_scrollbar.config(command=self.text_msglist.yview)
        self.label1.grid(row = 1, column = 0)
        self.text_msglist.grid(row = 2, column = 0,sticky='nsew')
        self.text_scrollbar.grid(row=2, column=0, sticky='nse')
        # 创建消息输入框
        self.label2 = Label(self.root, text='输入信息')
        self.text_msg = Text(self.root, width=50, height=2,font = ft3)
        self.label2.grid(row = 3,sticky='nsew')
        self.text_msg.grid(row = 4,sticky='nsew')
        #创建成员显示列表
        self.label2 = Label(self.root, text='在线成员')
        self.text_member_scrollbar = Scrollbar(self.root)
        self.text_member = Text(self.root,width = 20,height = 25,font = ft1)
        self.text_member.focus_set()
        self.text_member['yscrollcommand'] = self.text_member_scrollbar.set
        self.text_member_scrollbar.config(command=self.text_member.yview)
        self.label2.grid(row = 1,column=1)
        self.text_member.grid(row = 2,column=1,sticky='nsw')
        self.text_member_scrollbar.grid(row=2, column=2, sticky='nse')
        # 创建消息发送按钮
        self.button_sendmsg = Button(self.root, text='发送', command=self.sendMessage)
        self.button_sendmsg.grid(row = 5, column = 0, sticky = W)
        #创建输入统计框
        self.count = '0'
        self.label_count = Label(self.root, text= '输入字数\n' + self.count,font = ft4)
        self.label_count.grid(row=4,column = 1)
        # 创建几个tag
        self.text_msglist.tag_config('green', foreground='green')
        self.text_msglist.tag_config('red', foreground='red')
        self.text_msglist.tag_config('yellow', foreground='#FFD700')
        self.text_msglist.tag_config('blue', foreground='#0000FF')
        self.text_member.tag_config('red', foreground='red')
        self.text_member.tag_config('blue', foreground='#0000FF')
        self.text_member.tag_config('yellow', foreground='#FFD700')

        self.root.withdraw()

        #创建线程
        '''self.thread1 = threading.Thread(target=self.receiveMessage)
        self.thread2 = threading.Thread(target=self.connection_list_update)
        self.thread3 = threading.Thread(target=self.root.after, args=(100,self.readQueue))
        self.thread4 = threading.Thread(target=self.input_count)'''

    def readQueue(self):
        try:
            msg2 = self.queue2.get(0)
            self.text_member.delete('0.0',END)
            self.text_member.insert(END, '我的昵称：\n', 'yellow')
            self.text_member.insert(END, self.petname, 'yellow')
            self.text_member.insert(END, '\n全体成员：\n')
            self.text_member.insert(END, msg2, 'blue')
        except:
            pass
        try:
            msg = self.queue.get(0)
            if msg[0] == 1:
                self.text_msglist.insert(END,msg[1],'red')
                self.text_msglist.insert(END,msg[2],'green')
            elif msg[0] == 2:
                self.text_msglist.insert(END, msg[1],'blue')
                self.text_msglist.insert(END, msg[2])
        except:
            pass
        self.root.after(100,self.readQueue)

    def receiveMessage(self):
            try:
                self.client_sock1.connect((self.host, self.port1))
                msg_sys = '系统消息:' + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + '\n'
                date = '连接成功\n'
                self.sock1_add = str(self.client_sock1.getsockname())
                msg = (1,msg_sys,date)
                self.queue.put(msg)
                # self.text_msglist.insert(END, msg_sys)
                #self.text_msglist.insert(END, '连接成功', 'green')
            except socket.error, e:
                msg_sys = '系统消息:' + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + '\n '
                self.text_msglist.insert(END, msg_sys,'red')
                self.text_msglist.insert(END, e , 'red')
                self.text_msglist.insert(END, '无法连接到服务器,请检查服务器是否启动\n', 'red')
            while 1:
                try:
                    buf = self.client_sock1.recv(1024) + '\n'
                    if len(buf):
                        msg_rcv = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + '\n\n'
                        msg = (2,msg_rcv,buf)
                        self.queue.put(msg)
                        #self.text_msglist.insert(END, msg_rcv, 'green')
                        #self.text_msglist.insert(END, buf)
                    else:
                        continue
                except:
                    pass

    def sendMessage(self):
        msg1 = '我 ' + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + '\n\n'
        self.lock.acquire()
        msg2 = self.text_msg.get('0.0', END) + '\n'
        self.lock.release()
        try:
            self.client_sock1.send(msg2.encode('utf-8'))
            self.text_msglist.insert(END, msg1, 'yellow')
            self.text_msglist.insert(END, msg2)
            self.text_msg.delete(0.0, END)
        except socket.error, e:
            msg_sys = '系统消息:' + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + '\n '
            self.text_msglist.insert(END, msg_sys,'red')
            self.text_msglist.insert(END, '发送失败，请检查网络设置', 'red')
            self.text_msg.delete(0.0, END)

    def connection_list_update(self):
        try:
            self.client_sock2.connect((self.host, self.port2))
        except socket.error, e:
            self.text_member.insert(END,e, 'red')
            self.text_member.insert(END,'\n列表刷新失败，请检查网络连接', 'red')
        while 1:
            try:
                buf = self.client_sock2.recv(1024)
                if len(buf):
                    self.queue2.put(buf)
                else:
                    continue
            except:
                pass

    def pet_name_send(self):
        self.petname = askstring("SimpleChat", "请输入昵称").encode('utf-8')
        msg = [str(self.client_sock1.getsockname()), self.petname]
        try:
            self.client_sock2.send(repr(msg))
            self.root2.destroy()
            self.root.deiconify()
            msg2 = '进入了房间'
            self.client_sock1.send(msg2)
            self.flag = 1
        except socket.error,  e:
            print e
    def input_count(self):
        while 1:
            if self.flag == 1:
                try:
                    time.sleep(0.5)
                    counter = str(len(self.text_msg.get('0.0', END)) - 1)
                    self.count = counter
                    self.label_count.config(text= '输入字数\n' + self.count)
                except:
                    pass

    def start(self):
        '''self.thread1.start()
        self.thread2.start()
        self.thread3.start()
        self.thread4.start()'''
        thread.start_new_thread(self.receiveMessage,())
        thread.start_new_thread(self.connection_list_update,())
        thread.start_new_thread(self.root.after,(100,self.readQueue))
        thread.start_new_thread(self.input_count,())

UI = ClientUI()
UI.start()
UI.root.mainloop()
