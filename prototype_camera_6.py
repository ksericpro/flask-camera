from time import time
import os
import config
import threading
from threading import Timer
import time as tm
import traceback

class Camera(object):
    def __init__(self, cam_id):
        self.frames = []
        print("Camera Class = {}".format(cam_id))
        self.cam_id = cam_id
        self.img_url = "{}/{}/".format(config.PLAYBACK_IMAGE_SRC, cam_id)
        print("camera id = {}, img_url = {}".format(cam_id, self.img_url))
        #self.readfiles(self.img_url)
        self._should_stop = False
        self.REACH_END = False
        self.run = True
        self.init()
        

    # initialize
    def init(self):
        delay_start = 10
        print("init:delay start={}s".format(delay_start))
       # self.current_frameset = self.frameset_1
        #t = Timer(config.PLAYBACK_CAMERA_DELAY_START, self.openfiles, args=(self.current_frameset, self.img_url))
        #t.start()
        t2 = Timer(delay_start, self.start_threads,)
        t2.start()
        #threading.Thread(target=lambda: self.every(config.PLAYBACK_PERIOD, self.iteration_checker)).start()
        print("init:completed")

    def start_threads(self):
        print("start_threads:started")
        self.iteration_checker()
        #t2 = Timer(5, self.iteration_checker,)
        #t2.start()
        self.current_frameset_iteration_completed = True
        self.thread= threading.Thread(target=lambda: self.every(10, self.iteration_checker))
        self.thread.start()

    def iteration_checker(self):
        print("iteration_checker:start:")

        print("iteration_check:reading new batch of files")
        test_set = []
        arr = self.readdir(test_set, self.img_url)
        sz = len(test_set)
        print("iteration_check: file(s)={}, arr={}".format(sz, len(arr)))
        if sz>0:
            self.frames = test_set
            self.CURRENT_MAX_FRAMES_LENGTH = len(test_set)
            print("self.frames size={}".format(self.CURRENT_MAX_FRAMES_LENGTH))
            if arr is not None:
                self.deletefiles(self.img_url, arr, config.PLAYBACK_DELETE_SRC_IMAGE_COMMIT)


        print("iteration_check:end")

       # Timer
    def every(self, delay, task):
        next_time = int(time()) + delay
        print("every:start")
        while self.run:
            tm.sleep(max(0, next_time - tm.time()))
            try:
                task()
            except Exception:
                traceback.print_exc()
            # in production code you might want to have this instead of course:
            # logger.exception("Problem while executing repetitive task.")
            # skip tasks if we are behind schedule:
            next_time += (int(time()) - next_time) // delay * delay + delay
        print("every:end")

    def stop_threads(self):
        print("stop_threads:started")

    def getfiles(self, dir, n):
        arr = os.listdir(dir)
        if len(arr) > n:
            return arr[:n]
        else:
            return arr
    
    def deletefiles(self, dir, arr, commit):
        for f in arr:
            f2 = os.path.join(dir,f)     
            if commit:
                print("deleting file {}".format(f2))
                # If file exists, delete it.
                if os.path.isfile(f2):
                    os.remove(f2)
                else:
                    print("Error: %s file not found" % f2)


    def readdir(self, frames_arr,  dir):
        try:
            if self.cam_id != -1:
                #self.startThreads()
                #arr = self.getfiles(dir, BATCH)
                arr = self.getfiles(dir, 999)
                for f in arr:
                    f2 = os.path.join(dir,f)
                    print("adding {}".format(f2))
                    frames_arr.append(open(f2, 'rb').read())
                #self.frames = [open(f + '.jpg', 'rb').read() for f in [dir + '1', self.img_url + '2', dir + '3']]
                return arr
        except Exception as e:
            print(e)
            return None
        
    def get_frame(self):
        if (self.frames is not None):
            sz = len(self.frames)
            if sz>0:
                tm = int(time())
                index = tm % len(self.frames)
               #print("{0}: Index={1}, self.CURRENT_MAX_FRAMES_LENGTH={2}".format(tm, index, self.CURRENT_MAX_FRAMES_LENGTH))
                if index == self.CURRENT_MAX_FRAMES_LENGTH -1:
                    #print("****Reach")
                    self.REACH_END = True
                
                if self.REACH_END == False:
                    return self.frames[index]
                else:
                    return self.frames[self.CURRENT_MAX_FRAMES_LENGTH -1]
            else:
                return None
        else:
            return None
