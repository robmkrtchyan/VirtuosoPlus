from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

#keeps all the rooms
rooms = {
    "0000": {
        "game": "TicTacToe",
        "limit": 2,
        "players": 0
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
    game = request.form.get("game_menu")
    room_code = "QQQQ"
    rooms[room_code] = {
        "game": game, 
        "limit": 2,
        "players": 0
    }
    
    if (request.method == "POST" ):
        return redirect(url_for('room', room_code=room_code))
    return render_template("create.html")
    

@app.route('/room/<room_code>')
def room(room_code):
    room_info = rooms.get(room_code)
    print(rooms[room_code])
    if room_info:
        return render_template('room.html', room_info=room_info)
    else:
        return "Room not found!"
    
    
app.run(debug=True)