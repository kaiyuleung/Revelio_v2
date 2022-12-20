from flask import Blueprint, jsonify, request, redirect, url_for, render_template
from werkzeug import exceptions

#* Login
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from tool import get_random_string, get_random_avatar

#* Email
from flask_mail import Mail, Message
mail = Mail()

#* Socket.io
from flask_socketio import SocketIO, disconnect, emit
import functools
socketio = SocketIO()
def authenticated_only(f):
    @functools.wraps(f)
    def wrapped(*args, **kwargs):
        if not current_user.is_authenticated:
            disconnect()
        else:
            return f(*args, **kwargs)
    return wrapped

#* Session
from flask_session import Session
session = Session()

#* MVC
from ..models.user import User
from ..database.db import db
from ..controllers import users

user = Blueprint("user", __name__)

@user.route("/dashboard")
def dashboard():
    if (current_user.is_authenticated):
        return render_template('dashboard.html', user = current_user, user_stats = users.stats(current_user)), 200
    else:
        return redirect(url_for('home'))

@user.route("/login", methods=['POST'])
def login():
    userData = request.form
    foundUsername = User.query.filter_by(username=str(userData['username'])).first()
    if (foundUsername and check_password_hash(foundUsername.password, userData['password'])):
        login_user(foundUsername, remember=True)
        return redirect(url_for('user.dashboard'))
    else:
        raise exceptions.BadRequest(f"Failed login! \nIncorrect login details")

@user.route("/register", methods=['POST'])
def register():
    userData = request.json
#* Check register detail
# # Empty username
# if not (userData["username"] or len(userData["username"])):
#     return exceptions.BadRequest("username cannot be empty")
# # Empty password
# if not (userData["password"] or len(userData["password"])):
#     return exceptions.BadRequest("password cannot be empty")
# # Invalid email
# if not ("@" in userData["email"] or "." in userData["email"]):
#     return exceptions.BadRequest("Invalid Email")
# Unmatched email
    if (userData['email'] != userData['confirm_email']):
        return {"message": "Email does not match"}, 400
    # Unmatched password
    if (userData['password'] != userData['confirm_password']):
        return {"message": "Password does not match"}, 400

    
    if (User.query.filter_by(username=str(userData["username"])).first()):
        return {"message": "User already exists"}, 409
    else:
        new_user = User(
            username = userData["username"], 
            email = userData["email"],
            password = generate_password_hash(userData["password"], method='sha256'),
            OTP = get_random_string(),
            wins = 0, 
            wins_as_hunter = 0, 
            games_played = 0,
            avatar_url = get_random_avatar(),
            )
        db.session.add(new_user)
        db.session.commit()
        
        login_user(new_user, remember=True)
        
        username = userData["username"]
        msg = Message(
            f"Thank you for register an account with us, {username}!", 
            sender='gustafsson_revelio@outlook.com',
            recipients=[userData["email"]])
        msg.html = "<h1>Revelio Welcomes you!</h1>"
        msg.msgId = msg.msgId.split('@')[0] + '@Revelio'
        mail.send(msg)
        return {"message": "User created"}, 200

@user.route("/forgot_password", methods=['GET', 'POST'])
def forgotPassword():
    if (request.method == 'GET'):
        return render_template('forgot_password.html'), 200
    elif (request.method == 'POST'):
        #? {
        #?     "username": "",
        #?     "email": ""
        #? }
        userData = request.json
        if not ('username' in userData and 'email' in userData):
            return {"message": "You need to have corresponding username and email to reset your password."}, 400
        try:
            # user can use the same email to register muiltiply accounts with different username
            foundUsername = User.query.filter_by(username=str(userData['username'])).first()
            if(foundUsername.email == userData['email']):
                foundUsername.OTP = get_random_string()
                db.session.commit()
                msg = Message(
                    f"Here is your OTP, {foundUsername.username}!", 
                    sender='gustafsson_revelio@outlook.com',
                    recipients=[userData["email"]])
                msg.html = f"<h1>Here is your 8-characters OTP for your Revelio account:<br> {foundUsername.OTP}</h1><h2><a href='https://revelio.netlify.app/' >Link to reset</a></h2>"
                msg.msgId = msg.msgId.split('@')[0] + '@Revelio'
                mail.send(msg)
            return { "message": "Please check your Email inbox for resetting the password" }, 200
        except:
            return { "message": "Please check your Email inbox for resetting the password" }, 200

@user.route("/reset_password", methods=['GET', 'PATCH'])
def resetPassword():
    if (request.method == 'GET'):
        return render_template('reset_password.html'), 200
    elif (request.method == 'PATCH'):
        #? {
        #?     "username": "",
        #?     "OTP": "",
        #?     "new_password": "",
        #? }
        userData = request.json
        print(userData)
        if not ('username' in userData and 'OTP' in userData and 'new_password' in userData):
            return { "message" : "You need to have corresponding username, OTP, new_password to reset your password." }, 400
        
        foundUsername = User.query.filter_by(username=str(userData['username'])).first()
        if(foundUsername and foundUsername.OTP == userData['OTP']):
            foundUsername.password = generate_password_hash(userData["new_password"], method='sha256')
            foundUsername.OTP = get_random_string()
            db.session.commit()
            return "Reset Password Successful!", 200
        return { "message" : "Failed to reset! \nIncorrect details" }, 400

@user.route("/logout")
@login_required
def logout():
    logout_user()
    return "Logged out.", 200

# @user.route("/profile")
# @login_required
# def profile():
#     stats = { 
#         "avatar_url": current_user.avatar_url,
#         "wins": current_user.wins,
#         "wins_as_hunter": current_user.wins_as_hunter,
#         "games_played": current_user.games_played,
#     }
#     return jsonify(stats)

@user.route("/stats-update", methods=['PATCH'])
@login_required
def stats_update():
    #? PATCH to http://127.0.0.1:3030/stats-update
    #? {
    #?     "win": true,
    #?     "win_as_hunter": true
    #? }
    
    current_user.games_played += 1
    
    # win = Boolean
    if request.json['win']:
        current_user.wins += 1
    
    # win_as_hunter = Boolean
    if request.json['win_as_hunter']:
        current_user.wins_as_hunter += 1
        
    if request.json['win_as_hunter'] and not request.json['win']:
        raise exceptions.BadRequest(f"you cannot lose but win as hunter at the same time")
    
    db.session.commit()
    
    stats = { 
        "wins": current_user.wins,
        "wins_as_hunter": current_user.wins_as_hunter,
        "games_played": current_user.games_played,
    }
    return jsonify(stats)
