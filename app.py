from flask import Flask, render_template, request, redirect, url_for
from flask_socketio import SocketIO, join_room, leave_room, emit
import secrets
import json
import html

app = Flask(__name__)
app.config["SECRET_KEY"] = secrets.token_hex(16)
socketio = SocketIO(app)

def messageToDict(encrypted_string):
    # Replace the special characters with quotes
    encrypted_string = encrypted_string.replace("&#39;", '"')
    
    try:
        # Convert the string to a dictionary
        decrypted_dict = json.loads(encrypted_string)
        return decrypted_dict
    except json.JSONDecodeError as e:
        print("Error decoding JSON:", e)
        return None



rooms = {
    "0000": {
        "game": "TicTacToe",
        "limit": 2,
        "players": [],
        "code": "0000"
    }
}

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/join")
def join():
    return render_template("join.html")

@app.route('/create', methods=['GET','POST'])
def create():
    if request.method == "POST":
        game = request.form.get("game_menu")
        name = request.form.get("name")
        room_code = secrets.token_hex(2)  # Generate a unique 4-character room code
        rooms[room_code] = {
            "game": game, 
            "limit": 2,
            "players": [],
            "code": room_code
        }
        return redirect(url_for('room', room_code=room_code, username=name))
    return render_template("create.html")
    

@app.route('/room/<room_code>/<username>')
def room(room_code, username):
    room_info = rooms.get(room_code)
    if room_info:
        return render_template('room.html', username=username, room_info=room_info)
    else:
        return "Room not found!"

@socketio.on('joined', namespace='/create')
def joined(message):
    print("_______________________________")
    print("OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO")
    print(message)
    message = messageToDict(message)
    print(message)
    room_code = message['code']  # Access the room code correctly
    rooms[room_code]["players"].append(message["username"])
    join_room(room_code)  # Join the correct room
    emit('status', {'msg': message['username'] + ' has joined the room.'}, room=room_code)

socketio.run(app, debug=True)
