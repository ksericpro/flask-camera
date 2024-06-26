from time import time
import os
import config
import threading
from threading import Timer
import traceback
import time as tm
import copy

class Camera(object):
    def __init__(self, cam_id):
        self.PLAYBACk_BATCH = config.PLAYBACK_PERIOD * config.PLAYBACK_FPS
        self.frameset_1 = []
        self.frameset_2 = []
        #print("Camera Class = {}".format(cam_id))
        self.cam_id = cam_id
        self.img_url = "{}/{}/".format(config.PLAYBACK_IMAGE_SRC, cam_id)
        print("camera id = {}, img_url = {}".format(cam_id, self.img_url))
        #self.openfiles(self.img_url) #working
        #self._should_stop = False
        self.current_frameset = self.frameset_1 # pointer
        self.toggle_frameset = 0
        self.current_frameset_iteration_completed = False
        self.init()
        
    # Thread test
    def every(self, delay, task):
        next_time = int(time()) + delay
        while True:
            tm.sleep(max(0, next_time - tm.time()))
            try:
                task()
            except Exception:
                traceback.print_exc()
            # in production code you might want to have this instead of course:
            # logger.exception("Problem while executing repetitive task.")
            # skip tasks if we are behind schedule:
            next_time += (int(time()) - next_time) // delay * delay + delay

    def iteration_checker(self):
        print("iteration_checker:start: current_frameset_iteration_completed= {}, toggle_frameset={}".format(self.current_frameset_iteration_completed, self.toggle_frameset))
        if self.current_frameset_iteration_completed:
            test_set = []
            if self.toggle_frameset == 0:
                self.openfiles(test_set, self.img_url)
                if len(test_set)>0:
                    self.frameset_2 = copy.deepcopy(test_set)
                    del self.frameset_1[:]
                    self.toggle_frameset = 1
                    self.current_frameset = self.frameset_2
                    self.current_frameset_iteration_completed = False
                else:
                    del self.frameset_1[:]
            else:
                self.openfiles(test_set, self.img_url)
                if len(test_set)>0:
                    self.frameset_1 = copy.deepcopy(test_set)
                    del self.frameset_2[:]
                    self.toggle_frameset = 0
                    self.current_frameset = self.frameset_1
                    self.current_frameset_iteration_completed = False
                else:
                    del self.frameset_2[:]
            del test_set[:]

            
        print("iteration_checker: current_frameset_iteration_completed= {}, toggle_frameset={}, frameset_1={}, frameset_2={}".format(self.current_frameset_iteration_completed,
         self.toggle_frameset, len(self.frameset_1), len(self.frameset_2)))
        #self.openfiles(self.current_frameset, self.img_url)

    def start_threads(self):
        threading.Thread(target=lambda: self.every(config.PLAYBACK_PERIOD, self.iteration_checker)).start()

    # initialize
    def init(self):
        print("init:delay start={}s".format(config.PLAYBACK_CAMERA_DELAY_START))
        self.current_frameset = self.frameset_1
        t = Timer(config.PLAYBACK_CAMERA_DELAY_START, self.openfiles, args=(self.current_frameset, self.img_url))
        t.start()
        t2 = Timer(config.PLAYBACK_CAMERA_DELAY_START, self.start_threads,)
        t2.start()
        #threading.Thread(target=lambda: self.every(config.PLAYBACK_PERIOD, self.iteration_checker)).start()
        print("init:completed")

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

    def openfiles(self, frames_arr, dir):
        try:
            print("openfiles:start")
            if self.cam_id != -1:
                del frames_arr[:]
                arr = self.getfiles(dir, self.PLAYBACk_BATCH)
                print("There are {} file(s)".format(len(arr)))
                for f in arr:
                    f2 = os.path.join(dir,f)
                    print("adding {}".format(f2))
                    frames_arr.append(open(f2, 'rb').read())
                #self.frames = [open(f + '.jpg', 'rb').read() for f in [dir + '1', self.img_url + '2', dir + '3']]
                print("frames size={}".format(len(frames_arr)))
                self.deletefiles(dir, arr, config.PLAYBACK_DELETE_SRC_IMAGE_COMMIT)
            print("openfiles:end")
        except Exception as e:
            print(e)
        
    def get_frame(self):
        #print("using current_frameset:{}".format(self.toggle_frameset))
        sz = len(self.current_frameset)
        if len(self.current_frameset)>0:
            #print("Getting frame for {}".format(self.cam_id))
            n = int(time()) % sz
            if n == sz -1:
               # print("End of Frame!!")
                self.current_frameset_iteration_completed = True
            #print("{}".format(n))
            #print("{}:Getting frame for {}, n={}".format(time(), self.cam_id, n))
            return self.current_frameset[n]
        else:
            return None