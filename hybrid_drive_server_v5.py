import socket
import select
import pickle
import numpy as np
import matplotlib.pyplot as plt
import time

import tensorflow as tf
import tensorflow.keras as K
import tensorflow.keras.layers as ll
import tensorflow.keras.optimizers as optim
import tensorflow.keras.losses as losses

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import cv2

from helper import *

from Model3 import *

gpus = tf.config.experimental.list_physical_devices('GPU')
num_gpu = 1
memory_limit = 1024*8
if gpus :
    try :
        tf.config.experimental.set_virtual_device_configuration(gpus[num_gpu-1], [tf.config.experimental.VirtualDeviceConfiguration(memory_limit = memory_limit)])
        print("Use {} GPU limited {}MB memory".format(num_gpu, memory_limit))
    except RuntimeError as e :
        print(e)

net = Net()
tr = Trainer(net)

try:
    net.load_model('model_check_points')
    print("load successful")
except:
    pass
    print("Failed to load model")

HEADER_LENGTH = 10

PORT = 1234

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server_socket.bind((socket.gethostname(), PORT))

server_socket.listen()

sockets_list = [server_socket]

clients = {}
new_img = "True"

str_enc = str(0.0).encode('utf-8')

str_hdr =  f"{len(str(0.0)):<{HEADER_LENGTH}}".encode('utf-8')
training = False

def receive_message(client_socket):
    temp = b''
    try:
        message_header = client_socket.recv(HEADER_LENGTH)
        
        if not len(message_header):
            return False
        
        message_length = int(message_header.decode("utf-8"))
        while len(temp) < message_length:
            temp += client_socket.recv(message_length-len(temp))
        return {"header": message_header, "data": temp}
    except:
        return False

        
while True:
    read_sockets, _, exception_sockets = select.select(sockets_list, [], sockets_list)

    for notified_socket in read_sockets:
        if notified_socket == server_socket:
            client_socket, client_address = server_socket.accept()
            user = receive_message(client_socket)
            if user is False:
                    continue
	
            sockets_list.append(client_socket)

            clients[client_socket] = user

            print(f"Accepted new connection from {client_address[0]}:{client_address[1]} username:{user['data'].decode('utf-8')}")
	
        else:
            st = time.time()
            message = receive_message(notified_socket)

            if message is False:
                    print(f"Closed connection from {clients[notified_socket]['data'].decode('utf-8')}")
                    sockets_list.remove(notified_socket)
                    del clients[notified_socket]
                    continue
	
            user = clients[notified_socket]
            if user['data'].decode('utf-8') != 'car':
                print(f"Received message from {user['data'].decode('utf-8')}: {message['data'].decode('utf-8')}")
                
                if user['data'].decode('utf-8') == 'netStart':
                    if training:
                        if tr.index > 64:
                            tr.train()
                    training = False
                    _steering = message['data'].decode('utf-8')
                    _str_enc = str(_steering).encode('utf-8')

                    _str_hdr =  f"{len(str(_steering)):<{HEADER_LENGTH}}".encode('utf-8')

                if user['data'].decode('utf-8') == 'tutor':
                    training = True
                    _steering = message['data'].decode('utf-8')
                    _str_enc = str(_steering).encode('utf-8')

                    _str_hdr =  f"{len(str(_steering)):<{HEADER_LENGTH}}".encode('utf-8')

                
            else:
                print(f"Received message from {user['data'].decode('utf-8')}")
                img = pickle.loads(message['data'])
                if training:
                    tr.record(img, _steering)

                # Save img, _steering to log

                X = Warp(img, src, target)/256
                X_shape = X.shape
                X = X.reshape((1, X_shape[0], X_shape[1], X_shape[2]))

                output = net(X)
                output = np.array(output)
                steering = output[0,0]                

                print(f"Net: {50*steering:.2f}, Error: {50*(float(_steering)-steering):.2f}")

                #print(f"Tutor: {50*_steering:.2f} Net: {50*steering:.2f}")
                str_enc = str(steering).encode('utf-8')

                str_hdr =  f"{len(str(steering)):<{HEADER_LENGTH}}".encode('utf-8')
                print(f"fps ~ {1/(time.time()-st)}")
                #new_img = "True"

            for client_socket in clients:
                if client_socket != notified_socket:
                    if clients[client_socket]['data'] == 'car'.encode('utf-8'):
                        if not training:
                            client_socket.send(f"{len('net'):<{HEADER_LENGTH}}".encode('utf-8') + "net".encode('utf-8') + str_hdr + str_enc)
                        else:
                            client_socket.send(f"{len('net'):<{HEADER_LENGTH}}".encode('utf-8') + "net".encode('utf-8') + _str_hdr + _str_enc)

                
    for notified_socket in exception_sockets:
        sockets_list.remove(notified_socket)
        del clients[notified_socket]
	


