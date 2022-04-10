import datetime
import os
import discord
from discord.ext import commands
import traceback
from database import userdb, guildprefix
import random
import asyncio
from random import choices
from dotenv import load_dotenv
# from pycord_components import PycordComponents
from tools import get_options

load_dotenv()
TOKEN = os.environ.get("TOKEN")
DEFAULT_PREFIX = "a!"
ownerID = ["624174437821972480", "710852927543050292"]
OPTIONS = []

def user_is_me(ctx):
    if str(ctx.message.author.id) in ownerID:
        return True
    else:
        return False

async def prefix_get(bot, message):
    if not message.guild:
        return commands.when_mentioned_or(DEFAULT_PREFIX)(bot, message)
    prefix = guildprefix.check_prefix(message.guild.id)
    return commands.when_mentioned_or(prefix,"a!", "A!")(bot, message)
                      
# Bot Variables
intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix= prefix_get , case_insensitive=True, intents=intents, allowed_mentions=discord.AllowedMentions(everyone=False,users=True,roles=False,replied_user=True))
bot.remove_command("help")


# Load & Unload Cog Functions
def unload_cogs():
    for file in os.listdir("./cogs"):
        if file.endswith(".py") and not file.startswith("_"):
            try:
                bot.unload_extension(f"cogs.{file[:-3]}")
            except Exception as e:
                print(f"COG UNLOAD ERROR : {e}")


def load_cogs():
    print("Loading...")
    for file in os.listdir("./cogs"):
        if file.endswith(".py") and not file.startswith("_"):
             
            try:
                bot.load_extension(f"cogs.{file[:-3]}")
                print(f'> Loaded cog: {file[:-3]}'.title())
            except Exception as e:
                print(f"COG LOAD ERROR : {e}\n\n{traceback.format_exc()}\n\n")


@bot.command(aliases=["reload"], hidden=True)
@commands.check(user_is_me)
async def reloadcogs(ctx):

    unload_cogs()
    load_cogs()
    await ctx.reply("All Cogs Reloaded!")

async def switchpresence():
    await bot.wait_until_ready()
    statuses = ["UR MOM"]
    while not bot.is_closed():
        status = random.choice(statuses)

        await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name=status))
        await asyncio.sleep(10)


@bot.event
async def on_ready():
    print(f"Logged in as : {bot.user.name}\nID : {bot.user.id}")
    # print(f"Total Servers : {len(bot.guilds)}\n")
    # PycordComponents(bot)
    load_cogs()
    print("Bot is ready to roll out\n")
    if not hasattr(bot, "uptime"):
        bot.uptime = datetime.datetime.now()

    print(f"Ready: {bot.user} | Servers: {len(bot.guilds)}")
    a = get_options(bot)
    for o in a:
        OPTIONS.append(o)

bot.loop.create_task(switchpresence())
bot.run(TOKEN)