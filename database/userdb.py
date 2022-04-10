import pyrebase
from json import loads , load 
import datetime
import time
import discord

with open("firebase.json", "r") as read_file:
    firebase = pyrebase.initialize_app(load(read_file))
db = firebase.database()


disct = {
    "siblings" : "0",
    "profile" : True,
    "currency" : 0,
    "partner" : {
            "id": "0",
            "date": "0",
            "day": "0",
            "ring" : "0",
            "dates" : 0,
            "scores": 0,
            "dateToday": False
        },
            "actions" : {
            "hug" : {"received" : 0 , "given": 0},
            "pat" : {"received" : 0 , "given": 0},
            "punch" : {"received" : 0 , "given": 0},
            "kiss" : {"received" : 0 , "given": 0},
            "cuddle" : {"received" : 0 , "given": 0},
            "slap" : {"received" : 0 , "given": 0},
            "handhold" : {"received" : 0 , "given": 0},
            "poke" : {"received" : 0 , "given": 0},
            "bonk" : {"received" : 0 , "given": 0},
            "kill" : {"received" : 0 , "given": 0},
            "tickle" : {"received" : 0 , "given": 0}
        }
        }

# New Member
def new_member(id: str):
    db.child("USER").child(id).set(disct)

# PARTNER VARS
def checkPartner(id : str, val):
    if db.child("USER").child(id).get().val() == None:
        new_member(id)
    partnerVar = db.child("USER").child(id).child("partner").child(val).get().val()
    return partnerVar

def change_date(id, v:bool):
    if db.child("USER").child(id).get().val() == None:
        new_member(id)  
    db.child("USER").child(id).child("partner").child("dateToday").set(False) 

def addPartner(id: str, ctx, val):
    if db.child("USER").child(id).get().val() == None:
        new_member(id)
    if is_sibling(id, val):
        return
    if ctx.lower() == "id":
        db.child("USER").child(id).child("partner").child(ctx).set(val)
        return
    elif ctx.lower() == "date":
        val = str(datetime.datetime.now().strftime("%a, %B %d,%Y"))
        db.child("USER").child(id).child("partner").child(ctx).set(val)
        return
    elif ctx.lower() == "day":
        val = str(datetime.date.today())
        db.child("USER").child(id).child("partner").child(ctx).set(val)
        return
    elif ctx.lower() == "ring":
        db.child("USER").child(id).child("partner").child(ctx).set(val)
        return
    elif ctx.lower() == "dates":
        org = db.child("USER").child(id).child("partner").child(ctx).get().val()
        org += int(val)
        db.child("USER").child(id).child("partner").child(ctx).set(org)
        return
    elif ctx.lower() == "scores":
        org = db.child("USER").child(id).child("partner").child(ctx).get().val()
        org += int(val)
        db.child("USER").child(id).child("partner").child(ctx).set(org)
        return
    else:
        return

def rmvPartner(id: str):
    val = "0"
    if db.child("USER").child(id).get().val() == None:
        new_member(id)
    db.child("USER").child(id).child("partner").child("id").set(val)
    db.child("USER").child(id).child("partner").child("date").set(val)
    db.child("USER").child(id).child("partner").child("day").set(val)
    db.child("USER").child(id).child("partner").child("ring").set(val)

def show_date(user_id: str, ctx):
    guild_relationship = db.child("USER").child(user_id).child(ctx).get().val()
    if guild_relationship == None:
        new_member(user_id)
        guild_relationship = db.child("USER").child(user_id).child(ctx).get().val()
    date = guild_relationship["date"]
    return date

def show_day(user_id: str, ctx):
    guild_relationship = db.child("USER").child(user_id).child(ctx).get().val()
    if guild_relationship == None:
        new_member(user_id)
        guild_relationship = db.child("USER").child(user_id).child(ctx).get().val()
    days = guild_relationship["days"]
    return days

def date_today(id:str):
    if db.child("USER").child(id).get().val() == None:
        new_member(id)
    partnerVar = db.child("USER").child(id).child("partner").child("dateToday").get().val()
    return partnerVar

# COMPARE
def is_sibling(rel1:str, rel2: str):
    rel = db.child("USER").child(rel1).child("siblings").get().val()
    q= rel.split(",")
    if str(rel2) in q:
        return True
    else:
        return False

def is_partner(rel1: str, rel2:str):
    prsn1 = db.child("USER").child(rel1).get().val()
    if prsn1 == None:
        new_member(rel1)
        
    prsn1 = db.child("USER").child(rel1).child("partner").child("id").get().val()
    if str(prsn1) == str(rel2):
        return True
    else:
        return False

def is_married(rel1):
    prsn1 = db.child("USER").child(rel1).get().val()
    if prsn1 == None:
        new_member(rel1)
        
    prsn1 = db.child("USER").child(rel1).child("partner").child("id").get().val()
    if str(prsn1) == "0":
        return False
    else:
        return True
# Profile
def enableProfile(id: str):
    guild_val = db.child("USER").child(id).get().val()
    if guild_val == None:
        new_member(id)
        guild_val = db.child("USER").child(id).get().val()
    guild_val["profile"] = True
    db.child("USER").child(id).set(guild_val)
    
def disableProfile(id: str):
    guild_val = db.child("USER").child(id).get().val()
    if guild_val == None:
        new_member(id)
        guild_val = db.child("USER").child(id).get().val()
    guild_val["profile"] = False
    db.child("USER").child(id).set(guild_val)
    
def is_profile_enabled(id: str):
    guild_val = db.child("USER").child(id).get().val()
    if guild_val == None:
        new_member(id)
        guild_val = db.child("USER").child(id).get().val()
    if guild_val["profile"] == True:
        return True
    else:
        return False

# SIB
def rmvSib(id: str, relID: str):
    sib = db.child("USER").child(id).child("siblings").get().val()
    li = sib.split(',')
    if sib == "0":
        return
    if relID in li:
        li.remove(relID)
        sib = ','.join(li)
        db.child("USER").child(id).child("siblings").set(sib)
    else:
        return

def addSib(id: str, relID: str):
    if db.child("USER").child(id).get().val() == None:
        new_member(id)
    if is_partner(id, relID):
        return
    sib = db.child("USER").child(id).child("siblings").get().val()
    if sib == "0":
        sib = str(relID)
    else:
        sib = str(sib)+ "," + str(relID)
    db.child("USER").child(id).child("siblings").set(sib)

def showSib(id:str):
    if db.child("USER").child(id).get().val() == None:
        new_member(id)
    return db.child("USER").child(id).child("siblings").get().val()


# Currency

def addmoney(id: str, money:int):
    if db.child("USER").child(id).get().val() == None:
        new_member(id)
    val = db.child("USER").child(id).child("currency").get().val()
    val += money
    db.child("USER").child(id).child("currency").set(val)

def rmvmoney(id: str, money:int):
    if db.child("USER").child(id).get().val() == None:
        new_member(id)
    val = db.child("USER").child(id).child("currency").get().val()
    val = val - money
    db.child("USER").child(id).child("currency").set(val)

def showMoney(id: str, money:int):
    if db.child("USER").child(id).get().val() == None:
        new_member(id)
    val = db.child("USER").child(id).child("currency").get().val()
    return val

def addaction(id: str, action ,ctx):
    if db.child("USER").child(id).get().val() == None:
        new_member(id)
    actionnum = db.child("USER").child(id).child("actions").child(action).child(ctx).get().val()
    actionnum = int(actionnum) + 1
    db.child("USER").child(id).child("actions").child(action).child(ctx).set(str(actionnum))

def showaction(id: str, action ,ctx):
    if db.child("USER").child(id).get().val() == None:
        new_member(id)
    action = db.child("USER").child(id).child("actions").child(action).child(ctx).get().val()
    return action



async def get_guild_Mlb(bot, guild: discord.Guild, auth):
    lb_dict = {}
    desc = f""
    all_users = db.child("USER").get()
    for user in all_users.each():
        uid = user.key()
        if guild.get_member(int(uid)) is not None:
            h = db.child("USER").child(uid).child("currency").get().val()
            lb_dict[uid] = h
    sort_lb = dict(sorted(lb_dict.items(), key=lambda x: x[1], reverse=True))
    slb = dict(list(sort_lb.items())[:10])
    for u in slb: 
        
        pos = list(slb.keys()).index(u) + 1
        he = sort_lb[u]
        if pos == 1:
            he = db.child("USER").child(u).child("currency").get().val()
            desc += f"`#01.` `{discord.utils.get(bot.get_all_members(), id=int(u))}`\n> Currency : `{he}`\n"
        elif pos == 10:  # ONE SPACE LESSER
            he = db.child("USER").child(u).child("currency").get().val()
            desc += f"`#{str(pos)}.` `{discord.utils.get(bot.get_all_members(), id=int(u))}`\n> Currency : `{he}`\n"
        else:
            he = db.child("USER").child(u).child("currency").get().val()
            desc += f"`#0{str(pos)}.`  `{discord.utils.get(bot.get_all_members(), id=int(u))}`\n> Currency : `{he}`\n"
    posi = list(sort_lb.keys()).index(str(auth.id)) + 1
    if posi > 10:
        he = db.child("USER").child(u).child("currency").get().val()
        desc += f".\n.\n`#{str(posi)}.` `{auth}` \n> Currency : `{he}`\n"
    emb = discord.Embed(title=f"Top 10 Amy-Rankings - Guild", color=discord.Color.blurple(), description=desc)

    return emb       


async def get_Mb(bot, auth):
    lb_dict = {}
    desc = f""
    all_users = db.child("USER").get()
    for user in all_users.each():
        uid = user.key()
        h = db.child("USER").child(uid).child("currency").get().val()
        lb_dict[uid] = h
    sort_lb = dict(sorted(lb_dict.items(), key=lambda x: x[1], reverse=True))
    slb = dict(list(sort_lb.items())[:10])
    for u in slb: 
        
        pos = list(slb.keys()).index(u) + 1
        he = sort_lb[u]
        if pos == 1:
            he = db.child("USER").child(u).child("currency").get().val()
            desc += f"`#01.` `{discord.utils.get(bot.get_all_members(), id=int(u))}`\n> Currency : `{he}`\n"
        elif pos == 10:  # ONE SPACE LESSER
            he = db.child("USER").child(u).child("currency").get().val()
            desc += f"`#{str(pos)}.` `{discord.utils.get(bot.get_all_members(), id=int(u))}`\n> Currency : `{he}`\n"
        else:
            he = db.child("USER").child(u).child("currency").get().val()
            desc += f"`#0{str(pos)}.`  `{discord.utils.get(bot.get_all_members(), id=int(u))}`\n> Currency : `{he}`\n"
    posi = list(sort_lb.keys()).index(str(auth.id)) + 1
    if posi > 10:
        he = db.child("USER").child(u).child("currency").get().val()
        desc += f".\n.\n`#{str(posi)}.` `{auth}` \n> Currency : `{he}`\n"
    emb = discord.Embed(title=f"Top 10 Amy-Rankings - Global", color=discord.Color.blurple(), description=desc)
    emb.set_author(
        name="Global Marriage Leaderboard",
        icon_url=auth.display_avatar
    )
    return emb  