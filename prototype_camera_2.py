from time import time
import os
import config
import threading

class Camera(object):
    def __init__(self, cam_id):
        self.frames_1 = []
        self.frames_2 =[]
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
                arr = self.getfiles(dir, config.BATCH)
                print("There are {} file(s)".format(len(arr)))
                for f in arr:
                    f2 = os.path.join(dir,f)
                    print("adding {}".format(f2))
                    self.frames_1.append(open(f2, 'rb').read())
                #self.frames = [open(f + '.jpg', 'rb').read() for f in [dir + '1', self.img_url + '2', dir + '3']]
                print("self.frames size={}".format(len(self.frames_1)))
                self.deletefiles(dir, arr)
        except Exception as e:
            print(e)
        
    def get_frame(self):
        if (self.frames_1 is not None):
            #print("Getting frame for {}".format(self.cam_id))
            n = int(time()) % len(self.frames_1)
            if n == len(self.frames_1) -1:
                print("End of Frame!!")
            print("{}:Getting frame for {}, n={}".format(time(), self.cam_id, n))
            return self.frames_1[n]
        else:
            return None