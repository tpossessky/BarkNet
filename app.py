import time

from flask import Flask, render_template, Response
import cv2
import pyaudio
app = Flask(__name__)
video_stream = cv2.VideoCapture(0)


@app.route('/')
def base():  # put application's code here
    return render_template('base.html', title="Welcome", message="Welcome to BarkNet!")


def start_video(video_stream):
    while True:
        ret, frame = video_stream.read()
        if not ret:
            print("Bye!")
            break

        frame = cv2.flip(frame, 1)
        ret, buffer = cv2.imencode('.png', frame)  # Add this line
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/png\r\n\r\n' + frame + b'\r\n')


@app.route('/video_feed')
def video_feed():
    return Response(start_video(video_stream), 	mimetype="multipart/x-mixed-replace; boundary=frame")


@app.route('/stream')
def stream():
    return render_template('stream/stream.html')

if __name__ == '__main__':
    app.run(debug=True)

    #
    # if not video_stream.isOpened():
    #     print('Cannot open webcam')
    #     exit(1)
    #
    # org = (0, 475)
    # font = cv2.FONT_HERSHEY_SIMPLEX
    # color = (255, 255, 255)  # White
    #
    # while True:
    #     ret, frame = video_stream.read()
    #     if not ret:
    #         print("Bye!")
    #         break
    #
    #
    #
    #     frame = cv2.flip(frame, 1)
    #
    #     cv2.imshow('TestView', frame)
    #     if cv2.waitKey(1) == ord('q'):
    #         break
    #
    # video_stream.release()
    cv2.destroyAllWindows()
