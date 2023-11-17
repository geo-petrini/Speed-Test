#!/usr/bin/python3

import sys, time
from socket import *
import argparse

count = 1000
BUFSIZE = 1024000

def client(ip, port):
    testdata = 'x' * (BUFSIZE-1) + '\n'
    t1 = time.time()    #start time
    if ip.count(':') > 1:
        s = socket(AF_INET6, SOCK_STREAM)
    else:
        s = socket(AF_INET, SOCK_STREAM)
    t2 = time.time() #socket time
    s.connect((ip, int(port)))
    t3 = time.time() #connect time
    i = 0
    while i < count:
        i = i+1
        s.send(bytearray(testdata,"utf-8"))
    s.shutdown(1)
    t4 = time.time() #send time
    data = s.recv(BUFSIZE)
    t5 = time.time() #receive time
    print ('Data sent (bytes): "{}"'.format( len(testdata) ))
    print ('Data received: "{}"'.format(data.decode("utf-8")))
    print ('Ping: {}'.format( (t3-t2)+(t5-t4)/2) )
    print ('Time: {}'.format( t4-t3) )
    print ('Bandwidth: {} Kb/sec'.format( round((BUFSIZE*count*0.001) / (t4-t3), 3),) )


def parseIp(ip):
    port = None
    if '.' in ip:
        #ipv4
        if ':' in ip:
            #ip and port
            port = ip.split(':')[1]
            ip = ip.split(':')[0]
    elif ('[' in ip and ']' in ip) or ip.count(':') > 1:
        #ipv6
        if ']:' in ip:
            #ip and port
            port = ip.split(']:')[1]
            ip = ip.split(']:')[0].replace('[', '')
            ip = f'[{ip}]'
    else:
        #hostname
        if ':' in ip:
            #ip and port
            port = ip.split(':')[1]            
            ip = ip.split(':')[0]
            
    return (ip, port)


def start():
    parser = argparse.ArgumentParser(description='Ping client')
    parser.add_argument('-s', '--server', default=None, help='Server hostname or ip')
    parser.add_argument('-p', '--port', default=None, help='Server port')
    args = parser.parse_args()
    ip = args.server
    port = args.port  
    
    if ip != None and port == None:
        (ip, port) = parseIp(ip)
    if ip == None: ip=input("ip: ")
    if port == None: port = input("Port: ")

    if len(ip)>0 and len(port)>0:
        print(f'Server: "{ip}:{port}"')
        client(ip, port)
    else:
        print(f'Invalid server: "{ip}:{port}"')

if __name__ == "__main__":
    start()
