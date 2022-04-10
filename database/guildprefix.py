import discord
from discord.ext import commands
import pyrebase
from json import loads , load 
import time

with open("firebase.json", "r") as read_file:
    firebase = pyrebase.initialize_app(load(read_file))
db = firebase.database()

GUILD ={
    "prefix" : "a!",
    "blacklist" : "0"
}

def new_guild(guild):
    db.child("GUILD").child(guild).set(GUILD)

def add_prefix(guild_id: int, prefix: str):
    guild_prefix = db.child("GUILD").child(guild_id).get().val()
    if guild_prefix == None:
        new_guild(guild_id)
    guild_prefix["prefix"] = prefix
    db.child("GUILD").child(guild_id).set(guild_prefix)

def check_prefix(guild_id: int):
    guild_prefix = db.child("GUILD").child(guild_id).get().val()
    if guild_prefix == None:
        new_guild(guild_id)
        guild_prefix = db.child("GUILD").child(guild_id).get().val()
    prefix = str(guild_prefix["prefix"])
    return prefix

def add_blacklist(guild_id: int, channelId: str):
    guild_data = db.child("GUILD").child(guild_id).get().val()
    if guild_data == None:
        new_guild(guild_id)
    if guild_data["blacklist"] == "0":
        guild_data["blacklist"] = str(channelId)
    else:
        guild_data["blacklist"] = str(guild_data["blacklist"])+ "," + str(channelId)
    db.child("GUILD").child(guild_id).set(guild_data)
    return


def check_channel(guild_id: int ):
    guild_data = db.child("GUILD").child(guild_id).get().val()
    if guild_data == None:
        new_guild(guild_id)
        guild_data = db.child("GUILD").child(guild_id).get().val()
    relation = guild_data["blacklist"]
    return relation

def is_channel_blacklisted(guild_id: int, channel_id):
    guild_data = str(check_channel(int(guild_id)))
    q= guild_data.split(",")
    if str(channel_id) in q:
        return True
    else:
        return False

def remv_blacklist(guild, channel):
    guild_data = db.child("GUILD").child(guild).get().val()
    li = guild_data["blacklist"].split(",")
    if guild_data["blacklist"] == "0":
        return 0
    if channel in li:
        li.remove(channel)
        guild_data["blacklist"] = ",".join(li)
        db.child("GUILD").child(guild).set(guild_data)
    elif not channel in li:
        return 1
    else:
        return None


