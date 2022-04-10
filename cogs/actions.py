import discord
from discord.ext import commands
from PIL import Image, ImageDraw
from io import BytesIO
import requests
import json
import random
from dotenv import load_dotenv
import os
from database import userdb
import random
from tools import return_gif


class Actions(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.emoji = "꒰ <:EmotesCategory:943427911027925082> ꒱"
        self.hidden = False
        self.description = "Includes Roleplay/Action Commands."

    @commands.command(name=f"hug",aliases=[],usage="`< user >`", description=f"Hug a User.")
    async def hug(self, ctx, m: discord.Member = None):
        """Hug a User."""
        if m == None:
            await ctx.send("Please mention someone to hug!")
            return
        if userdb.is_partner(m.id, ctx.author.id):
            num = random.randint(1 , 5)
            emb = discord.Embed(description=f"{ctx.author.mention} hugs {m.mention} ~~ awiee!\n Umhmm :smirk: You Both Look Adorable, Here's your {num} UwU points!", color=ctx.author.color)
            userdb.addaction(ctx.author.id, "hug", "given")
            userdb.addaction(m.id, "hug", "received")
            userdb.addPartner(ctx.author.id, "scores", num)
            userdb.addPartner(m.id, "scores", num)
            given = userdb.showaction(ctx.author.id, "hug", "given")
            received = userdb.showaction(ctx.author.id, "hug", "received")
            emb.set_footer(text=f"{ctx.author.name} gave others {given} hugs and received {received} hugs")
            emb.set_image(url=return_gif("hug"))
            return await ctx.send(embed=emb)
        if m == ctx.author:
            await ctx.send(f"{ctx.author.mention} Do you need someone to hug..? I can hug you :)")
        else:
            emb = discord.Embed(description=f"{ctx.author.mention} hugs {m.mention} ~~ awiee!", color=ctx.author.color)
            userdb.addaction(ctx.author.id, "hug", "given")
            userdb.addaction(m.id, "hug", "received")
            given = userdb.showaction(ctx.author.id, "hug", "given")
            received = userdb.showaction(ctx.author.id, "hug", "received")
            emb.set_footer(text=f"{ctx.author.name} gave others {given} hugs and received {received} hugs")
            emb.set_image(url=return_gif("hug"))
            await ctx.send(embed=emb)

    @commands.command(name=f"pat",usage="`< user >`", description=f"Pat a User.")
    async def pat(self, ctx, m: discord.Member = None):
        """Pat a User."""
        if m == None:
            return await ctx.send("Please mention someone to pat!")
        if userdb.is_partner(m.id, ctx.author.id):
            num = random.randint(1 , 5)
            userdb.addPartner(ctx.author.id, "scores", num)
            userdb.addPartner(m.id, "scores", num)
            emb = discord.Embed(description=f"{ctx.author.mention} pats {m.mention} ~~ awiee!\n Umhmm :smirk: You Both Look Adorable, Here's your {num} UwU points!", color=ctx.author.color)
            userdb.addaction(ctx.author.id, "pat", "given")
            userdb.addaction(m.id, "pat", "received")
            given = userdb.showaction(ctx.author.id, "pat", "given")
            received = userdb.showaction(ctx.author.id, "pat", "received")
            emb.set_footer(text=f"{ctx.author.name} gave others {given} pats and received {received} pats")
            emb.set_image(url=return_gif("pat"))
            return await ctx.send(embed=emb)
        if m == ctx.author:
            await ctx.send(f"{ctx.author.mention} Do you need someone to pat..? I can pat you :)")
        else:
            emb = discord.Embed(description=f"{ctx.author.mention} pats {m.mention} ~~ awiee!", color=ctx.author.color)
            userdb.addaction(ctx.author.id, "pat", "given")
            userdb.addaction(m.id, "pat", "received")
            given = userdb.showaction(ctx.author.id, "pat", "given")
            received = userdb.showaction(ctx.author.id, "pat", "received")
            emb.set_footer(text=f"{ctx.author.name} gave others {given} pats and received {received} pats")
            emb.set_image(url=return_gif("pat"))
            await ctx.send(embed=emb)
    
    @commands.command(name=f"punch",aliases=[],usage="`< user >`", description=f"Punch a User.")
    async def punch(self, ctx, m: discord.Member = None):
        """Punch a User."""
        if m == None:
            await ctx.send("Please mention someone to punch!")
        if m == ctx.author:
            await ctx.send(f"{ctx.author.mention} You want to punch yourself..? Are you sure..?")
        elif m.id == self.bot.user.id:
            emb = discord.Embed(description=f"no u {ctx.author.mention}", color=0xf72585)
            emb.set_image(url="https://c.tenor.com/eaAbCBZy0PoAAAAS/reverse-nozumi.gif")
            await ctx.reply(embed=emb)
        else:
            emb = discord.Embed(description=f"{ctx.author.mention} punches {m.mention} ~ OwO", color=0xf72585)
            userdb.addaction(ctx.author.id, "punch", "given")
            userdb.addaction(m.id, "punch", "received")
            given = userdb.showaction(ctx.author.id, "punch", "given")
            received = userdb.showaction(ctx.author.id, "punch", "received")
            emb.set_footer(text=f"{ctx.author.name} gave others {given} punches and received {received} punches")
            req = requests.get('https://shiro.gg/api/images/punch')
            rjson = json.loads(req.content)
            emb.set_image(url=rjson['url'])
            await ctx.send(embed=emb)

    @commands.command(name=f"kiss",aliases=[],usage="`< user >`",description="Kiss a User.")
    async def kiss(self, ctx, m: discord.Member = None):
        if m == None:
            await ctx.send("Please mention someone to kiss!")
        if userdb.is_partner(m.id, ctx.author.id):
            num = random.randint(1 , 10)
            userdb.addPartner(ctx.author.id, "scores", num)
            userdb.addPartner(m.id, "scores", num)
            emb = discord.Embed(description=f"{ctx.author.mention} kisses {m.mention} ~~ awiee!\n Umhmm :smirk: Thats :flushed:, Here's your {num} UwU points!", color=ctx.author.color)
            userdb.addaction(ctx.author.id, "kiss", "given")
            userdb.addaction(m.id, "kiss", "received")
            given = userdb.showaction(ctx.author.id, "kiss", "given")
            received = userdb.showaction(ctx.author.id, "kiss", "received")
            emb.set_footer(text=f"{ctx.author.name} gave others {given} kisses and received {received} kisses")
            emb.set_image(url=return_gif("kiss"))
            return await ctx.send(embed=emb)
        if m == ctx.author:
            await ctx.send(f"{ctx.author.mention} You want to kiss yourself ...? I can give you a kiss :)")
        emb = discord.Embed(description=f"{ctx.author.mention} kisses {m.mention} ~ cute", color=0xf72585)
        userdb.addaction(ctx.author.id, "kiss", "given")
        userdb.addaction(m.id, "kiss", "received")
        given = userdb.showaction(ctx.author.id, "kiss", "given")
        received = userdb.showaction(ctx.author.id, "kiss", "received")
        emb.set_footer(text=f"{ctx.author.name} gave others {given} kisses and received {received} kisses")
        emb.set_image(url=return_gif("kiss"))
        await ctx.send(embed=emb)
    
    @commands.command(name=f"cuddle",aliases=[],usage="`< user >`",description="Cuddle a User.")
    async def cuddle(self, ctx, m: discord.Member = None):
        if m == ctx.author:
            await ctx.reply("aww, you want a cuddle? I can give you a cuddle :)")
        if userdb.is_partner(m.id, ctx.author.id):
            num = random.randint(1 , 5)
            userdb.addPartner(ctx.author.id, "scores", num)
            userdb.addPartner(m.id, "scores", num)
            emb = discord.Embed(description=f"{ctx.author.mention} cuddles {m.mention} ~~ awiee!\n Umhmm :smirk: You Both Look Adorable, Here's your {num} UwU points!", color=ctx.author.color)
            userdb.addaction(ctx.author.id, "cuddle", "given")
            userdb.addaction(m.id, "cuddle", "received")
            given = userdb.showaction(ctx.author.id, "cuddle", "given")
            received = userdb.showaction(ctx.author.id, "cuddle", "received")
            emb.set_footer(text=f"{ctx.author.name} gave others {given} cuddles and received {received} cuddles")
            emb.set_image(url=return_gif("cuddle"))
            return await ctx.send(embed=emb)
        if m == None:
            await ctx.reply("Please `mention` someone to cuddle!")
        else:
            emb = discord.Embed(description=f"{ctx.author.mention} cuddles {m.mention} ~ kyaaa!", color=0xf72585)
            userdb.addaction(ctx.author.id, "cuddle", "given")
            userdb.addaction(m.id, "cuddle", "received")
            given = userdb.showaction(ctx.author.id, "cuddle", "given")
            received = userdb.showaction(ctx.author.id, "cuddle", "received")
            emb.set_footer(text=f"{ctx.author.name} gave others {given} cuddles and received {received} cuddles")
            emb.set_image(url=return_gif("cuddle"))
            await ctx.send(embed=emb)
    
    @commands.command(name=f"slap",aliases=[],usage="`< user >`",description="Slap a User.")
    async def slap(self, ctx, m: discord.Member = None):
        if m == None:
            m = ctx.author
        else:
            emb = discord.Embed(description=f"{ctx.author.mention} slaps {m.mention} ~ baakaah", color=0xf72585)
            userdb.addaction(ctx.author.id, "slap", "given")
            userdb.addaction(m.id, "slap", "received")
            given = userdb.showaction(ctx.author.id, "slap", "given")
            received = userdb.showaction(ctx.author.id, "slap", "received")
            emb.set_footer(text=f"{ctx.author.name} gave others {given} slaps and received {received} slaps")
            emb.set_image(url=return_gif("slap"))
            await ctx.send(embed=emb)
    
    @commands.command(name=f"pout",aliases=[],usage="`< user >`",description="Pout at a User.")
    async def pout(self, ctx, m: discord.Member = None):
        if m == None:
            m = ctx.author
        emb = discord.Embed(description=f"{ctx.author.mention} pouts at {m.mention} ~ hmph", color=0xf72585)
        req = requests.get('https://shiro.gg/api/images/pout')
        rjson = json.loads(req.content)
        emb.set_image(url=rjson['url'])
        await ctx.send(embed=emb)

    @commands.command(name=f"smug",aliases=[],usage="`< user >`",description="Smug at a User.")
    async def smug(self, ctx, m: discord.Member = None):
        if m == None:
            m = ctx.author
        emb = discord.Embed(description=f"{ctx.author.mention} smugs at {m.mention} ~ blehh", color=0xf72585)
        emb.set_image(url=return_gif("smug"))
        await ctx.send(embed=emb)

    @commands.command(name=f"tickle",aliases=[],usage="`< user >`",description="Tickle a User.")
    async def tickle(self, ctx, m: discord.Member = None):
        if m == None:
            m = ctx.author
        emb = discord.Embed(description=f"{ctx.author.mention} tickles {m.mention} ~_~", color=0xf72585)
        userdb.addaction(ctx.author.id, "tickle", "given")
        userdb.addaction(m.id, "tickle", "received")
        given = userdb.showaction(ctx.author.id, "tickle", "given")
        received = userdb.showaction(ctx.author.id, "tickle", "received")
        emb.set_footer(text=f"{ctx.author.name} gave others {given} tickles and received {received} tickles")
        emb.set_image(url=return_gif("tickle"))
        await ctx.send(embed=emb)

    @commands.command(name=f"kill",aliases=[],usage="`< user >`",description="Kill a User.")
    async def kill(self, ctx, m: discord.Member = None):
        if m == None:
            await ctx.reply("Who do you want to `kill`?")
        else:
            emb = discord.Embed(description=f"{ctx.author.mention} kills {m.mention} ~ RIP", color=0xf72585)
            userdb.addaction(ctx.author.id, "kill", "given")
            userdb.addaction(m.id, "kill", "received")
            given = userdb.showaction(ctx.author.id, "kill", "given")
            received = userdb.showaction(ctx.author.id, "kill", "received")
            emb.set_footer(text=f"{ctx.author.name} gave others {given} kills and received {received} kills")
            emb.set_image(url=return_gif("kill"))
            await ctx.send(embed=emb)

    @commands.command(name=f"bonk",aliases=[],usage="`< user >`",description="Bonk a User.")
    async def bonk(self, ctx, m: discord.Member = None):
        if m == None:
            m = ctx.author
        emb = discord.Embed(description=f"{ctx.author.mention} bonks {m.mention} ~ >.<", color=0xf72585)
        userdb.addaction(ctx.author.id, "bonk", "given")
        userdb.addaction(m.id, "bonk", "received")
        given = userdb.showaction(ctx.author.id, "bonk", "given")
        received = userdb.showaction(ctx.author.id, "bonk", "received")
        emb.set_footer(text=f"{ctx.author.name} gave others {given} bonks and received {received} bonks")
        emb.set_image(url=return_gif("bonk"))
        await ctx.send(embed=emb)

    @commands.command(name=f"highfive",aliases=[],usage="`< user >`",description="Give a User Highfive.")
    async def highfive(self, ctx, m: discord.Member = None):
        if m == None:
            m = ctx.author
        emb = discord.Embed(description=f"{ctx.author.mention} high fives {m.mention} ~ yoshh!", color=0xf72585)
        emb.set_image(url=return_gif('highfive'))
        await ctx.send(embed=emb)

    @commands.command(name=f"nom",aliases=[],usage="`< user >`",description="Ur Mom Nom Nom")
    async def nom(self, ctx, m: discord.Member = None):
        if m == None:
            m = ctx.author
        emb = discord.Embed(description=f"{ctx.author.mention} noms {m.mention} ~ nyaa!", color=0xf72585)
        req = requests.get('https://shiro.gg/api/images/nom')
        rjson = json.loads(req.content)
        emb.set_image(url=rjson['url'])
        await ctx.send(embed=emb)

    @commands.command(name=f"pokes",usage="`< user >`",description="Poke a User.",aliases=['boop'])
    async def pokes(self, ctx, m: discord.Member = None):
        if m == None:
            m = ctx.author
        emb = discord.Embed(description=f"{ctx.author.mention} pokes {m.mention} ~ OwO", color=0xf72585)
        req = requests.get('https://shiro.gg/api/images/poke')
        rjson = json.loads(req.content)
        userdb.addaction(ctx.author.id, "poke", "given")
        userdb.addaction(m.id, "poke", "received")
        given = userdb.showaction(ctx.author.id, "poke", "given")
        received = userdb.showaction(ctx.author.id, "poke", "received")
        emb.set_footer(text=f"{ctx.author.name} gave others {given} pokes and received {received} pokes")
        emb.set_image(url=rjson['url'])
        await ctx.send(embed=emb)

    @commands.command(name=f"blush",aliases=[],usage="`< user >`",description="Blush :flushed:.")
    async def blush(self, ctx, m: discord.Member = None):
        if m == None:
            m = ctx.author
        emb = discord.Embed(description=f"{ctx.author.mention} blushes at {m.mention} ~ >.<", color=0xf72585)

        emb.set_image(url=return_gif("blush"))
        await ctx.send(embed=emb)

    @commands.command(aliases=["hold"],name=f"",usage="`< user >`",description="Handhold a User.")
    async def handhold(self, ctx, m: discord.Member = None):
        if m == None:
            m = ctx.author
        emb = discord.Embed(description=f"{ctx.author.mention} holds {m.mention}'s hands ~ cutee", color=0xf72585)
        userdb.addaction(ctx.author.id, "handhold", "given")
        userdb.addaction(m.id, "handhold", "received")
        given = userdb.showaction(ctx.author.id, "handhold", "given")
        received = userdb.showaction(ctx.author.id, "handhold", "received")
        emb.set_footer(text=f"{ctx.author.name} gave others {given} handholds and received {received} handholds")
        emb.set_image(url=return_gif("handhold"))
        await ctx.send(embed=emb)

    @commands.command(name=f"feed",aliases=[],usage="`< user >`",description="Feed a User.")
    async def feed(self, ctx, m: discord.Member = None):
        if m == None:
            m = ctx.author
        emb = discord.Embed(description=f"{ctx.author.mention} feeds {m.mention} ~ uwu", color=0xf72585)
        emb.set_image(url=return_gif("feed"))
        await ctx.send(embed=emb)

    @commands.command(name=f"cringe",aliases=[],usage="`< user >`",description="EE Cringe.")
    async def cringe(self, ctx):

        emb = discord.Embed(description=f"{ctx.author.mention} cringes!", color=0xf72585)
        emb.set_image(url=return_gif("cringe"))
        await ctx.send(embed=emb)

    @commands.command(name=f"wink",aliases=[],usage="`< user >`",description="Wink at a User.")
    async def wink(self, ctx, m: discord.Member = None):
        if m == None:
            m = ctx.author
        emb = discord.Embed(description=f"{ctx.author.mention} winks at {m.mention} ~ uwu", color=0xf72585)
        emb.set_image(url=return_gif("wink"))
        await ctx.send(embed=emb)

def setup(bot):
    bot.add_cog(Actions(bot))