import os
from flask import Flask, send_from_directory, json, session, render_template
from flask_socketio import SocketIO
from flask_cors import CORS

name_arr = []

app = Flask(__name__, static_folder='./build/static')

cors = CORS(app, resources={r"/*": {"origins": "*"}})

socketio = SocketIO(
    app,
    cors_allowed_origins="*",
    json=json,
    manage_session=False
)
@app.route('/register')
def new_user():
    return render_template("login.html")

@app.route('/', defaults={"filename": "index.html"})
@app.route('/<path:filename>')
def index(filename):
    return send_from_directory('./build', filename)

# When a client connects from this Socket connection, this function is run
@socketio.on('connect')
def on_connect():
    print('User connected!')

# When a client disconnects from this Socket connection, this function is run
@socketio.on('disconnect')
def on_disconnect():
    print('User disconnected!')
    
#When a Client enters a username and emits the event 'name', this function is run
@socketio.on('name')
def on_name(data):
    print(str(data))
    name_arr.append(data['message'])
    playerSize = len(name_arr)
    
    if (playerSize == 1):
        playerType = 1
    elif (playerSize == 2):
        playerType = 2
    elif (playerSize > 2 ):
        playerType = 3   
    
    print('User ' + str(data['message']) + ' has connected')
    socketio.emit(name_arr[-1], [playerType, data], broadcast=True, include_self=False)
    socketio.emit('name', name_arr, broadcast=True, include_self=False)

# When a client emits the event 'chat' to the server, this function is run
# 'chat' is a custom event name that we just decided
@socketio.on('tic')
def on_chat(data): # data is whatever arg you pass in your emit call on client
    print(str(data))
    # This emits the 'chat' event from the server to all clients except for
    # the client that emmitted the event that triggered this function
    socketio.emit('tic',  data, broadcast=True, include_self=False)

# Note that we don't call app.run anymore. We call socketio.run with app arg
socketio.run(
    app,
    host=os.getenv('IP', '0.0.0.0'),
    port=8081 if os.getenv('C9_PORT') else int(os.getenv('PORT', 8081)),
)