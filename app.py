from flask import Flask, request, render_template, Response
from camera import Video
from hat import Video1
from dog import Video2
from hand import Video3

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/camera')
def camera():
    return render_template('camera.html')


@app.route('/hat1')
def hat1():
    return render_template('hat1.html')


@app.route('/dog1')
def dog1():
    return render_template('dog1.html')


@app.route('/hand1')
def hand1():
    return render_template('hand1.html')


def gen(camera):
    while True:
        frame = camera.get_frame()
        yield(b'--frame\r\n'
              b'Content-Type: image/jpeg\r\n\r\n'+frame +
              b'\r\n\r\n')


@app.route('/video')
def video():
    return Response(gen(Video()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/hat')
def video1():
    return Response(gen(Video1()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/dog')
def video2():
    return Response(gen(Video2()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/hand')
def video3():
    return Response(gen(Video3()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


app.run(debug=True)
