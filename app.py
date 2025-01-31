from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit
import random

app = Flask(__name__)
socketio = SocketIO(app)

users = {}

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('connect')
def handle_connect():
    username = f'User{random.randint(1, 100)}'
    gender = random.choice(["girl", "boy"])
    avatar_url = f'https://avatar.iran.liara/run/public/{gender}?username={username}'

    users[request.sid] = {"username": username, "avatar_url": avatar_url}

    emit('user_joined', {"username": username, "avatar_url": avatar_url}, broadcast=True)
    emit('set_username', {"username" : username})

@socketio.on('disconnect')
def handle_disconnect():
    user = users.pop(request.sid, None)
    if user:
        emit('user_left', {"username": user["username"]}, broadcast=True)

@socketio.on('send_message')
def handle_send_message(data):
    user = users.get(request.sid)
    if user:
        emit('new_message', {"username": user["username"], "avatar_url": user["avatar_url"], "message": data["message"]}, broadcast=True)

@socketio.on('change_username')
def handle_change_username(data):
    old_username = users[request.sid]["username"]
    new_username = data["username"]
    users[request.sid]["username"] = new_username

    emit('user_changed_username', {"old_username": old_username, "new_username": new_username}, broadcast=True)
    
    emit('user_left', {"username": username}, broadcast=True)

if __name__ == '__main__':
    socketio.run(app)

