import discord
from discord.ext import commands
import PIL
from io import BytesIO
import imageio
import requests
import weeby
from dotenv import load_dotenv
import os
import numpy as np
import datetime
from petpetgif import petpet 
import random
from typing import Union, Optional
import aiohttp
import json

load_dotenv()
WEEBY_API_KEY = os.environ.get("WEEBY_API_KEY")
my_weeby = weeby.Weeby(WEEBY_API_KEY)

class Meme(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.emoji = "꒰ <:MemeCategory:943427907877994507> ꒱"
        self.hidden = False
        self.description = "Includes Meme Related Commands."



    @commands.command(usage=f"`< user >`", description=f"Simp Overlay")
    async def simp(self, ctx, m1:discord.Member=None):
        '''Simp Overlay'''
        if m1 is None:
            m1=ctx.author
        image = my_weeby.set_overlay().overlay(image_url=m1.avatar.url, type="simp")
        im = PIL.Image.open(BytesIO(image))
        im.save("generated.png")
        file = discord.File(f"generated.png", filename="pic.jpg")
        emb = discord.Embed(title="", description=f"", color=0xe91e63)
        emb.set_image(url="attachment://pic.jpg")
        await ctx.send(file=file, embed=emb)

    @commands.command(description=f"Ship Two User.", usage=f"`< user1 >` `< user2 >`")
    async def ship(self, ctx, m1:discord.Member=None, m2:discord.Member=None):
        if m1 == None or m2 == None:
            return
        image = my_weeby.generate().two_image(type="ship", url1=m1.avatar.url, url2=m2.avatar.url)
        im = PIL.Image.open(BytesIO(image))
        im.save("generated.png")
        file = discord.File(f"generated.png", filename="pic.jpg")
        emb = discord.Embed(title="", description=f"", color=0xe91e63)
        emb.set_image(url="attachment://pic.jpg")
        await ctx.send(file=file, embed=emb)

    @commands.command(aliases=['amongus'], usage=f"`< user1 >` `< user2 >`", description=f"Among US Meme.")
    async def amogus(self, ctx, m1:discord.Member=None, m2:discord.Member=None):
        '''Among US Meme.'''
        if m1 == None or m2 == None:
            return
        image = my_weeby.generate().two_image(type="amogus", url1=m1.avatar.url, url2=m2.avatar.url)
        im = PIL.Image.open(BytesIO(image))
        im.save("generated.png")
        file = discord.File(f"generated.png", filename="pic.jpg")
        emb = discord.Embed(title="", description=f"", color=0xe91e63)
        emb.set_image(url="attachment://pic.jpg")
        await ctx.send(file=file, embed=emb)

    # @commands.command()
    # async def jojoshock(self, ctx, m1:discord.Member=None):
    #     '''Jojo Meme'''
    #     if m1 == None :
    #         m1=ctx.author
    #     image = my_weeby.generate().one_image(type="jojoshock", url=m1.avatar.url)
    #     im = PIL.Image.open(BytesIO(image))
    #     im.save("generated.png")
    #     file = discord.File(f"generated.png", filename="pic.jpg")
    #     emb = discord.Embed(title="", description=f"", color=0xe91e63)
    #     emb.set_image(url="attachment://pic.jpg")
    #     await ctx.send(file=file, embed=emb)

    @commands.command(usage=f"`< user >`", description=f"Eject a User to find whether he is SUSSY BAKA.")
    async def eject(self, ctx, m1:discord.Member=None):
        '''Eject a User to find whether he is SUSSY BAKA.'''
        if m1 == None :
            m1=ctx.author
        outcome = random.choice(["imposter", "crewmate"])
        image = my_weeby.generate().eject(url=m1.avatar.url, text=m1.name, outcome=outcome)
        im = PIL.Image.open(BytesIO(image))
        im.save("generated.gif")
        file = discord.File(f"generated.gif", filename="pic.gif")
        emb = discord.Embed(title="", description=f"", color=0xe91e63)
        emb.set_image(url="attachment://pic.gif")
        await ctx.send(file=file, embed=emb)

    @commands.command(usage=f"`< user >`", description=f"Pet Pet Generator.")
    async def petpet(self, ctx, m1:discord.Member=None):
        '''Pet Pet Generator.'''
        if m1 == None :
            m1=ctx.author
        asset = m1.avatar.with_size(512)
        await asset.save('av.png')
        dest = BytesIO()
        petpet.make('av.png', dest)
        dest.seek(0)
        file = discord.File(dest, filename="pat.gif")
        emb = discord.Embed(description=f"`{m1.name.lower()}_pat`",color=0x2e69f2)
        emb.set_image(url="attachment://pat.gif")
        await ctx.send(embed=emb, file=file)

    @commands.command(usage="`< user >`", description=f"AWW! U ARE TRIGGERED?")
    async def triggered(self, ctx, member: discord.Member=None):
        '''AWW! U ARE TRIGGERED?'''
        member = member or ctx.author
        await ctx.trigger_typing()
        async with aiohttp.ClientSession() as session:
            async with session.get(f'https://some-random-api.ml/canvas/triggered?avatar={member.avatar.with_format("png").url}') as af:
                if 300 > af.status >= 200:
                    fp = BytesIO(await af.read())
                    file = discord.File(fp, "triggered.gif")
                    em = discord.Embed(
                        color=0xf1f1f1,
                    )
                    em.set_image(url="attachment://triggered.gif")
                    await ctx.send(embed=em, file=file)
                else:
                    return
                await session.close()

    @commands.command(usage="`< user >`", description=f"Horny license just for u!")
    async def horny(self,ctx, member: discord.Member = None):
        '''Horny license just for u!'''
        member = member or ctx.author
        await ctx.trigger_typing()
        async with aiohttp.ClientSession() as session:
            async with session.get(f'https://some-random-api.ml/canvas/horny?avatar={member.avatar.with_format("png").url}') as af:
                if 300 > af.status >= 200:
                    fp = BytesIO(await af.read())
                    file = discord.File(fp, "horny.png")
                    em = discord.Embed(
                        color=0xf1f1f1,
                    )
                    em.set_image(url="attachment://horny.png")
                    await ctx.send(embed=em, file=file)
                else:
                    await ctx.send('No horny :(')
                await session.close()

    @commands.command(usage="`< user >`", description=f"You are Gae Bro!")
    async def gaycard(self, ctx, member: discord.Member=None):
        '''You are Gae Bro!'''
        member = member or ctx.author
        await ctx.trigger_typing()
        async with aiohttp.ClientSession() as session:
            async with session.get(f'https://some-random-api.ml/canvas/gay?avatar={member.avatar.with_format("png").url}') as af:
                if 300 > af.status >= 200:
                    fp = BytesIO(await af.read())
                    file = discord.File(fp, "gay.gif")
                    em = discord.Embed(
                        color=0xf1f1f1,
                    )
                    em.set_image(url="attachment://gay.gif")
                    await ctx.send(embed=em, file=file)
                else:
                    return
                await session.close()

    @commands.command(usage="`< user >`", description=f"Hands Up!'")
    async def wasted(self, ctx, member: discord.Member=None):
        '''Hands Up!'''
        member = member or ctx.author
        await ctx.trigger_typing()
        async with aiohttp.ClientSession() as session:
            async with session.get(f'https://some-random-api.ml/canvas/wasted?avatar={member.avatar.with_format("png").url}') as af:
                if 300 > af.status >= 200:
                    fp = BytesIO(await af.read())
                    file = discord.File(fp, "wasted.gif")
                    em = discord.Embed(
                        
                        color=0xf1f1f1,
                    )
                    em.set_image(url="attachment://wasted.gif")
                    await ctx.send(embed=em, file=file)
                else:
                    return
                await session.close()

    @commands.command(usage="`< user >`", description=f"Mission Passed")
    async def mission(self, ctx, member: discord.Member=None):
        '''Mission Passed'''
        member = member or ctx.author
        await ctx.trigger_typing()
        async with aiohttp.ClientSession() as session:
            async with session.get(f'https://some-random-api.ml/canvas/mission?avatar={member.avatar.with_format("png").url}') as af:
                if 300 > af.status >= 200:
                    fp = BytesIO(await af.read())
                    file = discord.File(fp, "mission.gif")
                    em = discord.Embed(
                        
                        color=0xf1f1f1,
                    )
                    em.set_image(url="attachment://mission.gif")
                    await ctx.send(embed=em, file=file)
                else:
                    return
                await session.close()

    @commands.command(usage="`< user >`", description=f"Take me to Jail.")
    async def jail(self, ctx, member: discord.Member=None):
        '''Take me to Jail.'''
        member = member or ctx.author
        await ctx.trigger_typing()
        async with aiohttp.ClientSession() as session:
            async with session.get(f'https://some-random-api.ml/canvas/jail?avatar={member.avatar.with_format("png").url}') as af:
                if 300 > af.status >= 200:
                    fp = BytesIO(await af.read())
                    file = discord.File(fp, "jail.gif")
                    em = discord.Embed(
                        
                        color=0xf1f1f1,
                    )
                    em.set_image(url="attachment://jail.gif")
                    await ctx.send(embed=em, file=file)
                else:
                    return
                await session.close()

    @commands.command(aliases=["communist"],usage="`< user >`", description=f"OUR COMMAND!")
    async def comrade(self, ctx, member: discord.Member=None):
        '''OUR COMMAND!'''
        member = member or ctx.author
        await ctx.trigger_typing()
        async with aiohttp.ClientSession() as session:
            async with session.get(f'https://some-random-api.ml/canvas/comrade?avatar={member.avatar.with_format("png").url}') as af:
                if 300 > af.status >= 200:
                    fp = BytesIO(await af.read())
                    file = discord.File(fp, "comrade.gif")
                    em = discord.Embed(
                        
                        color=0xf1f1f1,
                    )
                    em.set_image(url="attachment://comrade.gif")
                    await ctx.send(embed=em, file=file)
                else:
                    return
                await session.close()
        
    @commands.command(usage="`< user >`", description=f"Simpcard just for u")
    async def simpcard(self,ctx, member: discord.Member = None):
        '''Simpcard just for u'''
        member = member or ctx.author
        await ctx.trigger_typing()
        async with aiohttp.ClientSession() as session:
            async with session.get(f'https://some-random-api.ml/canvas/simpcard?avatar={member.avatar.with_format("png").url}') as af:
                if 300 > af.status >= 200:
                    fp = BytesIO(await af.read())
                    file = discord.File(fp, "simpcard.png")
                    em = discord.Embed(
                        
                        color=0xf1f1f1,
                    )
                    em.set_image(url="attachment://simpcard.png")
                    await ctx.send(embed=em, file=file)
                else:
                    print(af.status)
                    await ctx.send('No simping :(')
                await session.close()

    @commands.command(usage="`< user >`", description=f"TRY THIS.")
    async def lolice(self,ctx, member: discord.Member = None):
        '''TRY THIS.'''
        member = member or ctx.author
        await ctx.trigger_typing()
        async with aiohttp.ClientSession() as session:
            async with session.get(f'https://some-random-api.ml/canvas/lolice?avatar={member.avatar.with_format("png").url}') as af:
                if 300 > af.status >= 200:
                    fp = BytesIO(await af.read())
                    file = discord.File(fp, "lolice.png")
                    em = discord.Embed(
                        
                        color=0xf1f1f1,
                    )
                    em.set_image(url="attachment://lolice.png")
                    await ctx.send(embed=em, file=file)
                else:
                    await ctx.send('No simping :(')
                await session.close()



def setup(bot):
    bot.add_cog(Meme(bot))