from time import time
import config

class Camera(object):
    def __init__(self, cam_id):
        print("Camera Class = {}".format(cam_id))
        self.cam_id = cam_id
        self.img_url = "{}/{}/".format(config.img_url, cam_id)
        print("camera id = {}, img_url = {}".format(cam_id, self.img_url))
        self.openfiles()
       
    
    def openfiles(self):
        try:
            if self.cam_id != -1:
                self.frames = [open(f + '.jpg', 'rb').read() for f in [self.img_url + '1', self.img_url + '2', self.img_url + '3']]
        except Exception as e:
            print(e)
        
    def get_frame(self):
        if (self.frames):
            print("Getting frame for {}".format(self.cam_id))
            return self.frames[int(time()) % config.max_frame]
        else:
            return None