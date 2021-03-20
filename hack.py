import argparse
import socket


def main():
    parse_args = argparse.ArgumentParser()
    parse_args.add_argument("address")
    parse_args.add_argument("port")
    parse_args.add_argument("message")
    args = parse_args.parse_args()

    with socket.socket() as client_socket:
        hostname = args.address
        port = int(args.port)
        address = (hostname, port)

        client_socket.connect(address)

        data = args.message
        data = data.encode()

        client_socket.send(data)

        response = client_socket.recv(1024)

        response = response.decode()
        print(response)


if __name__ == '__main__':
    main()
