#!/usr/bin/python3

import sys, time
from socket import *
import threading
import argparse

BUFSIZE = 1024000

def server(port):
    s = socket(AF_INET, SOCK_STREAM)
    s.bind(('', int(port)))
    s.listen(1)
    print ('Server ready...')
    while 1:
        conn, (host, remoteport) = s.accept()
        datasize = 0
        while 1:
            data = conn.recv(BUFSIZE)
            if not data:
                break
            else:
                datasize += len(data)
            del data
        conn.send(b'OK')
        conn.close()
        print (f'Done with {host} port {remoteport} datasize {datasize}')


def start():
    parser = argparse.ArgumentParser(description='Ping server')
    parser.add_argument('-p', '--port', default=None, help='Input port')
    args = parser.parse_args()
    port = args.port  
    print(f'port {port}')
    if port == None: port = input("Port: ")
    if len(port)>0:
        server(port)
    else:
        print(f'Invalid port: "{port}"')

if __name__ == "__main__":
    start()
