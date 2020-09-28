import socket
import random
import argparse
import sys
import time

MAX_BYTES = 65535


class Interval:
    def __init__(self, interval):
        if interval == 1:
            self.__max_wait = 2
            self.__increase = 2
        elif interval == 2:
            self.__max_wait = 4
            self.__increase = 3
        else:
            self.__max_wait = 1
            self.__increase = 2

    def get_max_wait(self):
        return self.__max_wait

    def get_increase(self):
        return self.__increase


def get_interval():
    t = time.localtime()
    current_time = time.strftime("%H:%M:%S", t)

    if 12 <= int(current_time[:2]) < 17:
        return 1
    elif 17 <= int(current_time[:2]) <= 23:
        return 2
    else:
        return 3


class Server:
    def __init__(self, interface, port):
        self.interface = interface
        self.port = port

    def run(self):
        soc = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        soc.bind((self.interface, self.port))
        print(f"Server binds with {soc.getsockname()}")

        while True:
            data, address = soc.recvfrom(MAX_BYTES)
            if random.random() < 0.5:
                print(f"Pretending to drop packet from {address}")
                continue
            data = data.decode('ascii')
            print(f"The client at {address} says {data}")
            msg = "Welcome to Spotify. Enjoy music!"
            msg = msg.encode('ascii')
            soc.sendto(msg, address)


class Client:
    def __init__(self, hostname, port):
        self.hostname = hostname
        self.port = port

    def run(self):
        soc = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        hostname = sys.argv[2]
        soc.connect((self.hostname, self.port))
        print("Connected")

        delay = 0.1
        msg = "Hello Spotify. Thank you for enjoyable musics!"
        msg = msg.encode('ascii')
        time = Interval(get_interval())
        while True:
            soc.send(msg)
            print(f"Waiting up to {delay} seconds for reply")
            soc.settimeout(delay)
            try:
                data = soc.recv(MAX_BYTES)
            except socket.timeout:
                delay *= time.get_increase()
                if delay > time.get_max_wait():
                    raise RuntimeError("Sorry, try again to connect Spotify")
            else:
                break
        data = data.decode('ascii')
        print(data)


def main():

    choises = {'server': Server, 'client': Client}
    parser = argparse.ArgumentParser(description="Spotify server")
    parser.add_argument("role", choices=choises)
    parser.add_argument(
        "ip", type=str, metavar="IP_ADDRESS", default="127.0.0.1")
    parser.add_argument("p", type=int, metavar="PORT", default=3030)

    args = parser.parse_args()

    clss = choises[args.role](args.ip, args.p)
    clss.run()


if __name__ == '__main__':
    main()
