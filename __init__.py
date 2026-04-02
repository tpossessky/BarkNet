import cv2
from flask import Flask
from flask_session import Session


def create_app():
    app = Flask(__name__)
    video_stream = cv2.VideoCapture(0)

    # Configuration
    app.config['SECRET_KEY'] = 'your-secret-key-change-in-production'
    app.config['SESSION_TYPE'] = 'filesystem'
    app.config['PERMANENT_SESSION_LIFETIME'] = 300  # 5 minutes in seconds
    app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'

    # Register blueprints FIRST (before initializing video)
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)
    Session(app)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    # Initialize video stream AFTER blueprints are registered
    from . import main  # Import the module itself
    main.init_video_stream(video_stream)

    return app