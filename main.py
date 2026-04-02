import cv2
from flask import Blueprint, render_template, Response, app, redirect, url_for
from flask_login import login_required, current_user
from .auth import login_required_simple
import datetime

main = Blueprint('main', __name__)
video_stream = None

def init_video_stream(stream):
    global video_stream
    video_stream = stream
def get_date_str():
    x = datetime.datetime.now()

    weekday = x.strftime("%a")
    month = x.strftime("%m")
    day = x.strftime("%d")
    year = x.strftime("%y")

    hour = x.strftime("%I")
    minute = x.strftime("%M")
    ampm = x.strftime("%p")

    return f"{weekday} {month}/{day}/{year}: {hour}:{minute} {ampm}"

@main.route('/')
def index():
    return redirect(url_for('auth.login'))

def start_video():
    while True:
        ret, frame = video_stream.read()
        if not ret:
            print("Bye!")
            break
        datetime.datetime.now()
        frame = cv2.flip(frame, 1)
        frame = cv2.putText(frame, get_date_str(), (40, 680), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
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