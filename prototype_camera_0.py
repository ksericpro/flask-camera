from time import time
import os
import config
import threading

BATCH = 10

class Camera(object):
    def __init__(self, cam_id):
        self.frames = []
        print("Camera Class = {}".format(cam_id))
        self.cam_id = cam_id
        self.img_url = "{}/{}/".format(config.img_url, cam_id)
        print("camera id = {}, img_url = {}".format(cam_id, self.img_url))
        self.openfiles(self.img_url)
        self._should_stop = False
        
       
    def print_square(self, num):
        print("Square: {}" .format(num * num))

    def startThreads(self):
        t1 = threading.Thread(target=self.print_square, args=(100,))
        t1.start()
        t1.join()

    def getfiles(self, dir, n):
        arr = os.listdir(dir)
        if len(arr) > n:
            return arr[:n]
        else:
            return arr
    
    def deletefiles(self, dir, arr):
        for f in arr:
            f2 = os.path.join(dir,f)
            print("deleting file {}".format(f2))


    def openfiles(self, dir):
        try:
            if self.cam_id != -1:
                self.startThreads()
                arr = self.getfiles(dir, BATCH)
                for f in arr:
                    f2 = os.path.join(dir,f)
                    print("adding {}".format(f2))
                    self.frames.append(open(f2, 'rb').read())
                #self.frames = [open(f + '.jpg', 'rb').read() for f in [dir + '1', self.img_url + '2', dir + '3']]
                print("self.frames size={}".format(len(self.frames)))
                self.deletefiles(dir, arr)
        except Exception as e:
            print(e)
        
    def get_frame(self):
        if (self.frames is not None):
            #print("Getting frame for {}".format(self.cam_id))
            return self.frames[int(time()) % len(self.frames)]
        else:
            return None