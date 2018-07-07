# -*- coding: utf-8 -*-
import socket,select,threading,time

petname_dict = {}
lock = threading.Lock()

class Server():
    connection_list = []
    host = ''
    def __init__(self,port):
        self.port = port
        self.server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_sock.setblocking(0)
        self.server_sock.bind((self.host, self.port))
        self.server_sock.listen(10)
        self.connection_list.append(self.server_sock)
        self.thread = threading.Thread(target=self.run)
        self.thread.start()


    def broad_cast(self, sock, message):
        for socket in self.connection_list:
            if socket != self.server_sock and socket != sock:
                try:
                    socket.send(message)
                except:
                    #print str(socket.getpeername()) + ' is offline'
                    socket.close()
                    self.connection_list.remove(socket)
            else:
                pass
    def run(self):
        global petname_dict
        while 1:
            readable, writable, error = select.select(self.connection_list, [], [])
            for sock in readable:
                if sock == self.server_sock:
                    connection, connection_add = sock.accept()
                    '''message = str(petname_dict[str(connection_add)]) + '进入了房间\n'
                    self.broad_cast(connection, message)'''
                    print connection_add, '%s connect'
                    self.connection_list.append(connection)
                else:
                    try:
                        date = sock.recv(1024)
                        #print str(petname_dict[str(sock.getpeername())]) + ': ' + date
                        self.broad_cast(sock, str(petname_dict[str(sock.getpeername())]) + ': ' + date)
                    except:
                        try:
                            message2 = ' ' + str(petname_dict[str(sock.getpeername())]) + ' ' + '离开了房间\n'
                            self.broad_cast(sock, message2)
                            print str(sock.getpeername()) + ' is offline'
                            lock.acquire()
                            del petname_dict[str(sock.getpeername())]
                            lock.release()
                            sock.close()
                            self.connection_list.remove(sock)
                        except:
                            petname_dict = {}
                        continue

class ConnectionListUpdate():
    connection_list = []
    host = ''
    petname_list = {}

    def __init__(self, port):
        self.port = port
        self.server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_sock.setblocking(0)
        self.server_sock.bind((self.host, self.port))
        self.server_sock.listen(10)
        self.connection_list.append(self.server_sock)
        self.thread1 = threading.Thread(target=self.receive)
        self.thread2 = threading.Thread(target=self.send)
        self.thread1.start()
        self.thread2.start()
    def broad_cast(self, message):
        for socket in self.connection_list:
            if socket != self.server_sock:
                try:
                    socket.send(message)
                except:
                    socket.close()
                    #print str(socket.getpeername())+' is offline'
                    self.connection_list.remove(socket)
            else:
                pass

    def receive(self):
        global petname_dict
        while 1:
            readable2, writable2, error2 = select.select(self.connection_list, [], [])
            for sock in readable2:
                if sock == self.server_sock:
                    try:
                        connection, connection_add = sock.accept()
                        self.connection_list.append(connection)
                    except:
                        pass
                else:
                    try:
                        petname = sock.recv(1024)
                        lock.acquire()
                        petname_dict[eval(petname)[0]] = eval(petname)[1]
                        lock.release()
                    except:
                        self.connection_list.remove(sock)

    def send(self):
        global petname_dict
        while 1:
            message = ''
            for key in petname_dict:
                message = message + petname_dict[key] + '\n'
            self.broad_cast(message)
            time.sleep(1)

server_message = Server(10001)
server_update = ConnectionListUpdate(20000)