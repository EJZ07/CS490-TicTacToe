import os
from flask import Flask, send_from_directory, json, session, render_template
from flask_socketio import SocketIO
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv, find_dotenv
from flask_socketio import SocketIO

name_arr = []
playerType = 0

load_dotenv(find_dotenv())

app = Flask(__name__, static_folder='./build/static')

# Point SQLAlchemy to your Heroku database
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
# Gets rid of a warning
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# IMPORTANT: This must be AFTER creating db variable to prevent
# circular import issues
import sqlalchemy
from app import db
import models
db.create_all()

models.Username.query.all()

cors = CORS(app, resources={r"/*": {"origins": "*"}})

socketio = SocketIO(app,
                    cors_allowed_origins="*",
                    json=json,
                    manage_session=False)


@app.route('/register')
def new_user():
    return render_template("login.html")


@app.route('/', defaults={"filename": "index.html"})
@app.route('/<path:filename>')
def index(filename):
    # Note that we don't call app.run anymore. We call socketio.run with app arg
    return send_from_directory('./build', filename)


    # When a client connects from this Socket connection, this function is run
@socketio.on('connect')
def on_connect():
    print('User connected!')


# When a client disconnects from this Socket connection, this function is run
@socketio.on('disconnect')
def on_disconnect():
    all_people = models.Username.query.all()
    for user in all_people:
        db.session.delete(user)
        db.session.commit()
    print('User disconnected!')


@socketio.on('goodbye_all')
def on_gbAll():
    global name_arr
    name_arr = []
    print('Everyone is gone')


@socketio.on('goodbye')
def on_gb(data):
    global name_arr
    name_arr.remove(data)
    print(data + ' is gone')


#When a Client enters a username and emits the event 'name', this function is run
@socketio.on('name')
def on_name(data):
    print(str(data))
    name_arr = add_user(data['message'])
    playerSize = len(name_arr)

    if (playerSize == 1):
        playerType = 1
    elif (playerSize == 2):
        playerType = 2
    elif (playerSize > 2):
        playerType = 3

    if (playerType < 3):
        socketio.emit('name', [name_arr, 100], broadcast=True, include_self=True)

    print('User ' + str(data['message']) + ' has connected')
    socketio.emit(name_arr[-1], [playerType, data],
                  broadcast=True,
                  include_self=True)
    #socketio.emit('name', [name_arr, 100], broadcast=True, include_self=False)

def add_user(username):
   
    new_name = models.Username(username=username, score=100)
    db.session.add(new_name)
    #db.session.query(models.Username).order_by(models.Username.id)
    db.session.commit()
    all_people = models.Username.query.all()
    name_arr = []
    for user in all_people:
        name_arr.append(user.username)
    
    return name_arr
        
# When a client emits the event 'chat' to the server, this function is run
# 'chat' is a custom event name that we just decided
@socketio.on('tic')
def on_chat(data):  # data is whatever arg you pass in your emit call on client
    print(str(data))
    # This emits the 'chat' event from the server to all clients except for
    # the client that emmitted the event that triggered this function
    socketio.emit('tic', data, broadcast=True, include_self=True)


@socketio.on('score')
def on_score(data):
    change = new_score(data)

    print("New score: " + str(change[0]))
    socketio.emit('score', [data['message'], change[0], change[1]],
                  broadcast=True,
                  include_self=True)
def new_score(win_data):
    if (win_data['message'] == 'X'):
        print("Winner " + str(win_data['playerBase'][0]))
        winner = models.Username.query.filter_by(
            username=win_data['playerBase'][0]).first()
        winner.score += 1
        loser = models.Username.query.filter_by(
            username=win_data['playerBase'][1]).first()
        loser.score -= 1
        db.session.commit()
    elif (win_data['message'] == 'O'):
        winner = models.Username.query.filter_by(
            username=win_data['playerBase'][1]).first()
        winner.score += 1
        loser = models.Username.query.filter_by(
            username=win_data['playerBase'][0]).first()
        loser.score -= 1
        db.session.commit()
    
    return [winner.score, loser.score]

@socketio.on('reset')
def on_reset(data):
    socketio.emit('reset', data, broadcast=True, include_self=True)


if __name__ == "__main__":
    socketio.run(
        app,
        host=os.getenv('IP', '0.0.0.0'),
        port=8081 if os.getenv('C9_PORT') else int(os.getenv('PORT', 8081)),
    )
