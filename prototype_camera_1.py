from time import time
import os
import config
import threading
import time

class Camera(object):
    def __init__(self, cam_id):
        #self.frames = []
        print("init:Camera Class = {}".format(cam_id))
        self.cam_id = cam_id
        self.img_url = "{}/{}/".format(config.img_url, cam_id)
        print("init:camera id = {}, img_url = {}".format(cam_id, self.img_url))
        self.open_files(self.img_url)
        self._should_stop = False
        #self.start_threads()

    def populate_frames(self, dir, n):
        print("populate frames:: batch size={}, dir={}".format(n, dir))
        try:       
            while not(self._should_stop):
                arr = self.getfiles(dir, n)
                for f in arr:
                        f2 = os.path.join(dir,f)
                        print("adding {}".format(f2))
                        self.frames.append(open(f2, 'rb').read())
                print("self.frames size={}".format(len(self.frames)))
                self.deletefiles(dir, arr)
                time.sleep(config.WAIT_READ_FILES)
                break
        except Exception as e:
            print(e)

    def open_files(self, dir):
        try:       
            arr = self.getfiles(dir, 0)
            for f in arr:
                    f2 = os.path.join(dir,f)
                    print("adding {}".format(f2))
                    self.frames.append(open(f2, 'rb').read())
            print("self.frames size={}".format(len(self.frames)))
        except Exception as e:
            print(e)

    def start_threads(self):
       # self.stop_threads()
       # time.sleep(config.WAIT_READ_FILES * 2)
        print("start_thread:start")
        t1 = threading.Thread(target=self.populate_frames, args=(self.img_url, config.BATCH,))
        t1.start()
        t1.join()
        print("start_thread:end")
        self._should_stop = False

    def stop_threads(self):
        self._should_stop = True

    # helpers

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
    
        
    def get_frame(self):
        if (self.frames is not None):
            print("get_frame:Getting frame for {}, frames size={}".format(self.cam_id, len(self.frames)))
            if len(self.frames)>0:
                n = int(time()) % len(self.frames)
                print("get_frame:Getting frame for {}, frames size={}, n={}".format(self.cam_id, len(self.frames), n))
                return self.frames[n]
        return None