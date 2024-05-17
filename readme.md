# Command
- python app.py
- open camera.html in browser

# curls
- curl localhost:5000/bwc/api/ping
- curl -XPOST -H "content-type:application/json" -d "{\"camera\":45}" localhost:5000/bwc/api/start_camera
- curl localhost:5000/bwc/api/stop_camera

# redis 
{"task":"START_LIVESTREAM", "camera":45, "to":"dotnet"}
{"task":"STOP_LIVESTREAM", "camera":45, "to":"dotnet"}

# Flow
- Wait 5 seconds
- Read 10 Images to Frames
- Wait 5 seconds
- Delete 10 Images from Frames
- Read 10 Images to Frames


# Link
- *[Flask Camera] (https://blog.miguelgrinberg.com/post/video-streaming-with-flask)
                 (https://blog.miguelgrinberg.com/post/flask-video-streaming-revisited)