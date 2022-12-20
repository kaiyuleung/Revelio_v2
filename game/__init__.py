from flask import Flask, jsonify, render_template, redirect, url_for
from flask_cors import CORS
from werkzeug import exceptions

#* Auth & Auth
from flask_login import LoginManager, current_user
from .models.user import User
from .controllers import users

#* Router
from .routes.user import user as user_route

#* Database
from dotenv import load_dotenv
from os import environ
from .database.db import db

#* Email
from flask_mail import Mail
mail = Mail()

#* Session
from flask_session import Session
session = Session()

#* Socket.io
from flask_socketio import SocketIO
socketio = SocketIO()

#* API
app = Flask(__name__)
load_dotenv()
app.config.update(
    SECRET_KEY = environ.get('SECRET_KEY'),
    SQLALCHEMY_DATABASE_URI = environ.get('DATABASE_URL'),
    SQLALCHEMY_TRACK_MODIFICATIONS = environ.get('SQLALCHEMY_TRACK_MODIFICATIONS'),
    SESSION_TYPE = 'filesystem',
    MAIL_SERVER = environ.get('MAIL_SERVER'),
    MAIL_PORT = environ.get('MAIL_PORT'),
    MAIL_USERNAME = environ.get('MAIL_USERNAME'),
    MAIL_PASSWORD = environ.get('MAIL_PASSWORD'),
    MAIL_USE_TLS = True,
    MAIL_USE_SSL = False,
)
CORS(app)
with app.app_context():
    db.app = app
    db.init_app(app)

#* Route
@app.route('/')
def home():
    # return render_template('phaser.html'), 200
    # return "<h1>Welcome to this demo of flask-template-login-socket.</h1>", 200
    if (current_user.is_authenticated):
        return redirect(url_for('user.dashboard'))
    else:
        return render_template('home.html'), 200

app.register_blueprint(user_route)

#* Login Manager
login_manager = LoginManager()
login_manager.init_app(app)
@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

#* Email
mail.init_app(app)

#* Session
session.init_app(app)

#* Socket.io
socketio.init_app(app, manage_session=False)

@socketio.on('connect')
def on_connect():
    if current_user.is_authenticated:
        print(f'\033[92m>>>>>>>>>> {current_user.username} connected. <<<<<<<<<<\033[0m')
    else:
        print('>>>>>>>>>> Anonymous connected. <<<<<<<<<<')

@socketio.on('disconnect')
def on_disconnect():
    if current_user.is_authenticated:
        print(f'\033[96m>>>>>>>>>> {current_user.username} disconnected. <<<<<<<<<<\033[0m')
    else:
        print('>>>>>>>>>> Anonymous disconnected. <<<<<<<<<<')


#* Error Handlers
@app.errorhandler(exceptions.BadRequest)
def handle_400(err):
    return jsonify({"message": f"{err.description}"}), 400
@app.errorhandler(exceptions.NotFound)
def handle_404(err):
    return jsonify({"message": f"Fallout 4, I think you are lost."}), 404
@app.errorhandler(exceptions.InternalServerError)
def handle_500(err):
    return jsonify({"message": f"Oops, that probably is our fault."}), 500
@app.errorhandler(exceptions.MethodNotAllowed)
def handle_405(err):
    return jsonify({"message": f"Naughty method is not allowed"}), 405
@app.errorhandler(exceptions.Conflict)
def handle_409(err):
    return jsonify({"message": f"{err.description}"}), 409

if __name__ == "__main__":
    app.run(debug=True)

