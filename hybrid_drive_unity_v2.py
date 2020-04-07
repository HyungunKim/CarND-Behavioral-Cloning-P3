import argparse
import base64
from datetime import datetime
import os
import shutil

import numpy as np
import socket
import select
import pickle

import socketio
import eventlet
import eventlet.wsgi
from PIL import Image
from flask import Flask
from io import BytesIO
import sys

import matplotlib.pyplot as plt
import matplotlib.image as mpimg

import time

#from keras.models import load_model
import h5py
#from keras import __version__ as keras_version

##################** Socket for Net_Train Server**##################
HEADER_LENGTH = 10
IP = "203.246.114.231"
PORT = 1234

my_username = "car"
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((IP, PORT))
client_socket.setblocking(False)

username = my_username.encode('utf-8')
username_header = f"{len(username):<{HEADER_LENGTH}}".encode('utf-8')
client_socket.send(username_header + username)




######################################################################
sio = socketio.Server()
app = Flask(__name__)
prev_image_array = None

class SimplePIController:
    def __init__(self, Kp, Ki):
        self.Kp = Kp
        self.Ki = Ki
        self.set_point = 0.
        self.error = 0.
        self.integral = 0.

        self.go = True

    def set_desired(self, desired):
        self.integral = 0.
        self.set_point = desired


    def update(self, measurement):
        # proportional error
        if self.go:
            self.error = self.set_point - measurement

            # integral error
            self.integral += self.error

            return self.Kp * self.error + self.Ki * self.integral
        else:
            return 0.0


controller = SimplePIController(0.1, 0.002)
set_speed = 9
controller.set_desired(set_speed)

message = 0
send_image = True
training = True
@sio.on('telemetry')
def telemetry(sid, data):
    global message, send_image, training
    if data:
        # The current steering angle of the car
        steering_angle = data["steering_angle"]
        # The current throttle of the car
        throttle = data["throttle"]
        # The current speed of the car
        speed = data["speed"]
        # The current image from the center camera of the car
        imgString = data["image"]
        image = Image.open(BytesIO(base64.b64decode(imgString)))
        image_array = np.asarray(image)
        #image_array = tf.image.resize([image_array], (32,64))

        ##################** Socket for Net_Train Server**##################
        


        try:
            # receive things
            username_header = client_socket.recv(HEADER_LENGTH)
            if not len(username_header):
                print("connection closed by the server")
                sys.exit()
                
            username_length = int(username_header.decode('utf-8'))
            username = client_socket.recv(username_length).decode('utf-8')
            if username == 'net':
                if training:
                    controller.set_desired(set_speed)
                send_image = True
                training = False
            if username == 'tutor':
                if not training:
                    controller.set_desired(set_speed)
                training = True

            if send_image:
                out_message = pickle.dumps(image_array)
                out_message_header = f"{len(out_message):<{HEADER_LENGTH}}".encode('utf-8')
                client_socket.send(out_message_header + out_message)
                send_image = False
                #time.sleep(0.1)

            message_header = client_socket.recv(HEADER_LENGTH)
            message_length = int(message_header.decode('utf-8'))
            message = client_socket.recv(message_length).decode('utf-8')
            
            #print(f"{username} > {message}")

                
        except Exception as e:
            pass
        ####################################################################
        try:
            str(float(message))
            steering_angle = message
        except:
            pass
        throttle = controller.update(float(speed))

        print(steering_angle, throttle)
        send_control(steering_angle, throttle)

        # save frame
        if args.image_folder != '':
            timestamp = datetime.utcnow().strftime('%Y_%m_%d_%H_%M_%S_%f')[:-3]
            image_filename = os.path.join(args.image_folder, timestamp)
            image.save('{}.jpg'.format(image_filename))
    else:
        # NOTE: DON'T EDIT THIS.
        sio.emit('manual', data={}, skip_sid=True)


@sio.on('connect')
def connect(sid, environ):
    print("connect ", sid)
    send_control(0, 0)


def send_control(steering_angle, throttle):
    sio.emit(
        "steer",
        data={
            'steering_angle': steering_angle.__str__(),
            'throttle': throttle.__str__()
        },
        skip_sid=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Remote Driving')
    parser.add_argument(
        'image_folder',
        type=str,
        nargs='?',
        #default='',
        default='Eval_capture',
        help='Path to image folder. This is where the images from the run will be saved.'
    )
    args = parser.parse_args()

    # check that model Keras version is same as local Keras version
    """
    f = h5py.File(args.model, mode='r')
    model_version = f.attrs.get('keras_version')
    keras_version = str(keras_version).encode('utf8')

    if model_version != keras_version:
        print('You are using Keras version ', keras_version,
              ', but the model was built using ', model_version)

    model = load_model(args.model)
    
    """
    #print(f"loading from {args.model}")
    #net.load_weights(args.model)
    
    if args.image_folder != '':
        print("Creating image folder at {}".format(args.image_folder))
        if not os.path.exists(args.image_folder):
            os.makedirs(args.image_folder)
        else:
            shutil.rmtree(args.image_folder)
            os.makedirs(args.image_folder)
        print("RECORDING THIS RUN ...")
    else:
        print("NOT RECORDING THIS RUN ...")

    # wrap Flask application with engineio's middleware
    app = socketio.Middleware(sio, app)

    # deploy as an eventlet WSGI server
    eventlet.wsgi.server(eventlet.listen(('', 4567)), app)
