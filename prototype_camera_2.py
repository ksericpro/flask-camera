from time import time
import os
import config
import threading
from threading import Timer

class Camera(object):
    def __init__(self, cam_id):
        self.PLAYBACk_BATCH = config.PLAYBACK_PERIOD * config.PLAYBACK_FPS
        self.frameset_1 = []
        self.frameset_2 = []
        #print("Camera Class = {}".format(cam_id))
        self.cam_id = cam_id
        self.img_url = "{}/{}/".format(config.img_url, cam_id)
        print("camera id = {}, img_url = {}".format(cam_id, self.img_url))
        #self.openfiles(self.img_url) #working
        #self._should_stop = False
        self.current_frameset = None # pointer
        self.init()
        
    # Thread test
    def startThreads(self):
        t1 = threading.Thread(target=self.openfiles, args=(self.frameset_1, self.img_url))
        t1.start()
        t1.join()

    # initialize
    def rotate_populate(self)
        print("rotate populate:start")
        print("rotate populate:end")

    def init(self):
        print("init:delay start={}s".format(config.PLAYBACK_CAMERA_DELAY_START))
        self.current_frameset = self.frameset_1
        t = Timer(config.PLAYBACK_CAMERA_DELAY_START, self.openfiles, args=(self.current_frameset, self.img_url))
        t2 = Timer(config.PLAYBACK_CAMERA_DELAY_START, self.rotate_populate, args=(,))
        t.start()
        t2.start()
        print("init:completed")

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
            # If file exists, delete it.
            if os.path.isfile(f2):
                os.remove(f2)
            else:
                print("Error: %s file not found" % f2)

    '''
    def openfiles(self, dir):
        try:
            print("openfiles:start")
            if self.cam_id != -1:
                arr = self.getfiles(dir, self.PLAYBACk_BATCH)
                print("There are {} file(s)".format(len(arr)))
                for f in arr:
                    f2 = os.path.join(dir,f)
                    print("adding {}".format(f2))
                    self.frameset_1.append(open(f2, 'rb').read())
                #self.frames = [open(f + '.jpg', 'rb').read() for f in [dir + '1', self.img_url + '2', dir + '3']]
                print("self.frames size={}".format(len(self.frameset_1)))
                self.deletefiles(dir, arr)
        except Exception as e:
            print(e)
    '''

    def openfiles(self, frames_arr, dir):
        try:
            print("openfiles:start")
            if self.cam_id != -1:
                arr = self.getfiles(dir, self.PLAYBACk_BATCH)
                print("There are {} file(s)".format(len(arr)))
                for f in arr:
                    f2 = os.path.join(dir,f)
                    print("adding {}".format(f2))
                    frames_arr.append(open(f2, 'rb').read())
                #self.frames = [open(f + '.jpg', 'rb').read() for f in [dir + '1', self.img_url + '2', dir + '3']]
                print("frames size={}".format(len(frames_arr)))
                self.deletefiles(dir, arr)
            print("openfiles:end")
        except Exception as e:
            print(e)
        
    def get_frame(self):
        if len(self.current_frameset)>0:
            #print("Getting frame for {}".format(self.cam_id))
            n = int(time()) % len(self.current_frameset)
            #if n == len(self.current_frameset) -1:
            #    print("End of Frame!!")
           # print("{}:Getting frame for {}, n={}".format(time(), self.cam_id, n))
            return self.current_frameset[n]
        else:
            return None