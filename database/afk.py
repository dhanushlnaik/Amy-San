import discord
from discord.ext import commands
import pyrebase
from json import loads , load 
import time

with open("firebase.json", "r") as read_file:
    firebase = pyrebase.initialize_app(load(read_file))
db = firebase.database()

AFK_VAR = {
    "AFK" : True,
    "MESSAGE" : "Something",
    "TIME": 0,
    "PING" : 0
}

def afkcreate(id, guild, message):
    db.child("AFKs").child(id).child(guild).set({"AFK" : True, "MESSAGE": message, "PING": 0, "TIME": f"{time.time()}"})


def checkafk(id, guild):
    if db.child("AFKs").child(id).child(guild).get().val() == None:
        return False
    check = db.child("AFKs").child(id).child(guild).child("AFK").get().val()
    if check == None or check == False:
        return False
    elif check == True:
        return True

def get_afk_message(id, guild):
    message = db.child("AFKs").child(id).child(guild).child("MESSAGE").get().val()
    return message

def get_time(id, guild):
    time = db.child("AFKs").child(id).child(guild).child("TIME").get().val()
    return time

def get_ping(id, guild):
    ping = db.child("AFKs").child(id).child(guild).child("PING").get().val()
    return ping

def remove_afk(id, guild):
    db.child("AFKs").child(id).child(guild).remove()

def add_ping(id, guild):
    ping = db.child("AFKs").child(id).child(guild).child("PING").get().val()
    if ping == None:
        return 0
    ping += 1
    ping = db.child("AFKs").child(id).child(guild).child("PING").set(ping)