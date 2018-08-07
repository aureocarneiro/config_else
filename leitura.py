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

# funcoes de leitura

def cnct(msgm):
    client_socket1.send(format_message(msgm))
    data = client_socket1.recv(1024)
    return data

type = ''
sense = ''
dados1 = cnct("\x0201001GM")
time.sleep(1)
dados2 = cnct("\x0201001GK")
time.sleep(1)
dados3 = cnct("\x0201001GN")
time.sleep(1)
dados4 = cnct("\x0201001GL")

# mensagem crua
print("\n" + dados1 + "\n" + dados2 + "\n" + dados3 + "\n" + dados4 + "\n" + "============================" + "\n")

if dados2[8] == "0":
    type = "ION CHAMBER"
elif dados2[8] == "1":
    type = "NEUTRON Bf3"
elif dados2[8] == "2":
    type = "PROPORTINAL C"
elif dados2[8] == "3":
    type = "GEIGER MULLER"
elif dados2[8] == "4":
    type = "NEUTRON He3"
elif dados2[8] == "5":
    type = "TESTE INPUT"

if dados2[23] == "0":
    sense = "10 nSv/h"
elif dados2[23] == "1":
    sense = "100 nSv/h"
elif dados2[23] == "2":
    sense = "1 uSv/h"
elif dados2[23] == "3":
    sense = "10 uSv/h"
elif dados2[23] == "4":
    sense = "1 nSv/h"

# mensagem filtrada
print('ICP parameters \nDETECTOR TYPE = ' + type + '\nINTR. BACKGND = ' + dados3[20:24] + '\n1º SAMPLE N. = ' + dados4[8:11])
print('2º SAMPLE N. = ' + dados4[12:15] + '\n3º SAMPLE N. = ' + dados4[16:19] + '\n4º SAMPLE N. = ' + dados4[20:23])
print('1º THR LEVEL = ' + dados1[8:15] + '\n2º THR LEVEL = ' + dados1[16:23] + '\n3º THR LEVEL = ' + dados1[24:31])
print('MEASURE UNIT = uSv/h' + '\nIC MIN SENS = ' + sense + '\nFALLING THRESHOLD LEVEL(%) = ' + dados4[24:27])
print('\n============================\n')
