#!/usr/bin/env python
from flask import Flask, request, render_template, Response
from prototype_camera_2 import Camera
import os
import redis
import global_settings
import config
import sys
import signal
from flask_cors import CORS
import json

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
print("ROOT_DIR={}".format(ROOT_DIR))
STARTED = True
PREV_CAM_ID = -1
CAM_ID = -1

# setup global
global_settings.init('bwc_manage', True)

# Logger
_logger = global_settings._logger

# redis mgr
_redis_mgr = global_settings._redis_mgr

#handler Exit
def signal_handler(signal, frame):
    print("Ctrl Break detected.")
    _redis_mgr.cleanup()
    sys.exit()

app = Flask(__name__,
            static_url_path='', 
            static_folder='web/static',
            template_folder='web/templates')
CORS(app)

@app.route('/')
def index():
    return render_template('camera.html')

def gen(camera):
    print("start {}".format(camera.cam_id))
    global STARTED, PREV_CAM_ID
    while STARTED:
        #print(STARTED)
        frame = camera.get_frame()
       # print(frame)
        if frame is not None:
            yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        else:
            yield('')
    _logger.info("Camera {} stream is terminated!".format(PREV_CAM_ID))

@app.route(config.API_PREFIX + '/video_feed')
def video_feed():
    global CAM_ID
    _logger.info("Video feed on CAM_ID={}".format(CAM_ID))
    if CAM_ID != -1:
        #CAM = gen(Camera(CAM_ID))
        return Response(gen(Camera(CAM_ID)), 
                        mimetype='multipart/x-mixed-replace; boundary=frame')
    else:
        dir = os.getcwd()
        return Response(open( dir + "/no_video.jpg", 'rb').read(), 
                        mimetype='multipart/x-mixed-replace; boundary=frame')
        

@app.route(config.API_PREFIX + "/api/ping", methods=['GET'])
def ping():
    return {
        "msg": "pong",
    }, 200

@app.route(config.API_PREFIX + "/api/start_camera", methods=['POST'])
def start_camera():
    try:
        request_data = request.get_json()
        camera = request_data['camera']
        data = {
            "task": "START_LIVESTREAM",
            "camera": camera,
            "to": "dotnet",
        }

        # convert into JSON:
        data_json = json.dumps(data)
        _redis_mgr.publish(config.REDIS_BWC_TOPIC, data_json)
        global CAM_ID, PREV_CAM_ID, STARTED
        PREV_CAM_ID = CAM_ID
        CAM_ID = int(camera)
        STARTED = True
        _logger.info("Start CAM_ID={}".format(CAM_ID))
        return {
            "msg": "camera {} started".format(camera)
        }, 200
    except Exception as e:
        print(e)
        return {
            "msg": "error"
        }, 500

@app.route(config.API_PREFIX + "/api/stop_camera", methods=['GET'])
def stop_camera():
    try: 
        global CAM_ID, PREV_CAM_ID, STARTED
        _logger.info("test")
        _logger.info("Stop CAM_ID={}".format(CAM_ID))
        PREV_CAM_ID = CAM_ID
        CAM_ID = -1
        STARTED = False
        data = {
            "task": "STOP_LIVESTREAM",
            "camera": PREV_CAM_ID,
            "to": "dotnet",
        }

        # convert into JSON:
        data_json = json.dumps(data)
        _redis_mgr.publish(config.REDIS_BWC_TOPIC, data_json)
        return {
            "msg": "camera {} stopped".format(PREV_CAM_ID),
        }, 200
    except Exception as e:
        print(e)
        return {
            "msg": "error"
        }, 500

if __name__ == '__main__':
    signal.signal(signal.SIGINT, signal_handler)
    _logger.info(config.APPLICATION_NAME + " " + config.APPLICATION_VERSION)
    app.run(debug=config.FLASK_DEBUG, host='0.0.0.0', port=config.FLASK_PORT)