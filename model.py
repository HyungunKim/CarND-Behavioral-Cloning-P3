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

import os

#Tensorflow 2.x GPU limitation
gpus = tf.config.experimental.list_physical_devices('GPU')
num_gpu = 1
memory_limit = 1024
if gpus :
    try :
        tf.config.experimental.set_virtual_device_configuration(gpus[num_gpu-1], [tf.config.experimental.VirtualDeviceConfiguration(memory_limit = memory_limit)])
        print("Use {} GPU limited {}MB memory".format(num_gpu, memory_limit))
    except RuntimeError as e :
        print(e)

sdy = 0
src = np.array([[110, 110 + sdy], #l high
                [60, 160], #l low
                [210, 110 + sdy], #r high
                [260, 160]], dtype=np.float32)#r low 
dx = 10
dy = 0
target = np.array([[4*(110-160)//5+160+dx, 130+dy], #l high
                   [4*(110-160)//5+160+dx, 160],#l low
                   [4*(210-160)//5+160-dx, 130+dy], #r high
                   [4*(210-160)//5+160-dx, 160]], dtype=np.float32)#r low 


def Warp(img, src, target, mat=False):
    try:
        y, x, c = img.shape
    except:
        y, x = img.shape
    #img = cv2.undistort(img, mtx, dist, None, mtx)

    M = cv2.getPerspectiveTransform(src, target)
    
    warped = cv2.warpPerspective(img, M, (x, y), flags=cv2.INTER_LINEAR)
    if mat:
        return warped, M
    return warped

class Net(K.Model):
    def __init__(self, decode = False):
        super().__init__()
        self.decode = decode

        self.encoder = K.Sequential( [
            ll.Conv2D(16, 3, input_shape=(160,320,3), padding='same', activation='relu', kernel_regularizer=K.regularizers.l2(0.001)),
            ll.MaxPool2D(),
            #ll.Dropout(0.5),
            
            ll.Conv2D(32, 3, padding='same', activation='relu', kernel_regularizer=K.regularizers.l2(0.001)),
            ll.MaxPool2D(),
            #ll.Dropout(0.5),
            
            ll.Conv2D(32, 3, padding='same', activation='relu', kernel_regularizer=K.regularizers.l2(0.001)),
            ll.MaxPool2D(),
            #ll.Dropout(0.5),
            
            ll.Conv2D(64, 3, padding='same', activation='relu', kernel_regularizer=K.regularizers.l2(0.001)),
            ll.MaxPool2D(),
            #ll.Dropout(0.5),
            
            ll.Conv2D(64, 3, padding='same', activation='relu', kernel_regularizer=K.regularizers.l2(0.001)),
            ll.MaxPool2D()])

        if decode:
            self.decoder = K.Sequential([
                ll.UpSampling2D(input_shape=(5,10,64)),
                ll.Conv2D(64, 3, padding='same', activation='relu', kernel_regularizer=K.regularizers.l2(0.001)),
                
                ll.UpSampling2D(),
                ll.Conv2D(64, 3, padding='same', activation='relu', kernel_regularizer=K.regularizers.l2(0.001)),
                
                ll.UpSampling2D(),
                ll.Conv2D(32, 3, padding='same', activation='relu', kernel_regularizer=K.regularizers.l2(0.001)),
                
                ll.UpSampling2D(),
                ll.Conv2D(32, 3, padding='same', activation='relu', kernel_regularizer=K.regularizers.l2(0.001)),
                
                ll.UpSampling2D(),
                ll.Conv2D(3, 3, padding='same', activation='sigmoid', kernel_regularizer=K.regularizers.l2(0.001))])
            
        self.predict_conv =  K.Sequential( [
            ll.Conv2D(64, 3, input_shape=(5,10,64), padding='same', activation='relu', kernel_regularizer=K.regularizers.l2(0.001)),
            ll.Conv2D(64, 3, padding='same', activation='relu', kernel_regularizer=K.regularizers.l2(0.001)),
            ll.MaxPool2D(),
            ll.Conv2D(128, 3, padding='same', activation='relu', kernel_regularizer=K.regularizers.l2(0.001)),
            ll.Conv2D(128, 3, padding='same', activation='relu', kernel_regularizer=K.regularizers.l2(0.001)),
            ll.GlobalMaxPool2D()])

        self.predict = K.Sequential([
            ll.Dense(256, input_shape=(128,), activation='relu'),
            ll.Dropout(0.5),
            ll.Dense(256, activation='relu'),
            ll.Dropout(0.5),
            ll.Dense(1, activation='sigmoid')
        ])
        self.epochs = 0
        

    def call(self, warped):
        if self.decode:
            encoded = self.encoder(warped)
            decoded = self.decoder(encoded)
            predict_conved = self.predict_conv(encoded)
            predicted = self.predict(predict_conved) - 0.5
            return predicted, decoded
        else:
            encoded = self.encoder(warped)
            predict_conved = self.predict_conv(encoded)
            predicted = self.predict(predict_conved) - 0.5
            return predicted

    def save_model(self, path='model_check_points'):
        self.encoder.save(f"{path}/encoder")
        
        if self.decode:
            self.decoder.save(f"{path}/decoder")

        self.predict_conv.save(f"{path}/predict_conv")
        self.predict.save(f"{path}/predict")

    def load_model(self, path):
        self.encoder = K.models.load_model(f"{path}/encoder")
        if self.decode:
            self.decoder = K.models.load_model(f"{path}/decoder")
        self.predict_conv = K.models.load_model(f"{path}/predict_conv")
        self.predict = K.models.load_model(f"{path}/predict")

class Trainer:
    def __init__(self, net, directory='Train_capture'):
        self.net = net
        self.index = 0

        self.directory = directory

        self.index += len(os.listdir((directory+'/img')))

    def record(self, img, steering):
        img = img.reshape(160,320,3)
        mpimg.imsave(f"{self.directory}/img/{self.index}.jpg", img)
        with open(f"{self.directory}/steering.csv", "a") as f:
            f.write(f"{steering}\n")
        self.index += 1



    def train(self, batch_size=64, epochs=4):
        criterion = losses.mean_squared_error
        optimizer = optim.Adam(lr=0.001)
        loops = self.index//batch_size
        df = pd.read_csv(f'{self.directory}/steering.csv')
        for e in range(epochs):
            for i in range(loops):
                B = np.random.randint(0,self.index, size=batch_size)
                X = np.zeros((batch_size, 160, 320, 3))
                S = np.zeros((batch_size, 1))
                for b in range(batch_size):
                    X[b] = Warp(mpimg.imread(f'{self.directory}/img/{B[b]}.jpg'), src, target)/256

                    X = np.array(X, dtype=np.float32)

                    S[b] = df.iloc[B[b]].steering
                    if np.random.choice([True,False]):
                        X[b] = np.flip(X[b], 1)
                        S[b] = -S[b]

                    else:
                        pass
                if self.net.decode:
                    with tf.GradientTape() as t:

                        output, dec = self.net(X)

                        loss1 = losses.MSE(S, output)

                    grads = t.gradient(loss1, self.net.encoder.trainable_variables +  self.net.predict_conv.trainable_variables + self.net.predict.trainable_variables)
                    optimizer.apply_gradients(zip(grads, self.net.encoder.trainable_variables +  self.net.predict_conv.trainable_variables + self.net.predict.trainable_variables))

                    with tf.GradientTape() as t:

                        output, dec = self.net(X)

                        loss2 = losses.MAE(X, dec)

                    grads = t.gradient(loss2, self.net.encoder.trainable_variables+ self.net.decoder.trainable_variables)
                    optimizer.apply_gradients(zip(grads, self.net.encoder.trainable_variables+ self.net.decoder.trainable_variables))
                    """
                    if e+i == 0:
                        self.net.compile(optimizer='adam', loss='MSE')
                        self.net.fit(X,S, batch_size=batch_size, shuffle=False)"""
                    print(f"epochs {self.net.epochs} | loss1 = {np.sum(loss1):.2f} | loss2 = {np.sum(loss2):.2f}\n")

                else:
                    with tf.GradientTape() as t:

                        output = self.net(X)

                        loss = losses.MSE(S, output)

                    grads = t.gradient(loss, self.net.trainable_variables)
                    optimizer.apply_gradients(zip(grads, self.net.trainable_variables))
                    """
                    if e+i == 0:
                        self.net.compile(optimizer='adam', loss='MSE')
                        self.net.fit(X,S, batch_size=batch_size, shuffle=False)"""
                    print(f"epochs {self.net.epochs} | loss1 = {np.sum(loss):.2f}\n")

            self.net.epochs += 1

            self.net.save_model('model_check_points')




def main1():
    net = Net(decode=True)
    try:
        net.load_model('model_check_points')
        print("Load Success")
    except:
        print("Failed to load model")
    tr = Trainer(net)
    tr.train()
    return net, tr

def main():
    net = Net()
    try:
        net.load_model('model_check_points')
        print("Load Success")
    except:
        print("Failed to load model")
    tr = Trainer(net)
    tr.train(epochs=3)
    return net, tr

def main2():
    net = Net()
    try:
        net.encoder = K.models.load_model(f"model_check_points/encoder")
        print("Load Success")
    except:
        print("Failed to load model")
    tr = Trainer(net)
    tr.train(epochs=3)
    return net, tr

if __name__ == '__main__':
    net, tr = main1()