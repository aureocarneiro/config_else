#!/usr/bin/python
# -*- coding: utf-8 -*-

# Modulos

import socket
import sys
import time

ip = str(sys.argv[1])

client_socket1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket1.connect((ip, 10001))

# funcão checksum
def format_message(message):
    checksum = ord(message[3]) ^ ord(message[4])
    for character in message[5:]:
        checksum ^= ord(character)
    return (message + "{0:02X}".format(checksum) + "\x03")


# funcoes de set

def set1():
    client_socket1.send(format_message("\x0201020SN240:015:003:001:090"))
    data = client_socket1.recv(1024)
    return data

def set2():
    client_socket1.send(format_message("\x0201024SL0003.80:0019.10:0057.40"))
    data = client_socket1.recv(1024)
    return data

resposta1 = set1()
time.sleep(1)
resposta2 = set2()
print(resposta1 + '\n============================\n')

if resposta1[7] == "\x06":
    print('SAMPLE NUMBER: Acknowledge')
elif resposta1[7] == "\x15":
    print('SAMPLE NUMBER: Not Acknowledge')
elif resposta1[7] == "\x05":
    print('SAMPLE NUMBER: Enquiry')

print(resposta2 + '\n============================\n')

if resposta2[7] == "\x06":
    print('THRESHOLD LEVEL: Acknowledge')
elif resposta2[7] == "\x15":
    print('THRESHOLD LEVEL: Not Acknowledge')
elif resposta2[7] == "\x05":
    print('THRESHOLD LEVEL: Enquiry')
