from time import time
import os
import config

class Camera(object):
    def __init__(self, cam_id):
        print("Camera Class = {}".format(cam_id))
        self.cam_id = cam_id
        self.img_url = "{}/{}/".format(config.img_url, cam_id)
        print("camera id = {}, img_url = {}".format(cam_id, self.img_url))
        self.openfiles(self.img_url)
       
    
    def getfiles(self, dir):
        arr = os.listdir(dir)
        return arr


    def openfiles(self, dir):
        try:
            if self.cam_id != -1:
                arr = self.getfiles(dir)
                self.frames = []
                for f in arr:
                    f2 = os.path.join(dir,f)
                    print("adding {}".format(f2))
                    self.frames.append(open(f2, 'rb').read())
                #self.frames = [open(f + '.jpg', 'rb').read() for f in [dir + '1', self.img_url + '2', dir + '3']]
                print("self.frames size={}".format(len(self.frames)))
        except Exception as e:
            print(e)
        
    def get_frame(self):
        if (self.frames is not None):
            #print("Getting frame for {}".format(self.cam_id))
            return self.frames[int(time()) % len(self.frames)]
        else:
            return None