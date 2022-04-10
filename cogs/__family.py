from datetime import datetime ,date
from os import set_inheritable
import discord
from discord.ext import commands
from database import guildprefix, userdb
from discord.ui import Button, View
import asyncio
from tools import get_image
import random
import asyncio

options = [
            discord.SelectOption(
                label="Partner", description="Check your Marital Status.", emoji=discord.PartialEmoji(name="amyChibiILY", id="863681666673147914")
            ),
            discord.SelectOption(
                label="Siblings", description="Check Your Siblings.", emoji=discord.PartialEmoji(name="amyBlush", id="898532188813950986")
            )
        ]

class FamilyOption(View):
    def __init__(self, bot, user):
        super().__init__()
        self.timeout = 180
        self.bot = bot
        self.user =user
        
        
        
    @discord.ui.select(placeholder="Choose an option.",min_values=1,max_values=1,options=options)
    async def callback(self,selection : discord.ui.Select , interaction: discord.Interaction):
        user1 = interaction.user.id
        if self.user.id:
            prefix = guildprefix.check_prefix(interaction.guild.id)
            desc = f""
            if selection.values[0].lower() == "siblings":
                sib = userdb.showSib(self.user.id).split(",")
                rel = userdb.showSib(self.user.id)
                
                if str(rel) == "0":
                    desc = "You have no E-siblings!"
                    lensib = "0"
                elif len(sib) == 1:
                    ppl = discord.utils.get(self.bot.get_all_members(), id=int(rel))
                    desc= f"`[1] {ppl.name}`"
                    lensib=f"{len(sib)}"
                else:
                    for a in range(len(sib)):
                        lensib = len(sib)
                        try:
                            print(sib[a])
                            ppl = discord.utils.get(self.bot.get_all_members(), id=int(sib[a]))
                            desc = desc + f"`{ppl.name}` | "
                        except Exception as e:
                            print(e)
                embed=discord.Embed(color=self.user.color,description=f"** Siblings[{lensib}] :**\n{desc}")
                embed.set_author(name=f"{self.user.name}'s Siblings", icon_url=self.user.avatar.url)
                embed.timestamp = datetime.utcnow()
                embed.set_footer(icon_url=self.bot.user.avatar.url,text="Team Tatsui ❤️")
                embed.set_image(url=get_image("sib"))
                for sel in options:
                    if sel.label == selection.values[0]:
                        sel.default = True
                    else:
                        sel.default= False
                msg1 = await interaction.response.edit_message(embed=embed,view=self)
            else:
                partner = int(userdb.checkPartner(self.user.id,"id"))

                if partner == 0:
                    emb = discord.Embed(description=f"{self.user.name}, you are not married! Please Marry Someone First! \n Usage : `{prefix}marry `<user>``", color=0xf72585)
                    emb.set_author(name=f"You are not currently married.", icon_url=self.user.avatar.url)
                    for sel in options:
                        if sel.label == selection.values[0]:
                            sel.default = True
                        else:
                            sel.default= False
                    msg1 = await interaction.response.edit_message(embed=emb, view=self)
                    return

                else:
                    dat = userdb.checkPartner(self.user.id, "date")
                    today = datetime.today()
                    some = userdb.checkPartner(self.user.id, "day")
                    someday = datetime.strptime(some ,'%Y-%m-%d')
                    diff = today - someday
                    dates = userdb.checkPartner(self.user.id, "dates")
                    scores = userdb.checkPartner(self.user.id, "scores")
                    prsn = discord.utils.get(self.bot.get_all_members(), id = partner)
                    emb = discord.Embed(description=f"Married since {dat} ({diff.days} days) ! The Perfect Cuple <3 UwU.\nYou've dated `{dates}` times ~Damn!\n> And Your UwU score is `{scores}`! Pretty Good :smirk:", color=0xf72585)
                    emb.set_author(name=f"{self.user.name}, you are happily married to {prsn.name}", icon_url=self.user.avatar.url)
                    emb.set_thumbnail(url=f"https://i.gifer.com/ZdPB.gif")
                    emb.set_footer(text="Team Tatsui ❤️")
            
                    emb.set_image(url=get_image("couple"))
                    for sel in options:
                        if sel.label == selection.values[0]:
                            sel.default = True
                        else:
                            sel.default= False
                    msg1 = await interaction.response.edit_message(embed=emb, view=self)
                    return
        else:
            return

class MarryButton(View):
    def __init__(self, user:discord.User):
        super().__init__()
        self.value = None
        self.user= user

    @discord.ui.button(style=discord.ButtonStyle.success, emoji="<:amyYes:913690556452974592>", label="Yes !!")
    async def yesButton(
        self, button: Button, interaction: discord.Interaction
    ):
        user1 = interaction.user.id
        if self.user.id == user1:
            # await interaction.response.send_message("Confirming", ephemeral=True)
            self.value = True
            self.stop()
        else:
            return


    # This one is similar to the confirmation button except sets the inner value to `False`
    @discord.ui.button(style=discord.ButtonStyle.danger, emoji="<:pepe_no:848275072435224586>", label="No ;-;")
    async def cancel(self, button: Button, interaction: discord.Interaction):
        user1 = interaction.user.id
        if self.user.id == user1:
            # await interaction.response.send_message("Confirming", ephemeral=True)
            self.value = False
            self.stop()
        else:
            return

class Family(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.emoji = "꒰ <:FamilyCategory:943427906674253865> ꒱"
        self.hidden = False
        self.description = "Includes Family Related Commands."

    @commands.command(usage="`<user>`",description="Marry another user !", aliases=["propose", "marrriage", "waifu", "wife", "husbando", "husband"], extras={"emoji": "💒"}, brief="Marry another user !")
    async def marry(self, ctx, user: discord.Member=None):

        prefix = guildprefix.check_prefix(ctx.guild.id)

        if user is None:
            partner = int(userdb.checkPartner(ctx.author.id,"id"))

            if partner == 0:
                emb = discord.Embed(description=f"{ctx.author.name}, you are not married! Please Marry Someone First! \n Usage : `{prefix}marry `<user>``", color=0xf72585)
                emb.set_author(name=f"You are not currently married.", icon_url=ctx.author.avatar.url)
                await ctx.channel.send(embed=emb)
                return

            else:
                dat = userdb.checkPartner(ctx.author.id, "date")
                today = datetime.today()
                some = userdb.checkPartner(ctx.author.id, "day")
                someday = datetime.strptime(some ,'%Y-%m-%d')
                diff = today - someday
                prsn = discord.utils.get(self.bot.get_all_members(), id = partner)
                points = userdb.checkPartner(ctx.author.id, "scores")
                dates = userdb.checkPartner(ctx.author.id, "dates")
                emb = discord.Embed(description=f"Married since {dat} ({diff.days} days) ! The Perfect Cuple <3 UwU.\nYou've dated `{dates}` times ~Damn!\n> And Your UwU score is `{points}`! Pretty Good :smirk:", color=0xf72585)
                emb.set_author(name=f"{ctx.author.name}, you are happily married to {prsn.name}", icon_url=ctx.author.avatar.url)
                emb.set_thumbnail(url=f"https://i.gifer.com/ZdPB.gif")
                emb.set_image(url=get_image("couple"))
                emb.set_footer(text="Team Tatsui ❤️")
                await ctx.channel.send(embed=emb)
                return
        
        elif not user.bot:
            if ctx.author.id == user.id:
                emb = discord.Embed(title=f"", description=f"> You Can't Marry Yourself Dumbo!\n**__Usage__:**\n`{prefix}marry `<user>``", color=0xf72585)
                emb.set_author(name=f"Sheesh!", icon_url=ctx.author.avatar.url)
                emb.set_image(url="https://c.tenor.com/mW-BeHkDVKEAAAAC/monsters-inc-pixar.gif")
                emb.timestamp = datetime.utcnow()
                emb.set_footer(text="Team Tatsui ❤️")
                await ctx.channel.send(embed=emb)
                return
            
            if userdb.is_sibling(ctx.author.id, user.id):
                emb = discord.Embed(title=f"", description=f"> You Can't Marry Your Sibling !!\nI mean u can- But my dev won't allow it.\n**__Usage__:**\n`{prefix}marry `<user>``", color=0xf72585)
                emb.set_author(name=f"Wha-! You Wanna Marry Your Sibling?", icon_url=ctx.author.avatar.url)
                emb.timestamp = datetime.utcnow()
                emb.set_footer(text="Team Tatsui ❤️")
                emb.set_image(url="https://c.tenor.com/wuupKv_VikQAAAAC/sweet-home-alabama.gif")
                await ctx.channel.send(embed=emb)
                return
            
            prsn1 = int(userdb.checkPartner(ctx.author.id,"id"))
            prsn2 = int(userdb.checkPartner(user.id, "id"))
            if prsn1 == 0 and prsn2 == 0:
                emb = discord.Embed(description=f"Hey, {user.mention}, it would make {ctx.author.mention} really happy if you would marry them. What do you say?\n", color=0xf72585)
                emb.set_author(name=f"{ctx.author.name} has proposed to {user.name}! <3 ")
                emb.timestamp = datetime.utcnow()



                btn3= Button(style=discord.ButtonStyle.blurple, emoji="<:amySad1:913697522474704916>", label="TIMEUP", disabled=True)

                view = MarryButton(user)


                msg = await ctx.channel.send(embed=emb, view=view)
                try:
                    await view.wait()
                    if view.value is None:

                        view2= View()
                        view2.add_item(btn3)
                        await msg.edit(view=view2)
                        emb = discord.Embed(f"😠 || Sorry, {ctx.author.mention}, {user.name} didn't reply on time!! Maybe They are confused, lets give them some time!", color=0xf72585)
                        emb.timestamp = datetime.utcnow()
                        await ctx.send(embed=emb)

                    elif view.value:
                        view2= View()
                        view2.add_item(btn3)
                        await msg.edit(view2)
                        emb = discord.Embed(description=f"💒 || {ctx.author.mention} and {user.mention} are now married! Congrats!!", color=0xf72585)
                        emb.timestamp = datetime.utcnow()
                        
                        await ctx.send(embed=emb)
                        userdb.addPartner(user.id, "id",str(ctx.author.id))
                        userdb.addPartner(ctx.author.id, "id",str(user.id))

                        userdb.addPartner(user.id, "date",str(ctx.author.id))
                        userdb.addPartner(ctx.author.id, "date",str(user.id))

                        userdb.addPartner(user.id, "day",str(ctx.author.id))
                        userdb.addPartner(ctx.author.id, "day",str(user.id))

                        userdb.addPartner(user.id, "dates",1)
                        userdb.addPartner(ctx.author.id, "dates",1)

                        userdb.addPartner(user.id, "scores",500)
                        userdb.addPartner(ctx.author.id, "scores",500)

                        return
                    else:
                        view2= View()
                        view2.add_item(btn3)
                        view2= View()
                        await msg.edit(view=view2)
                        emb = discord.Embed(f"💔 || {user.mention}, you have decline a marriage request to {ctx.author.mention}", color=0xf72585)
                        emb.timestamp = datetime.utcnow()
                        
                        await ctx.send(embed=emb)
                        
                        return

                except Exception as err:
                    print(err)
                    view2= View()
                    view2.add_item(btn3)
                    await msg.edit(view=view2)
                    emb = discord.Embed(f"😠 || Sorry, {ctx.author.mention}, {user.name} didn't reply on time!! Maybe They are confused, lets give them some time!", color=0xf72585)
                    emb.timestamp = datetime.utcnow()
                    await ctx.send(embed=emb)
                    return err
            elif prsn1 != 0 and prsn2==0 or  prsn1 == 0 and prsn2!=0 or prsn1 != 0 and prsn2 !=0:
                emb = discord.Embed(f":no_entry_sign: | **{ctx.author.name}** , you or your friend is already married!", color=0xf72585)
                emb.timestamp = datetime.utcnow()
                await ctx.send(embed=emb)
                
                return
            else:
                return


    @commands.command(description="Take a Divorce!", aliases=["divorce", "unmarry", "unwaifu", "unwife", "unhusbando", "unhusband"], extras={"emoji": "❌"}, brief="Take a Divorce!")
    async def div(self,ctx):

        
        prefix = guildprefix.check_prefix(ctx.guild.id)
        partner = int(userdb.checkPartner(ctx.author.id,"id"))

        if partner == 0:
            await ctx.reply(f":no_entry_sign: | {ctx.author.mention}, you can't divorce if you aren't married!")
            return
        else:
            try:
                ppl = discord.utils.get(self.bot.get_all_members(), id=partner)

                dat = userdb.checkPartner(ctx.author.id, "day")
                today = datetime.today()
                some = userdb.checkPartner(ctx.author.id, "date")
                someday = datetime.strptime(some ,'%Y-%m-%d')
                diff = today - someday
                
                emb=discord.Embed(description=f"You married on {dat} and have been married for {diff.days} days... Once you divorce, the ring will break and disappear.")
                emb.set_author(name=f"{ctx.author.name}, are you sure you want to divorce {ppl.name}?", icon_url=ctx.author.avatar.url)
                emb.set_thumbnail(url="https://i.gifer.com/ZdPB.gif")
                view = MarryButton(ctx.author)


                msg = await ctx.channel.send(embed=emb, view=view)
                try:
                    await view.wait()
                    if view.value is None:

                        view2= View()
                        btn3= Button(style=discord.ButtonStyle.blurple, emoji="<:amySad1:913697522474704916>", label="timeup", disabled=True)
                        view2.add_item(btn3)
                        await msg.edit(view=view2)
                        await ctx.send(f"😠 || Sorry, {ctx.author.mention} you didn't reply on time!!")

                    elif view.value:
                        view2= View()
                        btn3= Button(style=discord.ButtonStyle.blurple, emoji="<:amySad1:913697522474704916>", label="timeup", disabled=True)
                        view2.add_item(btn3)
                        await msg.edit(view2)
                        await ctx.send(f":broken_heart:  || {ctx.author.mention}, You have decided to divorce.")
                        userdb.rmvPartner(ctx.author.id)
                        userdb.rmvPartner(ppl.id)
                        
                        return
                    else:
                        view2= View()
                        btn3= Button(style=discord.ButtonStyle.blurple, emoji="<:amySad1:913697522474704916>", label="timeup", disabled=True)
                        await msg.edit(view=view2)
                        await ctx.send(f"👍 || {ctx.author.mention},You have declined to divorce.")
                        return

                except asyncio.TimeoutError:
                    view2= View()
                    btn3= Button(style=discord.ButtonStyle.blurple, emoji="<:amySad1:913697522474704916>", label="timeup", disabled=True)
                    await msg.edit(view=view2)
                    await ctx.send(f"😠 || Sorry, {ctx.author.mention} you didn't reply on time!!")
                    return
            except:
                return

    @commands.command(usage="`<user>`",description="Make someone your Sibling", aliases=["rakhi", "sib", "bro", "sis"], extras={"emoji": "❌"}, brief="Take a Divorce!")
    async def sibling(self, ctx, user: discord.Member=None):

        prefix = guildprefix.check_prefix(ctx.guild.id)
        if user == None:
            rel = userdb.showSib(ctx.author.id)
            sib = rel.split(",")
            desc = ""
            if rel == "0":
                emb=discord.Embed(description=f"{ctx.author.name}, You have no E-siblings right now! Please make Someone First! ex. `{prefix}sib `<user>`` ", color=0xf72585)
                emb.set_author(name="Lonely Soul", icon_url=ctx.author.avatar.url)
                emb.set_thumbnail(url="https://i.pinimg.com/originals/b3/8e/27/b38e27402bc8accd4e9b313a1b567fa6.gif")
                await ctx.send(embed=emb)
                return
            if len(sib) == 1:
                ppl = discord.utils.get(self.bot.get_all_members(), id=int(rel))
                emb=discord.Embed(description=f"▪️ {ppl.name} `({ppl.id})`", color=0xf72585)
                emb.set_author(name=f"{ctx.author.name}, you have {len(sib)} Siblings : ", icon_url=ctx.author.avatar.url)
                emb.set_thumbnail(url="https://4.bp.blogspot.com/-T2bVs6xiUks/XHeLMCZlvOI/AAAAAAAUQDU/k-8YrZmX5j4S9VOaOULzqtExdduBcfPtQCLcBGAs/s1600/AW3567431_10.gif")
                emb.timestamp = datetime.utcnow()
                emb.set_footer(icon_url=self.bot.user.avatar.url)
                await ctx.send(embed=emb)
                return
            else:
                for a in range(len(sib)):
                    try:
                        ppl = discord.utils.get(self.bot.get_all_members(), id=int(sib[a]))
                        desc = desc + f"`{ppl.name}` | "
                    except Exception as e:
                        print(e)

                emb=discord.Embed(description=f"{desc}\n>>> `Foolo ka Taaron Ka Sabka Kehna hai!`", color=0xf72585)
                emb.set_author(name=f"{ctx.author.name}, you have {len(sib)} siblings : ", icon_url=ctx.author.avatar.url)
                emb.timestamp = datetime.utcnow()
                emb.set_footer(icon_url=self.bot.user.avatar.url)
                emb.set_thumbnail(url="https://4.bp.blogspot.com/-T2bVs6xiUks/XHeLMCZlvOI/AAAAAAAUQDU/k-8YrZmX5j4S9VOaOULzqtExdduBcfPtQCLcBGAs/s1600/AW3567431_10.gif")
                await ctx.send(embed=emb)
                return
        if ctx.author.id ==user.id:
            await ctx.reply("Sad Soul!!")
            return
        elif not user.bot:
            rel = str(userdb.showSib(ctx.author.id))
            rel2 = str(userdb.showSib(user.id))

            if userdb.is_partner(ctx.author.id, user.id):
                emb = discord.Embed(title=f"", description=f"> If You wanna make your partner your sibling, First take a divorce!\n**__Usage__:**\n`{prefix}div `<user>``")
                emb.set_author(name=f"Wha-! You Wanna Make Your Partner Sibling?", icon_url=ctx.author.avatar.url)
                emb.timestamp = datetime.utcnow()
                emb.set_footer(text="Team Tatsui ❤️")
                await ctx.channel.send(embed=emb)
                return

            sib = rel.split(",")
            sib2 = rel2.split(",")
            if rel == "0" and rel2=="0" or str(user.id) not in sib and str(ctx.author.id) not in sib2 :
                emb = discord.Embed(description=f"Hey {user.mention},  I feel glad too say that {ctx.author.mention} wants to make you their sibling ! It would make them  really happy if you accept this proposal. What do you say?\n")
                emb.set_author(name=f"{ctx.author.name} wants to make {user.name} their Sibling! <3 ")
                emb.timestamp = datetime.utcnow()
                emb.set_thumbnail(url="https://cdn.discordapp.com/attachments/865570883170861077/865875381537734686/output-onlinegiftools.gif")
                emb.set_footer(icon_url=self.bot.user.avatar.url)
                
                view = MarryButton(user)


                msg = await ctx.channel.send(embed=emb, view=view)
                try:
                    await view.wait()
                    if view.value is None:

                        view2= View()
                        btn3= Button(style=discord.ButtonStyle.blurple, emoji="<:amySad1:913697522474704916>", label="timeup", disabled=True)
                        view2.add_item(btn3)
                        await msg.edit(view=view2)
                        await ctx.send(f"😠 || Sorry, {ctx.author.mention}, {user.name} didn't reply on time!! Maybe They are confused, lets give them some time!")

                    elif view.value:
                        view2= View()
                        btn3= Button(style=discord.ButtonStyle.blurple, emoji="<:amySad1:913697522474704916>", label="timeup", disabled=True)
                        view2.add_item(btn3)
                        await msg.edit(view=view2)
                        userdb.addSib(ctx.author.id, user.id)
                        userdb.addSib(user.id, ctx.author.id)
                        await ctx.send(f"🏡 || {user.mention}, Yay! {ctx.author.mention} is now your Sibling. Congrats!!")
                        return
                
                    else:
                        view2= View()
                        btn3= Button(style=discord.ButtonStyle.blurple, emoji="<:amySad1:913697522474704916>", label="timeup", disabled=True)
                        await msg.edit(view=view2)
                        await ctx.send(f"💔 || {ctx.author.mention} Sorry ! But {user.mention} declined your request :((")
                        return

                except asyncio.TimeoutError:
                    view2= View()
                    btn3= Button(style=discord.ButtonStyle.blurple, emoji="<:amySad1:913697522474704916>", label="timeup", disabled=True)
                    await msg.edit(view=view2)
                    await ctx.send(f"😠 || Sorry, {ctx.author.mention} you didn't reply on time!!")
                    return
            else:
                await ctx.send(f"You Guys are Already Siblings !")
        else:
            await ctx.reply("BRUH!! You can't make a bot your Sibling!!")

    @commands.command(aliases=["nosib"], brief="Disown Your Sister.",usage="`<user>`",name="disown",enabled="",help="Disown Your Sister.", extras={"emoji": "😭"},description="Disown Your Sister.")
    @commands.cooldown(rate=1, per=5, type=commands.BucketType.default)
    async def remvsib(self,ctx, user: discord.Member=None):

        prefix = guildprefix.check_prefix(ctx.guild.id)
        rel = userdb.showSib(ctx.author.id).seplit(',')
        if len(rel) == 0:
            await ctx.reply(f"{ctx.author.name}, You have no E-siblings right now! Please make Someone First! ex. `{prefix}sib `<user>``")
            return
        if user == None:
            await ctx.send("Please use @mention  someone.")
            return
        else:
            try:
                if str(user.id) in rel:
                    emb=discord.Embed(description=f"{ctx.author.mention}, Are you sure? ", color=discord.Color.nitro_pink())
                    emb.set_author(name=f"{ctx.author.name}, are you sure you want to disown {user.name} as your Sibling?", icon_url=ctx.author.avatar.url)
                    view = MarryButton(ctx.author)


                    msg = await ctx.channel.send(embed=emb, view=view)
                    try:
                        await view.wait()
                        if view.value is None:

                            view2= View()
                            btn3= Button(style=discord.ButtonStyle.blurple, emoji="<:amySad1:913697522474704916>", label="timeup", disabled=True)
                            view2.add_item(btn3)
                            await msg.edit(view=view2)
                            await ctx.send(f"😠 || Sorry, {ctx.author.mention}, {user.name} didn't reply on time!! Maybe They are confused, lets give them some time!")
                            return

                        elif view.value:
                            view2= View()
                            btn3= Button(style=discord.ButtonStyle.blurple, emoji="<:amySad1:913697522474704916>", label="timeup", disabled=True)
                            view2.add_item(btn3)
                            await msg.edit(view2)
                            await msg.edit( components=[])
                            await ctx.send(f":broken_heart:  || {ctx.author.mention}, You have decided to disown them as sibling.")
                            userdb.rmvSib(ctx.author.id, str(user.id))
                            userdb.rmvSib(user.id, str(ctx.author.id))

                            return
                    
                        else:
                            view2= View()
                            btn3= Button(style=discord.ButtonStyle.blurple, emoji="<:amySad1:913697522474704916>", label="timeup", disabled=True)
                            await msg.edit(view=view2)
                            await ctx.send(f"👍 || {ctx.author.mention},You have declined")
                            return

                    except asyncio.TimeoutError:
                        view2= View()
                        btn3= Button(style=discord.ButtonStyle.blurple, emoji="<:amySad1:913697522474704916>", label="timeup", disabled=True)
                        await msg.edit(view=view2)
                        await ctx.send(f"😠 || Sorry, {ctx.author.mention} you didn't reply on time!!")
                        return
                else:
                    await ctx.send(f"You Guys are Already Siblings !")
            except:
                return


    @commands.command(brief="Check your Family.",usage="`[user]`",name="family",help="Check your Family.", extras={"emoji": "👪"},description="Check your Family.")
    @commands.cooldown(rate=1, per=5, type=commands.BucketType.default)
    async def family(self,ctx, user: discord.Member=None):

        prefix = guildprefix.check_prefix(ctx.guild.id)
        if user == None:
            view = FamilyOption(self.bot, ctx.author)
            emb = discord.Embed(color=ctx.author.color,description=f"Nickname: `{ctx.author.name}`\nID: `{ctx.author.id}`")
            emb.set_thumbnail(url=ctx.author.avatar.url)
            emb.set_author(name=f"{ctx.author.name}'s Family", icon_url=ctx.author.avatar.url)
            emb.add_field(name=f"Check Family - ", value=f"Select Desired Family option from DropDown.")
            msg = await ctx.channel.send(embed=emb, view=view)
            try:
                await view.wait()        
                a = await view.on_timeout()
                await msg.edit(view=None)
            except Exception as err:
                print(err)
        else:
            if userdb.is_profile_enabled(user.id):
                view = FamilyOption(self.bot, user)
                emb = discord.Embed(color=user.color,description=f"Nickname: `{user.name}`\nID: `{user.id}`")
                emb.set_thumbnail(url=user.avatar.url)
                emb.set_author(name=f"{user.name}'s Family", icon_url=user.avatar.url)
                emb.add_field(name=f"Check Family - ", value=f"Select Desired Family option from DropDown.")
                msg = await ctx.channel.send(embed=emb, view=view)
                try:
                    await view.wait()        
                    a = await view.on_timeout()
                    await msg.edit(view=None)
                except Exception as err:
                    print(err)
            else: 
                return

    @commands.command(aliases=["daily", "hangout"],name="date",help="CLaim UwU Points by Dating.", extras={"emoji": "👪"},description="CLaim UwU Points by Dating.")
    async def date(self,ctx):
        prefix = guildprefix.check_prefix(ctx.guild.id)
        scores = userdb.checkPartner(ctx.author.id, "scores")
        part = userdb.checkPartner(ctx.author.id, "id")
        dates = userdb.checkPartner(ctx.author.id, "dates")
        money = random.randint(100,500)
        if not userdb.is_married(ctx.author.id):
            emb = discord.Embed(description=f"{ctx.author.name}, you are not married! In Order to get UwU points ,Please Marry Someone First! \n Usage : `{prefix}marry `<user>``")
            emb.set_author(name=f"You are not currently married.", icon_url=ctx.author.avatar.url)
            return await ctx.channel.send(embed=emb)
        else:
            if not userdb.date_today(ctx.author.id) or userdb.date_today(part):
                emb = discord.Embed(description=f"💰 | {ctx.author.mention}, Here is your daily for your date `{money}`\n💞 | You've dated {dates} times!\nAnd Your UwU score is `{scores}`! Pretty Good :smirk:")
                await ctx.channel.send(embed=emb)
                userdb.addmoney(ctx.author.id, money)
                userdb.addPartner(ctx.author.id, "dates", 1)
                userdb.addmoney(part, money)
                userdb.addPartner(part, "dates", 1)
                userdb.change_date(ctx.author.id, True)
                userdb.change_date(part, True)
                asyncio.sleep(25200)
                userdb.change_date(ctx.author.id, False)
                userdb.change_date(part, False)
                return
            else: return

    @commands.command(aliases=["lb", "marrylb"], usage=f"`[guild | global]`" )
    async def mlb(self, ctx, *, arg: str = None):
        """Shows Leadeboard for UwU points."""
        if arg == None:
            await ctx.send(embed = await userdb.get_lb(self.bot, ctx.author))
        elif arg.lower() == "guild":
            await ctx.send(embed = await userdb.get_guild_lb(self.bot,ctx.guild, ctx.author))
        elif arg.lower() == "global":
            await ctx.send(embed = await userdb.get_lb(self.bot,ctx.author))
        
        else:
            emb = discord.Embed(description="Commands Available:\n> `mlb guild` for server marriage leaderboard.\n> `mlb global` for global marriage leaderboard.", color=discord.Color.red())
            emb.set_author(
                name="Invalid Argument!",
                icon_url=ctx.author.display_avatar
            )
            await ctx.send(embed=emb)

    @commands.command(usage=f"`<enable | disable>`")
    async def profile(self, ctx, *, arg:str = None):
        "Enable or Disable Your Profile."
        if arg == None:
            await ctx.reply('Usage : `a!profile [enable | disable]`')
        elif arg.lower() == "enable":
            userdb.enableProfile(ctx.author.id)
            await ctx.message.react('👍')
        elif arg.lower() == "disable":
            userdb.disableProfile(ctx.author.id)
            await ctx.message.react('👍')
        
        else:
            return

def setup(bot):
    bot.add_cog(Family(bot))