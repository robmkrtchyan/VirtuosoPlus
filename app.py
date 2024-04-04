from flask import Flask, render_template, request, redirect, url_for
from flask_socketio import SocketIO, join_room, leave_room, emit
import secrets
import json
import html
import games.TicTacToe.TicTacToe as ttt

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

ogTicTacToe = ttt.TicTacToe()

rooms = {
    "0000": {
        "game": "TicTacToe",
        "limit": 2,
        "players": [],
        "code": "0000",
        "gboard": ogTicTacToe
    }
}

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/join", methods=['GET','POST'])
def join():
    if request.method == "POST":
        room_code = request.form.get('room_code')
        name = request.form.get('name')
        return redirect(url_for('room', room_code=room_code, username=name))
    return render_template("join.html")

@app.route('/create', methods=['GET','POST'])
def create():
    if request.method == "POST":
        gboard = ttt.TicTacToe()
        game = request.form.get("game_menu")
        name = request.form.get("name")
        room_code = secrets.token_hex(2)  # Generate a unique 4-character room code
        rooms[room_code] = {
            "game": game, 
            "limit": 2,
            "players": [],
            "code": room_code,
            "gboard": gboard
        }
        return redirect(url_for('room', room_code=room_code, username=name))
    return render_template("create.html")
    

@app.route('/room/<room_code>/<username>', methods = ["POST", "GET"])
def room(room_code, username):
    room_info = rooms.get(room_code)
    if room_info:
        if room_info['game'] == 'TicTacToe':
            if request.method == "POST":
                pos = request.form.get("cellIndex")
                rooms[room_info['code']]['gboard'].play(int(pos))
                print(rooms[room_info['code']]['gboard'].getBoard())
            return render_template('tictactoe.html', username=username, room_info = room_info, board = rooms[room_info['code']]['gboard'].toXO())
        return render_template('room.html', username=username, room_info=room_info)
    else:
        return "Room not found!"

@socketio.on('joined', namespace='/create')
def joined(message):
    print("_______________________________")
    print("OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO")
    print(message)
    room_info = messageToDict(message['room_info'])
    print(room_info)
    print(rooms)
    room_code = room_info['code']  # Access the room code correctly
    rooms[room_code]["players"].append(message['username'])
    join_room(room_code)  # Join the correct room
    emit('status', {'msg': message['username'] + ' has joined the room.'}, room=room_code)

@socketio.on('joined', namespace='/join')
def joined(message):
    print("_______________________________")
    print("OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO")
    print(message)
    room_info = messageToDict(message['room_info'])
    print(room_info)
    print(rooms)
    room_code = room_info['code']  # Access the room code correctly
    print(rooms)
    if room_code in rooms.keys():
        rooms[room_code]["players"].append(message['username'])
        join_room(room_code)  # Join the correct room
        emit('status', {'msg': message['username'] + ' has joined the room.'}, room=room_code)
    

@socketio.on('left', namespace='/create')
def left(message):
    room_info = messageToDict(message['room_info'])
    room_code = room_info['code']
    username = message['username']
    if username in rooms[room_code]["players"]:
        rooms[room_code]["players"].remove(username)
    leave_room(room_code)
    rooms[room_code]['gboard'] = ttt.TicTacToe()
    emit('status', {'msg': username + ' has left the room.'}, room=room_code)
    print(rooms)
    
@socketio.on('left', namespace='/join')
def left(message):
    room_info = messageToDict(message['room_info'])
    room_code = room_info['code']
    username = message['username']
    if username in rooms[room_code]["players"]:
        rooms[room_code]["players"].remove(username)
    leave_room(room_code)
    emit('status', {'msg': username + ' has left the room.'}, room=room_code)
    print(rooms)
    



socketio.run(app, debug=True)
'''qwerty'''
