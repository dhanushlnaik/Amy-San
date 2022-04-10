import discord
from discord.ext import commands
import requests
import json
from dotenv import load_dotenv
import os
from imgurpython import ImgurClient
from random import choice , randint
import giphy_client
from giphy_client.rest import ApiException

load_dotenv()
API_KEY = os.environ.get("WEEBY_API_KEY")
imgur = ImgurClient(os.environ.get("IMGUR"),os.environ.get("IMGUR_KEY"))
api_key = os.environ.get("API_KEY")

qcid = 902509178352988220
def return_gif(arg):
    request = requests.get(f"https://weebyapi.xyz/gif/{arg}?token={str(API_KEY)}")
    rjson = json.loads(request.content)
    return rjson['url']

def make_request(): # Get Quote
    response = requests.get("https://animechan.vercel.app/api/random", verify=False)
    resp = json.loads(response.content)
    return resp['anime'], resp['character'], resp['quote']

class Anime(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot
        self.emoji = "꒰ <a:EmiPuck:943366309775835247> ꒱"
        self.hidden = False
        self.description = "Includes Anime Related Commands."

    @commands.command(aliases=['animequote',"quote"], description=f"Get an Anime Quote!")
    @commands.cooldown(rate=1, per=5, type=commands.BucketType.default)
    async def sendquote(self, ctx):
        """Get an Anime Quote!"""
        anime, char, quote = make_request()
        # await ctx.message.add_reaction('✅')
        emb = discord.Embed(color=discord.Color.greyple())
        emb.set_author(name=f"{quote}\n\n~ {char} | {anime}")
        q = choice([anime, char])
        try:
            api_instance = giphy_client.DefaultApi()
            api_response = api_instance.gifs_search_get(api_key, q, limit=5, rating='g')
            lst = list(api_response.data)
            rgiff = choice(lst)
            emb.set_image(url=f"https://media.giphy.com/media/{rgiff.id}/giphy.gif")
        except ApiException as e:
            print("Exception when calling Api as "+e)
        await ctx.channel.send(embed=emb)

     
def setup(bot):
    bot.add_cog(Anime(bot))