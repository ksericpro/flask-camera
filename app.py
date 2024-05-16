#!/usr/bin/env python
from flask import Flask, request, render_template, Response
from camera import Camera
import os

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
print("ROOT_DIR={}".format(ROOT_DIR))
STARTED = True
PREV_CAM_ID = -1
CAM_ID = -1

app = Flask(__name__,
            static_url_path='', 
            static_folder='web/static',
            template_folder='web/templates')

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
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
    #print("EXITINNNNN")
    print("Camera {} stream is terminated!".format(PREV_CAM_ID))

@app.route('/video_feed')
def video_feed():
    global CAM_ID
    print("CAM_ID={}".format(CAM_ID))
    if CAM_ID != -1:
        #CAM = gen(Camera(CAM_ID))
        return Response(gen(Camera(CAM_ID)), 
                        mimetype='multipart/x-mixed-replace; boundary=frame')
    else:
        dir = os.getcwd()
        return Response(open( dir + "/no_video.jpg", 'rb').read(), 
                        mimetype='multipart/x-mixed-replace; boundary=frame')
        

@app.route("/api/ping", methods=['GET'])
def ping():
    return {
        "msg": "pong",
    }, 200

@app.route("/api/start_camera", methods=['POST'])
def start_camera():
    try:
        request_data = request.get_json()
        camera = request_data['camera']
        global CAM_ID, PREV_CAM_ID, STARTED
        PREV_CAM_ID = CAM_ID
        CAM_ID = int(camera)
        STARTED = True
        print("Start CAM_ID={}".format(CAM_ID))
        return {
            "msg": "camera {} started".format(camera)
        }, 200
    except Exception as e:
        print(e)
        return {
            "msg": "error"
        }, 500

@app.route("/api/stop_camera", methods=['GET'])
def stop_camera():
    try: 
        global CAM_ID, PREV_CAM_ID, STARTED
        print("Stop CAM_ID={}".format(CAM_ID))
        PREV_CAM_ID = CAM_ID
        CAM_ID = -1
        STARTED = False
        return {
            "msg": "camera {} stopped".format(PREV_CAM_ID),
        }, 200
    except Exception as e:
        print(e)
        return {
            "msg": "error"
        }, 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)