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
        self.socket.send(data.encode())

    def read_data(self):
        if self.socket is None:
            self.connect()
        return self.socket.recv(1024).decode()


class Passwords:
    def __init__(self, conn):
        self.conn = conn

    def brute_password(self):
        for password in Passwords.generate_password():
            if self.check_password(''.join(map(str, password))):
                print(password)
                break

    def dict_mod(self, dictionary):
        with open(dictionary, 'r') as dictionary:
            for password in Passwords.case_swith(dictionary):
                if self.check_password(password):
                    print(password)
                    break

    @staticmethod
    def case_swith(dictionary):
        for password in dictionary:
            password = password.strip("\n")
            if password.isdecimal():
                yield password
            else:
                for val in product(*([letter.lower(), letter.upper()] for letter in password)):
                    yield ''.join(val)

    def check_password(self, password):
        self.conn.send_data(password)
        resp = self.conn.read_data()
        if resp == 'Connection success!':
            return password
        if resp == 'Too many attempts':
            return 'Too many attempts'
        return False

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
    Passwords(conn).dict_mod('passwords.txt')
    conn.disconnect()


if __name__ == '__main__':
    main()
