# Command
- python app.py
- open camera.html in browser

# curls
- curl localhost:5000/bwc/api/ping
- curl -XPOST -H "content-type:application/json" -d "{\"camera\":45}" localhost:5000/bwc/api/start_camera
- curl localhost:5000/bwc/api/stop_camera

- curl https://smrtmbocc.certismozart.com/bwc/api/ping
- curl -XPOST -H "content-type:application/json" -d "{\"camera\":45}" https://smrtmbocc.certismozart.com/bwc/api/start_camera
- curl https://smrtmbocc.certismozart.com//bwc/api/stop_camera

# redis 
{"task":"START_LIVESTREAM", "camera":45, "to":"dotnet"}
{"task":"STOP_LIVESTREAM", "camera":45, "to":"dotnet"}

# Flow
- Wait 5 seconds
- Read 10 Images to Frames



# Link
- *[Flask Camera] (https://blog.miguelgrinberg.com/post/video-streaming-with-flask)
                 (https://blog.miguelgrinberg.com/post/flask-video-streaming-revisited)
- [Delete File] (https://superfastpython.com/timer-thread-in-python/)
- [Pointer] (https://www.tutorialspoint.com/what-is-the-pointer-in-python-does-a-pointer-exist-in-python#:~:text=Everything%20is%20an%20object%20in,place%20the%20object%20is%20kept.)
- [Repeated Timer] (https://pythonassets.com/posts/executing-code-every-certain-time/)
- [Repeated Task] (https://gist.github.com/allanfreitas/e2cd0ff49bbf7ddf1d85a3962d577dbf)
- [Delete list] (https://www.geeksforgeeks.org/python-front-and-rear-range-deletion-in-a-list/)
- [Mutex] (https://stackoverflow.com/questions/31508574/semaphores-on-python)