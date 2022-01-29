import requests
import socketio

import game

sio = socketio.Client()

def printRoom(gameID: int) -> None:
    print("Room:", gameID)

@sio.event
def connect():
    print("I'm connected!")

@sio.event
def connect_error(data):
    print("The connection failed!")

@sio.event
def disconnect():
    print("I'm disconnected!")

sio.connect("http://localhost:5000")
sio.emit("new_game", 7, callback=printRoom)