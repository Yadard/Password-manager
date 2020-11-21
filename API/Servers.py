from socket import socket, gethostname, gethostbyname, AF_INET, SOCK_STREAM
from threading import Thread, active_count
from API.Core import *
import time


class Server:
    def __init__(self, HEADER: int, PORT: int, FORMAT: str):
        self.HEADER = HEADER
        self._PORT = PORT
        self.FORMAT = FORMAT
        self.SERVER = gethostbyname(gethostname())
        self.DISCONNECT = '!DISCONNECT'
        print(self.SERVER)
        self._ADDR = (self.SERVER, self._PORT)
        self.server = socket(AF_INET, SOCK_STREAM)
        self.server.bind(self._ADDR)
        self.users = dict()
        self.message = ''

    def start(self):
        x = 0
        self.server.listen()
        while True:
            conn, addr = self.server.accept()
            self.users.update({x: conn})
            receiver = Thread(target=self.handle_client, args=(conn, addr, x))
            receiver.start()
            sender = Thread(target=self.send_msg, args=(x, 'twitter'))
            sender.start()
            x += 1
            print(f'[ACTIVE CONNECTIONS] {active_count()}')

    def handle_client(self, conn, addr, x):
        connected = True
        print(f'[User] addr = {addr}, ID = {self.users[x]}')
        while connected:
            msg_length = conn.recv(self.HEADER).decode(self.FORMAT)
            if msg_length:
                msg_length = int(msg_length)
                msg = conn.recv(msg_length).decode(self.FORMAT)
                print(msg)
                if msg == self.DISCONNECT:
                    connected = False
        conn.close()

    def send_msg(self, index: int, website):
        conn = self.users[index]
        manager = Password()
        conn.send(manager.get_password(website=website).encode(self.FORMAT))
        print(time.time())
        conn.close()


server = Server(64, 5050, 'utf-8')
server.start()
if server.message != "":
    server.send_msg(server.users[0], 'twitter')
