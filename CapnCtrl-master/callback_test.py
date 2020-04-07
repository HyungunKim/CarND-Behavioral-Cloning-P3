import threading
import time
from queue import Empty
import multiprocessing
import cv2

class test:

    def __init__(self):
        self.callbacks = []


    def start(self):
        self.queue = multiprocessing.Queue()

        self.t = threading.Thread(target=self.deamon)
        self.t.setDaemon(True)
        self.t.start()
        p = multiprocessing.Process(target=self.read_video, args=(self.queue,))
        p.start()

    def add_callback(self,cb):
        self.callbacks.append(cb)

    def deamon(self):
        while True:
            img = None
            try:
                img = self.queue.get(False)
            except Empty:
                img = None
            if img is not None:
                for cb in self.callbacks:
                    cb(img)
            time.sleep(0.01)


    def read_video(self, queue):
        vid = cv2.VideoCapture(0)
        while True:
            ret,img = vid.read()
            if ret:
                queue.put(img)



def foo(x):
    #cv2.imshow("test",x)
    print("got {}".format(x.shape))

t = test()
t.add_callback(foo)
t.start()

while True:
    print("waiting...")
    time.sleep(1)
