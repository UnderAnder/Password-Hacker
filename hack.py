import argparse
from socket import socket
from itertools import product


class TCPClient:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.socket = None

    def connect(self):
        if self.socket is None:
            self.socket = socket()
        self.socket.connect((self.host, self.port))

    def disconnect(self):
        self.socket.close()
        self.socket = None

    def send_data(self, data):
        if self.socket is None:
            self.connect()
        self.socket.send(data)

    def read_data(self):
        if self.socket is None:
            self.connect()
        return self.socket.recv(1024).decode()


class Passwords:
    def __init__(self, conn):
        self.conn = conn

    def brute_pass(self):
        for password in Passwords.generate_password():
            msg = ''.join(map(str, password)).encode()
            self.conn.send_data(msg)
            resp = self.conn.read_data()
            if resp == 'Connection success!':
                print(msg.decode())
                break

    @staticmethod
    def generate_password():
        index = 1
        while True:
            charset = 'abcdefghijklmnopqrstuvwxyz1234567890'
            yield from product(charset, repeat=index)
            index += 1


def main():
    parse_args = argparse.ArgumentParser()
    parse_args.add_argument('host', help='enter hostname')
    parse_args.add_argument('port', help='enter port number', type=int)
    args = parse_args.parse_args()

    conn = TCPClient(args.host, args.port)
    conn.connect()
    Passwords(conn).brute_pass()
    conn.disconnect()

if __name__ == '__main__':
    main()
