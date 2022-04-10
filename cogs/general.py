import discord
from discord.ext import commands
import requests
import json
from dotenv import load_dotenv
import os
from database import afk
from os import name
from disputils import BotEmbedPaginator
import PIL
from io import BytesIO
import imageio
import requests
from dotenv import load_dotenv
import os
import numpy as np
import datetime
import json
import discord



load_dotenv()
API_KEY = os.environ.get("WEEBY_API_KEY")


class General(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot
        self.emoji = "꒰ <:GeneralCategory:943427909752856577> ꒱"
        self.hidden = False
        self.description = "Includes General Commands."

    @commands.command(aliases=['avatar', 'pfp'], usage=f"`< user1 >` `< user2 >`", description=f"Check Avatar for Single and Shared Pfps.")
    async def av(self, ctx, m1: discord.Member = None, m2: discord.Member = None):
        '''Check Avatar for Single and Shared Pfps.'''
        #for single pfp
        if m1 == None and m2 == None:
            m1 = ctx.author
            if m1.avatar.is_animated():
                asset1 = m1.avatar.with_size(512)
                await asset1.save("avatar.gif")
                file = discord.File("avatar.gif")
                embed = discord.Embed(title="Avatar" ,color=0xe91e63,description=f"`Nickname: {m1.display_name}\nID: {m1.id}`")
                embed.set_author(name=m1, icon_url=m1.avatar.url)
                embed.timestamp = datetime.datetime.utcnow()
                embed.set_image(url="attachment://avatar.gif")

            else:
                asset1 = m1.avatar.with_size(512)
                await asset1.save("avatar.png")
                file = discord.File("avatar.png")
                embed = discord.Embed(title="Avatar" ,color=0xe91e63,description=f"`Nickname: {m1.display_name}\nID: {m1.id}`")
                embed.set_author(name=m1, icon_url=m1.avatar.url)
                embed.timestamp = datetime.datetime.utcnow()
                embed.set_image(url="attachment://avatar.png")

            await ctx.send(embed=embed, file = file)
        elif m1 != None and m2 == None:
            if m1.avatar.is_animated():
                asset1 = m1.avatar.with_size(512)
                await asset1.save("avatar.gif")
                file = discord.File("avatar.gif")
                embed = discord.Embed(title="Avatar" ,color=0xe91e63,description=f"`Nickname: {m1.display_name}\nID: {m1.id}`")
                embed.set_author(name=m1, icon_url=m1.avatar.url)
                embed.timestamp = datetime.datetime.utcnow()
                embed.set_image(url="attachment://avatar.gif")

            else:
                asset1 = m1.avatar.with_size(512)
                await asset1.save("avatar.png")
                file = discord.File("avatar.png")
                embed = discord.Embed(title="Avatar" ,color=0xe91e63,description=f"`Nickname: {m1.display_name}\nID: {m1.id}`")
                embed.set_author(name=m1, icon_url=m1.avatar.url)
                embed.timestamp = datetime.datetime.utcnow()
                embed.set_image(url="attachment://avatar.png")

            await ctx.send(embed=embed, file=file)
        elif m2 == m1:
            if m1.avatar.is_animated():
                asset1 = m1.avatar.with_size(512)
                await asset1.save("avatar.gif")
                file = discord.File("avatar.gif")
                embed = discord.Embed(title="Avatar" ,color=0xe91e63,description=f"`Nickname: {m1.display_name}\nID: {m1.id}`")
                embed.set_author(name=m1, icon_url=m1.avatar.url)
                embed.timestamp = datetime.datetime.utcnow()
                embed.set_image(url="attachment://avatar.gif")

            else:
                asset1 = m1.avatar.with_size(512)
                await asset1.save("avatar.png")
                file = discord.File("avatar.png")
                embed = discord.Embed(title="Avatar" ,color=0xe91e63,description=f"`Nickname: {m1.display_name}\nID: {m1.id}`")
                embed.set_author(name=m1, icon_url=m1.avatar.url)
                embed.timestamp = datetime.datetime.utcnow()
                embed.set_image(url="attachment://avatar.png")

            await ctx.send(embed=embed, file=file)

        #for shared pfp
        elif m2 != m1:
            bg = PIL.Image.open("./images/img.png")
            asset1 = m1.avatar.with_size(512)
            asset2 = m2.avatar.with_size(512)
            data1 = BytesIO(await asset1.read())
            data2 = BytesIO(await asset2.read())
            pfp1 = PIL.Image.open(data1)
            pfp2 = PIL.Image.open(data2)
            pfp1 = pfp1.resize((500, 500))
            pfp2 = pfp2.resize((500, 500))

            bg.paste(pfp1, (0, 0))
            bg.paste(pfp2, (500, 0))

            if m1.avatar.is_animated() and m2.avatar.is_animated():
                im1 = "pfp1.gif"
                im2 = "pfp2.gif"
                await m1.avatar.save(im1)
                await m2.avatar.save(im2)
                def resize(image):
                    size = 200, 200
                    im = PIL.Image.open(image)
                    frames = PIL.ImageSequence.Iterator(im)
                    def thumbnails(frames):
                        for frame in frames:
                            thumbnail = frame.copy()
                            thumbnail.thumbnail(size, PIL.Image.ANTIALIAS)
                            yield thumbnail
                    frames = thumbnails(frames)
                    om = next(frames)
                    om.info = im.info
                    return om, frames
                image1, frame1 = resize(im1)
                image1.save("pp1.gif", save_all=True, append_images=list(frame1), loop=0)
                image2, frame2 = resize(im2)
                image2.save("pp2.gif", save_all=True, append_images=list(frame2), loop=0)
                av1 = imageio.get_reader("pp1.gif")
                av2 = imageio.get_reader("pp2.gif")
                all_frames = min(av1.get_length(), av2.get_length())
                new_gif = imageio.get_writer('final.gif')
                c = 0
                for frame_number in range(all_frames):
                    try:
                        img1 = av1.get_next_data()
                        img2 = av2.get_next_data()
                        new_image = np.hstack((img1, img2))
                        new_gif.append_data(new_image)
                    except ValueError:
                        await ctx.send("Their is large difference in size of the avatars, so Kanna is not able to align them :(")
                        c = c + 1
                        break
                if c == 0:
                    gif = PIL.Image.open("./final.gif")
                    framess = [frame.copy() for frame in PIL.ImageSequence.Iterator(gif)]
                    framess[0].save('shared.gif',
        		        save_all = True, append_images = framess[1:],
        		        optimize = False, duration = 100, loop=0)
                    file = discord.File('shared.gif')
                    embed = discord.Embed(title="Avatar" ,color=0xe91e63)
                    embed.set_author(name=ctx.author, icon_url=ctx.author.avatar.url)
                    embed.timestamp = datetime.datetime.utcnow()
                    embed.set_image(url="attachment://shared.gif")

                    await ctx.send(embed=embed, file=file)
            else:
                bg.save("avatar.png")
                file = discord.File("avatar.png")
                embed = discord.Embed(title="Avatar" ,color=0xe91e63)
                embed.set_author(name=ctx.author, icon_url=ctx.author.avatar.url)
                embed.timestamp = datetime.datetime.utcnow()
                embed.set_image(url="attachment://avatar.png")
                await ctx.send(embed=embed, file=file)

    @commands.command(usage=f"`< user >`", description=f"Check Server Specific Avatar.")
    async def serverav(self, ctx,m1: discord.Member = None ):
        '''Check Server Specific Avatar.'''
        if m1 is None:
            m1 = ctx.author
        embed = discord.Embed(color=0xe91e63)
        embed.set_author(name=ctx.author, icon_url=ctx.author.avatar.url)
        embed.timestamp = datetime.datetime.utcnow()
        embed.set_image(url=m1.display_avatar.url)
        await ctx.send(embed=embed)

    @commands.command(usage=f"`< user >`",description=f"Check Banner of a User.")
    async def banner(self, ctx,m1: discord.Member = None ):
        '''Check Banner of a User.'''
        if m1 is None:
            m1 = ctx.author
        auth = await self.bot.fetch_user(m1.id)
        embed = discord.Embed(color=0xe91e63)
        embed.set_author(name=ctx.author, icon_url=ctx.author.avatar.url)
        embed.timestamp = datetime.datetime.utcnow()
        if auth.banner.url is None:
            return
        embed.set_image(url=auth.banner.url)
        await ctx.send(embed=embed)

    @commands.command(usage=f"`< user1 >` `< user2 >` ...", description=f"Multiple Pfp Merger.")
    async def multipfp(self, ctx):
        '''Multiple Pfp Merger.'''
        members = ctx.message.mentions
        if members == []:
            members = [ctx.author]
        if len(members) == 1:
            embed = discord.Embed(color=0xe91e63)
            embed.set_author(name=ctx.author, icon_url=ctx.author.avatar.url)
            embed.timestamp = datetime.datetime.utcnow()
            embed.set_image(url=members[0].avatar.url)
            await ctx.send(embed=embed)
            return

        animated = []
        for m in members:
            animated.append(m.avatar.is_animated())

        imgs = []
        for mem in members:
            url = requests.get(mem.avatar.url)
            im = PIL.Image.open(BytesIO(url.content))
            imgs.append(im)

        s = len(imgs)
        # print(animated)
        all_animated = all(animated)
        all_not_animated = not any(animated)
        # print(all_animated, all_not_animated)
        if all_animated:  # ANIMATED ############
            frames = []

            s = len(imgs)
            print("S", s)
            d = 250
            bg = PIL.Image.new(mode="RGBA", size=(d * s, d))

            for gif in imgs:
                f = []
                while True:
                    try:
                        gif.seek(gif.tell() + 1)
                        f.append(gif.copy().resize((d, d)))
                    except Exception as e:
                        frames.append(f)
                        break

            frames_imgs = []
            s = len(frames)
            f_no = 0
            while True:
                i = 0
                brk = False
                bg = PIL.Image.new(mode="RGBA", size=(d * s, d))
                for x in range(0, s):
                    try:
                        bg.paste(frames[i][f_no], (d * x, 0))
                        i += 1
                        frames_imgs.append(bg)
                    except Exception as e:
                        print(e, i)
                        brk = True
                f_no += 1
                if brk:
                    break
            # print(frames_imgs)
            if frames_imgs == []:
                frames_imgs = imgs

            # print(frames_imgs)
            frames_imgs[0].save(
                # f"images/generated/{ctx.author.id}.gif",
                # learn to put your generated stuff in a seperated folder and delete them later BRUH! :<
                f"{ctx.author.id}.gif",
                save_all=True,
                append_images=frames_imgs[:],
                loop=0,
                quality=1,
            )
            file = discord.File(
                # f"images/generated/{ctx.author.id}.gif", filename="pic.gif"
                f"{ctx.author.id}.gif", filename="pic.gif"
            )
            emb = discord.Embed(title="", description=f"", color=0xe91e63)
            emb.set_image(url="attachment://pic.gif")
        else:
            s = len(imgs)
            bg = PIL.Image.new(mode="RGBA", size=(500 * s, 500))
            i = 0
            for x in range(0, s):
                try:
                    bg.paste(imgs[i].resize((500, 500)), (500 * x, 0))
                    i += 1
                except Exception as e:
                    print(e, i)
                    pass
            # bg.save(f"images/generated/{ctx.author.id}.png", quality=10)
            bg.save(f"{ctx.author.id}.png", quality=10)
            file = discord.File(
                # f"images/generated/{ctx.author.id}.png", filename="pic.jpg"
                f"{ctx.author.id}.png", filename="pic.jpg"
            )
            embed = discord.Embed(color=0xe91e63)
            embed.set_author(name=ctx.author, icon_url=ctx.author.avatar.url)
            embed.timestamp = datetime.datetime.utcnow()
            embed.set_image(url="attachment://pic.jpg")

        await ctx.send(file=file, embed=embed)

    @commands.command(usage="`[ Message ]`", description=f"Set an AFK status to display when you are mentioned. [NOTE: If the message starts with `=` bot won't remove the afk.]")
    async def afk(self, ctx, *, message=None):
        """Set an AFK status to display when you are mentioned. [nOTE: If the message starts with `=` bot won't remove the afk.]"""
        if message == None:
            message = "AFK"
        nick = ctx.author.display_name
        if not "[AFK]" in ctx.author.display_name:
            nick = "[AFK] " + nick
        try:
            await ctx.author.edit(nick = nick)
            afk.afkcreate(ctx.author.id, ctx.guild.id, message)
            await ctx.reply(f"`{ctx.author.name}` your AFK has been set: {message}")
        except Exception:
            afk.afkcreate(ctx.author.id, ctx.guild.id, message)
            await ctx.reply(f"`{ctx.author.name}` your AFK has been set: {message}")
        
        
    @commands.Cog.listener()
    async def on_message(self, message):
        if afk.checkafk(message.author.id, message.guild.id):
            if not message.content.startswith("="):
                ping = afk.get_ping(message.author.id, message.guild.id)
                afk.remove_afk(message.author.id, message.guild.id)
                
                new_nick = message.author.display_name.strip("[AFK]")
                try:
                    await message.author.edit(nick=new_nick)
                    await message.reply(f"Welcome back! your AFK has been removed\nYou were pinged **{ping}** times! ", delete_after=15)
                except Exception:
                    await message.reply(f"Welcome back! your AFK has been removed\nYou were pinged **{ping}** times! ", delete_after=15)
        for mention in message.mentions:
            if afk.checkafk(mention.id, message.guild.id):
                if message.author.bot:
                    return
                else:
                    note = afk.get_afk_message(mention.id, message.guild.id)
                    await message.reply(
                    f"`{mention}` is AFK: **{note}**", delete_after=15)
                    afk.add_ping(mention.id, message.guild.id)

    @commands.command(name=f"enlarge",aliases=["jumbo"], brief="Enlarge an emoji!",usage="`< emoji >`",description="Enlarge an emoji!")
    async def enlarge(self, ctx, *, content):
        cont = content.split()
        embeds = []
        for word in cont:
            if word.startswith("<") and word.endswith(">"):
                lst = word.strip("<:a>").split(":")
                if word.startswith("<a:"):
                    emoj = discord.PartialEmoji(name=lst[0], id=lst[1], animated=True)
                else:
                    emoj = discord.PartialEmoji(name=lst[0], id=lst[1])
                asset = emoj.url
                emb = discord.Embed(description=f"`{lst[1]}`\n`{lst[0]}`", color=0x2e69f2)
                emb.set_author(
                    name="Enlarged Emotes!",
                    icon_url=ctx.author.avatar.url
                )
                emb.set_image(url=str(asset))
                embeds.append(emb)
        paginator = BotEmbedPaginator(ctx, embeds, control_emojis=("⏮", "◀", "▶", "⏭"))
        await paginator.run()

    # @commands.command()
    # async def blacklist(self, ctx, channel=None):
    #     """Blacklist a channel."""
    #     if channel is None:
    #         channel = ctx.channel
    #     if afk.is_channel_blacklisted(ctx.guild.id, channel.id):
    #         afk.remv_blacklist(ctx.guild.id, channel.id)
    #         emb = discord.Embed(description=f"Removed {channel} from blacklisted channels.")
    #         await ctx.channel.send(embed=emb)
    #     elif not afk.is_channel_blacklisted(ctx.guild.id, channel.id):
    #         afk.add_blacklist(ctx.guild.id, channel.id)
    #         emb = discord.Embed(description=f"Added {channel.id} to blacklisted channels.")
    #         await ctx.channel.send(embed=emb)
    #     else:
    #         return
        
    @commands.command(description=f"Split Image into Two Halves [Couple PFP :flushed:?]")
    async def splitimg(self, ctx):
        """Split Image into Two Halves [Couple PFP :flushed:?]"""
        if len(ctx.message.attachments) > 0  and len(ctx.message.attachments) < 4:
            size = 1000, 500  # 2:1 ratio
            for i in range(0,len(ctx.message.attachments)):
                if str(ctx.message.attachments[i].filename).endswith(".gif"):
                    url = requests.get(ctx.message.attachments[i].url)
                    im = PIL.Image.open(BytesIO(url.content))
                    left, right = [], []
                    for fn in range(0, im.n_frames):
                        im.seek(fn)
                        a = im.copy().resize(size)
                        b = a
                        l = a.crop((0, 0, 500, 500))
                        r = b.crop((500, 0, 1000, 500))
                        left.append(l)
                        right.append(r)

                    left[0].save(
                        f"images/generated/{ctx.author.id}_left.gif",
                        save_all=True,
                        append_images=left,
                    )
                    right[0].save(
                        f"images/generated/{ctx.author.id}_right.gif",
                        save_all=True,
                        append_images=right,
                    )

                    # upload on discord
                    file = [
                        discord.File(
                            f"images/generated/{ctx.author.id}_left.gif", filename="pic.gif"
                        ),
                        discord.File(
                            f"images/generated/{ctx.author.id}_right.gif",
                            filename="pic.gif",
                        ),
                    ]
                    await ctx.send(f"Left [{i+1}]", file=file[0])
                    await ctx.send(f"Right [{i+1}]", file=file[1])
                    # CLEAR SPACE
                    os.system(f"rm -rf images/generated/{ctx.author.id}_left.gif")
                    os.system(f"rm -rf images/generated/{ctx.author.id}_right.gif")
                else:
                    url = requests.get(ctx.message.attachments[i].url)
                    im = PIL.Image.open(BytesIO(url.content))
                    
                    a = im.copy().resize(size)
                    b = a
                    l = a.crop((0, 0, 500, 500))
                    r = b.crop((500, 0, 1000, 500))
                    l.save(f"images/generated/{ctx.author.id}_left.png")
                    r.save(f"images/generated/{ctx.author.id}_right.png")

                    # upload on discord
                    file = [
                        discord.File(
                            f"images/generated/{ctx.author.id}_left.png", filename="pic.png"
                        ),
                        discord.File(
                            f"images/generated/{ctx.author.id}_right.png",
                            filename="pic.png",
                        ),
                    ]
                    await ctx.send(f"Left [{i+1}]", file=file[0])
                    await ctx.send(f"Right [{i+1}]", file=file[1])
                    # CLEAR SPACE
                    os.system(f"rm -rf images/generated/{ctx.author.id}_left.png")
                    os.system(f"rm -rf images/generated/{ctx.author.id}_right.png")
        else:
            await ctx.send("No Images Provided! [Note: You have to upload it and u cant use links too. And You can only Upload 4 Image at Once.]")



def setup(bot):
    bot.add_cog(General(bot))