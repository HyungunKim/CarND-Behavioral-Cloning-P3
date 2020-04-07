import socket
import select

import sys
import numpy as np

import time
from capnctrl import cap, ctrl

HEADER_LENGTH = 10
IP = "203.246.114.231"
PORT = 1234

my_username = 'tutor'
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((IP, PORT))
client_socket.setblocking(False)

username = my_username.encode('utf-8')
username_header = f"{len(username):<{HEADER_LENGTH}}".encode('utf-8')
client_socket.send(username_header + username)


my_username2 = 'net'
client_socket2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket2.connect((IP, PORT))
client_socket2.setblocking(False)

username2 = my_username2.encode('utf-8')
username_header2 = f"{len(username2):<{HEADER_LENGTH}}".encode('utf-8')
client_socket2.send(username_header2 + username2)


steering = 0
target = 0
m2s = {'a':-0.1, 'd':0.1}
training = True
key = 'f'
message = "True"
while True:
    key = cap.keyboard()

    try:
        # receive things
        username_header = client_socket.recv(HEADER_LENGTH)
        if not len(username_header):
            print("connection closed by the server")
            sys.exit()
            
        username_length = int(username_header.decode('utf-8'))
        username = client_socket.recv(username_length).decode('utf-8')
        if username == 'SERVER':
            message_header = client_socket.recv(HEADER_LENGTH)
            message_length = int(message_header.decode('utf-8'))
            message = client_socket.recv(message_length).decode('utf-8')


    except :
        pass

    for i in range(len(key)):
        try:
            if key[i] == 'q':
                target = target * 0.6
                training = True
            elif key[i] == 'e':
                """
                if training:
                    out_message = 'net'.encode('utf-8')
                    out_message_header = f"{len(out_message):<{HEADER_LENGTH}}".encode('utf-8')
                    client_socket.send(out_message_header + out_message)
                """
                training = False
            else:
                training = True
                target = target + m2s[key[i]]
            
        except:
            pass
        target = np.max([-0.5, target])
        target = np.min([0.5, target])
        steering = 0.8*steering + 0.2*target
        steering = np.max([-0.5, steering])
        steering = np.min([0.5, steering])

        if training:
            out_message = str(steering).encode('utf-8')
            out_message_header = f"{len(out_message):<{HEADER_LENGTH}}".encode('utf-8')
            client_socket.send(out_message_header + out_message)
            time.sleep(0.1)

        else:
            if message == "True":
                out_message = str(steering).encode('utf-8')
                out_message_header = f"{len(out_message):<{HEADER_LENGTH}}".encode('utf-8')
                client_socket2.send(out_message_header + out_message)
                time.sleep(0.1)