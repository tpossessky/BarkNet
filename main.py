import cv2
from flask import Blueprint, render_template, Response, app, redirect, url_for
from flask_login import login_required, current_user
from .auth import login_required_simple


main = Blueprint('main', __name__)
video_stream = None

def init_video_stream(stream):
    global video_stream
    video_stream = stream

@main.route('/')
def index():
    return redirect(url_for('auth.login'))

def start_video():
    while True:
        ret, frame = video_stream.read()
        if not ret:
            print("Bye!")
            break

        frame = cv2.flip(frame, 1)
        ret, buffer = cv2.imencode('.jpg', frame)  # Add this line
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@main.route('/video_feed')
@login_required_simple  # Protect video feed too
def video_feed():
    return Response(start_video(), 	mimetype="multipart/x-mixed-replace; boundary=frame")


@main.route('/stream')
@login_required_simple
def stream():
    return render_template('stream/stream.html',title = "Video Feed")