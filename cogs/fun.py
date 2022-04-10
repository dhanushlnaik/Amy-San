import discord
from discord.ext import commands
import datetime
import time
from random import choice , randint
from asyncio import TimeoutError
from aiohttp import ClientSession
from imgurpython import ImgurClient
import giphy_client
from giphy_client.rest import ApiException
import praw
from tools import *
import urbandict
from typing import List
from discord.ext import commands
import discord
from dotenv import load_dotenv
from tools import last_replace , text_to_owo
from akinator.async_aki import Akinator
import akinator
import asyncio


load_dotenv()
REDDIT_APP_ID = os.environ.get("REDDIT_APP_ID")
REDDIT_APP_SECRET = os.environ.get("REDDIT_APP_SECRET")
REDDIT_ENABLED_MEME_SUBREDDITS = [
    'funny',
    'memes'
]
REDDIT_ENABLED_NSFW_SUBREDDITS = [
    'wtf'
]

def user_is_me(ctx):
    return ctx.message.author.id == 624174437821972480


async def notify_user(member, message):
    if member is not None:
        channel = member.dm_channel
        if channel is None:
            channel = await member.create_dm()
        await channel.send(message)

tenor_key = os.environ.get("TENOR_KEY")
api_key = os.environ.get("API_KEY")
imgur = ImgurClient(os.environ.get("IMGUR"),os.environ.get("IMGUR_KEY"))

async def get(session: object, url: object) -> object:
        async with session.get(url) as response:
            return await response.text()


rpsC = ["Rock", "Paper", "Scissors"]
melon = discord.Color.from_rgb(248,131,121)
response_list = ["As I see it, yes", "Yes", "No", "Very likely", "Not even close", "Maybe", "Very unlikely", "Gino's mom told me yes", "Gino's mom told me no", "Ask again later", "Better not tell you now", "Concentrate and ask again", "Don't count on it", " It is certain", "My sources say no", "Outlook good", "You may rely on it", "Very Doubtful", "Without a doubt"]

class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.reddit = None
        self.emoji = "꒰ <:FunCategory:943427905931857961> ꒱"
        self.hidden = False
        self.description = "Includes Fun Related Commands."
        if REDDIT_APP_ID and REDDIT_APP_SECRET:
            self.reddit = praw.Reddit(client_id=REDDIT_APP_ID, client_secret=REDDIT_APP_SECRET,
                                      user_agent="ULTIMATE_DISCORD_BOT:%s:1.0" % REDDIT_APP_ID)



    @commands.command(aliases=["shipping"], brief="Ship two users.",usage="`<user1>` `<user2>`",help="Ship two users.", extras={"emoji": "💟"},description="Ship two users.")
    @commands.cooldown(rate=1, per=5, type=commands.BucketType.default)
    async def shiprate(self, ctx, name1 : commands.clean_content, name2 : commands.clean_content):

        shipnumber = randint(0,100)
        if 0 <= shipnumber <= 10:
            status = "Really low! {}".format(choice(["Friendzone ;(", 
                                                            'Just "friends"', 
                                                            '"Friends"', 
                                                            "Little to no love ;(", 
                                                            "There's barely any love ;("]))
        elif 10 < shipnumber <= 20:
            status = "Low! {}".format(choice(["Still in the friendzone", 
                                                     "Still in that friendzone ;(", 
                                                     "There's not a lot of love there... ;("]))
        elif 20 < shipnumber <= 30:
            status = "Poor! {}".format(choice(["But there's a small sense of romance from one person!", 
                                                     "But there's a small bit of love somewhere", 
                                                     "I sense a small bit of love!", 
                                                     "But someone has a bit of love for someone..."]))
        elif 30 < shipnumber <= 40:
            status = "Fair! {}".format(choice(["There's a bit of love there!", 
                                                      "There is a bit of love there...", 
                                                      "A small bit of love is in the air..."]))
        elif 40 < shipnumber <= 60:
            status = "Moderate! {}".format(choice(["But it's very one-sided OwO", 
                                                          "It appears one sided!", 
                                                          "There's some potential!", 
                                                          "I sense a bit of potential!", 
                                                          "There's a bit of romance going on here!", 
                                                          "I feel like there's some romance progressing!", 
                                                          "The love is getting there..."]))
        elif 60 < shipnumber <= 70:
            status = "Good! {}".format(choice(["I feel the romance progressing!", 
                                                      "There's some love in the air!", 
                                                      "I'm starting to feel some love!"]))
        elif 70 < shipnumber <= 80:
            status = "Great! {}".format(choice(["There is definitely love somewhere!", 
                                                       "I can see the love is there! Somewhere...", 
                                                       "I definitely can see that love is in the air"]))
        elif 80 < shipnumber <= 90:
            status = "Over average! {}".format(choice(["Love is in the air!", 
                                                              "I can definitely feel the love", 
                                                              "I feel the love! There's a sign of a match!", 
                                                              "There's a sign of a match!", 
                                                              "I sense a match!", 
                                                              "A few things can be imporved to make this a match made in heaven!"]))
        elif 90 < shipnumber <= 100:
            status = "True love! {}".format(choice(["It's a match!", 
                                                           "There's a match made in heaven!", 
                                                           "It's definitely a match!", 
                                                           "Love is truely in the air!", 
                                                           "Love is most definitely in the air!"]))

        if shipnumber <= 33:
            shipColor = 0xE80303
        elif 33 < shipnumber < 66:
            shipColor = 0xff6600
        else:
            shipColor = 0x3be801

        emb = (discord.Embed(color=shipColor, \
                             title="Love test for:", \
                             description="**{0}** and **{1}** {2}".format(name1, name2, choice([
                                                                                                        ":sparkling_heart:", 
                                                                                                        ":heart_decoration:", 
                                                                                                        ":heart_exclamation:", 
                                                                                                        ":heartbeat:", 
                                                                                                        ":heartpulse:", 
                                                                                                        ":hearts:", 
                                                                                                        ":blue_heart:", 
                                                                                                        ":green_heart:", 
                                                                                                        ":purple_heart:", 
                                                                                                        ":revolving_hearts:", 
                                                                                                        ":yellow_heart:", 
                                                                                                        ":two_hearts:"]))))
        emb.add_field(name="Results:", value=f"{shipnumber}%", inline=True)
        emb.add_field(name="Status:", value=(status), inline=False)
        emb.set_author(name="Shipping", icon_url="http://moziru.com/images/kopel-clipart-heart-6.png")
        await ctx.send(embed=emb)
        
    @commands.command(aliases=["8ball", "tellme", "isittrue"], brief="Extra generic 8ball Game. ",usage="`<question>`",name="eightball",help="Extra generic 8ball Game. ", extras={"emoji": "🎱"},description="Extra generic 8ball Game. ")
    @commands.cooldown(rate=1, per=5, type=commands.BucketType.default)
    async def eightball(self, ctx, *, _ballInput: commands.clean_content):

        choiceType = choice(["(Affirmative)", "(Non-committal)", "(Negative)"])
        if choiceType == "(Affirmative)":
            prediction = choice(["It is certain ", 
                                        "It is decidedly so ", 
                                        "Without a doubt ", 
                                        "Yes, definitely ", 
                                        "You may rely on it ", 
                                        "As I see it, yes ",
                                        "Most likely ", 
                                        "Outlook good ", 
                                        "Yes ", 
                                        "Signs point to yes "]) + ":8ball:"

            emb = (discord.Embed(title="Question: {}".format(_ballInput), colour=0x3be801, description=prediction))
        elif choiceType == "(Non-committal)":
            prediction = choice(["Reply hazy try again ", 
                                        "Ask again later ", 
                                        "Better not tell you now ", 
                                        "Cannot predict now ", 
                                        "Concentrate and ask again "]) + ":8ball:"
            emb = (discord.Embed(title="Question: {}".format(_ballInput), colour=0xff6600, description=prediction))
        elif choiceType == "(Negative)":
            prediction = choice(["Don't count on it ", 
                                        "My reply is no ", 
                                        "My sources say no ", 
                                        "Outlook not so good ", 
                                        "Very doubtful "]) + ":8ball:"
            emb = (discord.Embed(title="Question: {}".format(_ballInput), colour=0xE80303, description=prediction))
        emb.set_author(name='Magic 8 ball', icon_url='https://www.horoscope.com/images-US/games/game-magic-8-ball-no-text.png')
        await ctx.send(embed=emb)


    @commands.command(aliases=[ "gayscanner"], brief="A Gay Scanner.",usage="`< user >`",name="gay",help="A Gay Scanner.", extras={"emoji": "🌈"},description="A Gay Scanner.")
    @commands.cooldown(rate=1, per=5, type=commands.BucketType.default)
    async def gay_scanner(self, ctx,* ,user: commands.clean_content=None):

        if not user:
            user = ctx.author.name
        gayness = randint(0,100)
        if gayness <= 33:
            gayStatus = choice(["No homo", 
                                       "Wearing socks", 
                                       '"Only sometimes"', 
                                       "Straight-ish", 
                                       "No homo bro", 
                                       "Girl-kisser", 
                                       "Hella straight"])
            gayColor = 0xFFC0CB
        elif 33 < gayness < 66:
            gayStatus = choice(["Possible homo", 
                                       "My gay-sensor is picking something up", 
                                       "I can't tell if the socks are on or off", 
                                       "Gay-ish", 
                                       "Looking a bit homo", 
                                       "lol half  g a y", 
                                       "safely in between for now"])
            gayColor = 0xFF69B4
        else:
            gayStatus = choice(["LOL YOU GAY XDDD FUNNY", 
                                       "HOMO ALERT", 
                                       "MY GAY-SENSOR IS OFF THE CHARTS", 
                                       "STINKY GAY", 
                                       "BIG GEAY", 
                                       "THE SOCKS ARE OFF", 
                                       "HELLA GAY"])
            gayColor = 0xFF00FF
        emb = discord.Embed(description=f"Gayness for **{user}**", color=gayColor)
        emb.add_field(name="Gayness:", value=f"{gayness}% gay")
        emb.add_field(name="Comment:", value=f"{gayStatus} :kiss_mm:")
        emb.set_author(name="Gay-Scanner™", icon_url="https://upload.wikimedia.org/wikipedia/commons/thumb/a/a4/ICA_flag.svg/2000px-ICA_flag.svg.png")
        await ctx.send(embed=emb)

    @commands.command(aliases=["reddit", "subrettit", "rslash", "r"], brief="Random Post from desired Subreddit.",usage="`< redditname >`",name="random",help="Random Post from desired Subreddit.", extras={"emoji": "😂"},description="Random Post from desired Subreddit.")
    @commands.cooldown(rate=1, per=5, type=commands.BucketType.default)
    async def random(self, ctx, subreddit: str="cat"):

        async with ctx.channel.typing():
            if self.reddit:
                allsubs = []
                submissions = self.reddit.subreddit(subreddit)
                top = submissions.top(limit=50)
                for subm in top:
                    allsubs.append(subm)

                randomsub = choice(allsubs)

                while True:
                    name = randomsub.title
                    url = randomsub.url
                    if url.endswith("jpg") or url.endswith("png"):
                        break
                    else:
                        randomsub = choice(allsubs)
                em = discord.Embed(title=name, color=discord.Color.blurple())
                em.set_image(url=url)
                await ctx.send(embed=em)
            else:
                await ctx.send("This is not working. Contact Administrator.")

    @commands.command(aliases=["mommajokes"], brief="Insults a user via Momma Joke.",usage="`< user >`",name="insult",help="Insults a user via Momma Joke.", extras={"emoji": "😹"},description="Insults a user via Momma Joke.")
    @commands.cooldown(rate=1, per=5, type=commands.BucketType.default)
    async def insult(self, ctx, member: discord.Member = None):

        insult = get_momma_jokes()
        if member is not None:
            await ctx.send("%s eat this: %s " % (member.name, insult))
        else:
            await ctx.send("%s for yourself: %s " % (ctx.message.author.name, insult))

    @commands.command(aliases= ["copy"], brief="Make me say Something.",usage="`< text >`",name="say",help="Make me say Something.", extras={"emoji": "🗣"},description="Drunkify a series of text.")
    @commands.cooldown(rate=1, per=5, type=commands.BucketType.default)
    async def say(self, ctx,*,msg):

        mes = await ctx.send(msg)
        await ctx.message.delete()



    @commands.command(aliases=["doggo", "doggies", "🐕", "doggie"], brief="Random Dog Picture and Fact.",name="dog",help="Random Dog Picture and Fact.", extras={"emoji": "🐕"},description="Random Dog Picture and Fact.")
    @commands.cooldown(rate=1, per=5, type=commands.BucketType.default)
    async def dog(self, ctx):

        async with ClientSession() as session:
            request = await session.get('https://some-random-api.ml/img/dog')
            dogjson = await request.json()
            # This time we'll get the fact request as well!
            request2 = await session.get('https://some-random-api.ml/facts/dog')
            factjson = await request2.json()

        embed = discord.Embed(title="Doggo!", color=discord.Color.purple(), description=factjson['fact'])
        embed.set_image(url=dogjson['link'])
        await ctx.send(embed=embed)

    @commands.command(aliases=["catto", "cattie", "🐈"], brief="Random Cat Picture and Fact.",name="cat",help="Random Cat Picture and Fact.", extras={"emoji": "😾"},description="Random Cat Picture and Fact.")
    @commands.cooldown(rate=1, per=5, type=commands.BucketType.default)
    async def cat(self, ctx):

        async with ClientSession() as session:
            request = await session.get('https://some-random-api.ml/img/cat')
            dogjson = await request.json()
            # This time we'll get the fact request as well!
            request2 = await session.get('https://some-random-api.ml/facts/cat')
            factjson = await request2.json()

        embed = discord.Embed(title="Cat", color=discord.Color.purple(), description=factjson['fact'])
        embed.set_image(url=dogjson['link'])
        await ctx.send(embed=embed)


    @commands.command(aliases=["img", "image","picture"], brief="Search for an Image from ImageUr.",usage="`< search result >`",name="imgur",help="Search for an Image from ImageUr.", extras={"emoji": "🖼"},description="Search for an Image from ImageUr.")
    @commands.cooldown(rate=1, per=5, type=commands.BucketType.default)
    async def imgur(self, ctx, *text: str):

        rand = randint(0, 29)
        if text == ():
            await ctx.send('**Please enter a search term**')
        elif text[0] != ():
            items = imgur.gallery_search(" ".join(text[0:len(text)]), advanced=None, sort='viral', window='all',page=0)
            await ctx.send(items[rand].link)

    @commands.command(aliases=[], brief="Search for a Gif from Giphy.",usage="`< search result >`",name="giphy",help="Search for a Gif from Giphy.", extras={"emoji": "📹"},description="Search for a Gif from Giphy.")
    @commands.cooldown(rate=1, per=5, type=commands.BucketType.default)    
    async def gif(self, ctx,*,q="Anime"):

        api_instance = giphy_client.DefaultApi()

        try:
            api_response = api_instance.gifs_search_get(api_key, q, limit=5, rating='g')
            lst = list(api_response.data)
            rgiff = choice(lst)
            emb = discord.Embed(color=ctx.author.color)
            emb.set_author(name=q.title(),icon_url=ctx.author.avatar.url)
            emb.set_image(url=f"https://media.giphy.com/media/{rgiff.id}/giphy.gif")
            await ctx.channel.send(embed=emb)
        except ApiException as e:
            print("Exception when calling Api as "+e)

    @commands.command(aliases=[], brief="Poke a User.",usage="`< user >`",name="poke",help="Poke a User.", extras={"emoji": "💢"},description="Poke a User.")
    @commands.cooldown(rate=1, per=5, type=commands.BucketType.default)
    async def poke(self, ctx, member: discord.Member = None):

        try:
            if member is not None:
                message = "%s poked you!!!!" % ctx.author.name
                await notify_user(member, message)
                await ctx.message.delete()
            else:
                await ctx.send("Please use @mention to poke someone.")
        except:
            message = "%s poked you!!!!" % ctx.author.name
            await ctx.send(f"{member.mention},{message}/n ||Cant Dm them||")
            
    @commands.command(aliases=[], brief="Owoify Text.",usage="`< text >`",name="owo",help="Owoify Text.", extras={"emoji": "😳"},description="Owoify Text.")
    @commands.cooldown(rate=1, per=5, type=commands.BucketType.default)
    async def owo(self, ctx):

        await ctx.send(text_to_owo(ctx.message.content))

    @commands.command(aliases=["d", "dre"], brief="Get a random Dare.",usage="`< user >`",name="dare",help="Get a random Dare.", extras={"emoji": "🎯"},description="Drunkify a series of text.")
    @commands.cooldown(rate=1, per=5, type=commands.BucketType.default)
    async def dare(self,ctx,*,msg=None):

        dareRand = get_dare()
        emb = discord.Embed(color = melon)
        emb.set_author(name=f"DARE : {dareRand}", icon_url=ctx.author.avatar.url)
        await ctx.send(embed=emb)

    @commands.command(aliases=["t", "true", "tru"], brief="Get a random Truth Question.",usage="`< user >`",name="truth",help="Get a random Truth Question.", extras={"emoji": "😬"},description="Get a random Truth Question.")
    @commands.cooldown(rate=1, per=5, type=commands.BucketType.default)
    async def truth(self,ctx,*,msg=None):

        truthRand = get_truth()
        emb = discord.Embed(color = melon)
        emb.set_author(name=f"TRUTH : {truthRand}", icon_url=ctx.author.avatar.url)
        await ctx.send(embed=emb)

    @commands.command(aliases=["wouldyou", "wouldyourather"],  brief="Get a random Would You Rather Question.",usage="``< user >``",name="wyr",help="Get a random Would You Rather Question.", extras={"emoji": "🙄"},description="Get a random Truth Question.")
    @commands.cooldown(rate=1, per=5, type=commands.BucketType.default)
    async def wyr(self,ctx,*,msg=None):

        wyrRand = get_wyr()
        emb = discord.Embed(color = melon)
        emb.set_author(name=f"{wyrRand}", icon_url=ctx.author.avatar.url)
        await ctx.send(embed=emb)

    @commands.command(aliases=["neverhaveiever"], brief="Get a random Never Have I Ever Question.",usage="``< user >``",name="nhie",help="Get a random Never Have I Ever Question.", extras={"emoji": "😏"},description="Get a random Never Have I Ever Question.")
    @commands.cooldown(rate=1, per=5, type=commands.BucketType.default)
    async def nhie(self,ctx,*,msg=None):

        nhieRand = get_nhie()
        emb = discord.Embed(color = melon)
        emb.set_author(name=f"{nhieRand}", icon_url=ctx.author.avatar.url)
        await ctx.send(embed=emb)

    @commands.command(aliases=["urbandict", "dict"], brief="Check Something in Urban Dictionary.",usage="`< text >`",name="df",help="Check Something in Urban Dictionary.", extras={"emoji": "📚"},description="Check Something in Urban Dictionary.")
    @commands.cooldown(rate=1, per=5, type=commands.BucketType.default)
    async def urban(self,ctx,*,define):

        term = urbandict.define(define)
        print(term)
        ex = term[0]['example']
        meaning = term[0]['def']
        embed = discord.Embed(title=f"{define.title()}",description=f"Meaning : {meaning}\n {term[1]['def']}",color=melon)
        embed.add_field(name="Example:", value=f"{ex}\n{term[1]['example']}")
        embed.timestamp = datetime.datetime.utcnow()
        await ctx.send(embed=embed)



def setup(bot):
    bot.add_cog(Fun(bot))