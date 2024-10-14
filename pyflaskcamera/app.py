#!/usr/bin/env python
from flask import Flask, request, render_template, Response
from prototype_camera_6 import Camera
import os
import redis
import global_settings
import config
import sys
import signal
from flask_cors import CORS
import json
import ssl

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
print("ROOT_DIR={}".format(ROOT_DIR))
STARTED = True
PREV_CAM_ID = -1
CAM_ID = -1
CAM = None

# setup global
global_settings.init('bwc_manage', True)

# Logger
_logger = global_settings._logger

# redis mgr
_redis_mgr = global_settings._redis_mgr

# ssl 
# get the current working directory
current_working_directory = os.getcwd()
print("current working dir = {}".format(current_working_directory))

if config.USE_SSL:
    print("using ssl")
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER) 
    context.load_cert_chain(os.path.join(current_working_directory, 'ssl/STAR_somesolutions_net.crt'), \
                            os.path.join(current_working_directory, 'ssl/private.key'))

#handler Exit
def signal_handler(signal, frame):
    print("Ctrl Break detected.")
    _redis_mgr.cleanup()
    sys.exit()
    
def checkheader(request):
    headers = request.headers
    auth = headers.get("X-Api-Key")
    print("auth={}".format(auth))
    if auth is None or auth != config.API_KEY:
        return False
    return True      
    
app = Flask(__name__,
            static_url_path='', 
            static_folder='web/static',
            template_folder='web/templates')
CORS(app)


#@app.route("/test")
#@authentication.check_mandatory_token
#def test():
#    return {"msg":"ok"},200

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


@app.route('/')
def index():
    return {"msg": "alive"}, 200

@app.route(config.API_PREFIX + '/')
def index2():
    return {"msg": "alive"}, 200

@app.route(config.API_PREFIX + "/api/ping", methods=['GET'])
def ping():
    return {"msg": "pong"}, 200

#@app.route(config.API_PREFIX + '/')
#def web():
#    return render_template('camera.html')

@app.route(config.API_PREFIX + '/video_feed')
def video_feed():
    global CAM_ID, CAM
    _logger.info("Video feed on CAM_ID={}".format(CAM_ID))
    if CAM_ID != -1:
        CAM = Camera(CAM_ID)
        #CAM = gen(Camera(CAM_ID))

        return Response(gen(CAM), 
                        mimetype='multipart/x-mixed-replace; boundary=frame')
    else:
        dir = os.getcwd()
        return Response(open( dir + "/no_video.jpg", 'rb').read(), 
                        mimetype='multipart/x-mixed-replace; boundary=frame')
        

@app.route(config.API_PREFIX + "/api/start_camera", methods=['POST'])
def start_camera():
    if not(checkheader(request)):
        return {"message": "ERROR: Unauthorized"}, 401
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
    if not(checkheader(request)):
        return {"message": "ERROR: Unauthorized"}, 401
    try: 
        global CAM_ID, PREV_CAM_ID, STARTED, CAM
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

        if CAM is not None:
            CAM.stop_threads()
            CAM = None
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
    if config.USE_SSL:
        app.run(debug=config.FLASK_DEBUG, host='0.0.0.0', port=config.FLASK_PORT, ssl_context=context)
    else: 
        app.run(debug=config.FLASK_DEBUG, host='0.0.0.0', port=config.FLASK_PORT)
