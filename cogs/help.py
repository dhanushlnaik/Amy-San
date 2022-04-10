import discord
from discord.ext import commands 
from datetime import datetime
import contextlib
from database import guildprefix
from discord.ui import View ,Button
from utils import HelpPaginator

def get_options(ctx):
    options = []
    bot = ctx.bot
    for cogn in bot.cogs:
            
        if not cogn: pass
        cog = bot.get_cog(cogn)
            
        options.append(discord.SelectOption(label=cogn, description=cog.description, emoji=cog.emoji))
        return options

def ButHelp(ctx,cog, desc):
    embed = discord.Embed(description=f"```diff\n- <> = optional argument\n- [] = required argument```")
    
    embed.set_author(name=f"{ctx.bot.user.name} | Help", icon_url=ctx.guild.icon.url)
    embed.set_footer(text=f"Team Tatsui", icon_url=ctx.bot.user.avatar.url)
    embed.set_thumbnail(url=ctx.author.avatar.url)
    embed.add_field(name=f"-꒰ Commands ꒱-", value=desc)
    return embed


options = [
    discord.SelectOption(label="Actions", description="Includes Roleplay/Action Commands.", emoji=discord.PartialEmoji(name="EmotesCategory", id=943427911027925082)),
    discord.SelectOption(label="Anime", description="Includes Anime Related Commands.", emoji=discord.PartialEmoji(name="EmiPuck", id=943366309775835247,animated=True)),
    discord.SelectOption(label="General", description="Includes General Commands.", emoji=discord.PartialEmoji(name="GeneralCategory", id=943427909752856577)),
    discord.SelectOption(label="Fun", description="Includes Fun Related Commands.", emoji=discord.PartialEmoji(name="FunCategory", id=943427905931857961)),
    discord.SelectOption(label="Meme", description="Includes Meme Related Commands.", emoji=discord.PartialEmoji(name="MemeCategory", id=943427907877994507)),
    discord.SelectOption(label="Info", description="Includes Info Related Commands.", emoji=discord.PartialEmoji(name="InformationCategory", id=943427908691701771)),
    discord.SelectOption(label="Utility", description="Includes Utility Related Commands.", emoji=discord.PartialEmoji(name="AEmiThinkC", id=943366254243233822)),
    discord.SelectOption(label="Moderation", description="Includes Moderation Related Commands.", emoji=discord.PartialEmoji(name="ModerationCategory", id=943428021212307476, animated=True)),
    discord.SelectOption(label="Family", description="Includes Family Related Commands.", emoji=discord.PartialEmoji(name="FamilyCategory", id=943427906674253865))
]

cog = ["Actions", "Anime","Fun", "Meme", "Info", "Utility", "Moderation", "Family"]

def getDesc(ctx):
    prefix = guildprefix.check_prefix(ctx.guild.id)
    descDic = {}
    descLi = []
    pages = []
    desc = f""
    cog = ["Actions", "Anime","Fun", "Meme", "Info", "Utility", "Moderation", "Family"]
    n = 1
    for cogn in cog:
        descDic[cogn] = []
        desc =f""
        
        for command in ctx.bot.walk_commands():
            if command.cog_name is None: pass
            elif command.cog_name.lower() == cogn.lower():
                if not len(desc) >= 900:
                    
                    if command.usage is None: 
                        desc += f"ꕤ `{command.name}`\n<:amyReply:944636367881797683> {command.description}\n\n"
                    else:
                        desc += f"ꕤ `{command.name}` {command.usage}\n<:amyReply:944636367881797683> {command.description}\n\n"
                else:
                    descDic[cogn].append(desc)
                    descLi.append(desc)
                    
                    desc = f""
                    if command.usage is None: 
                        desc += f"ꕤ `{command.name}`\n<:amyReply:944636367881797683> {command.description}\n\n"
                    else:
                        desc += f"ꕤ `{command.name}` {command.usage}\n<:amyReply:944636367881797683> {command.description}\n\n"
        descDic[cogn].append(desc)
        descLi.append(desc)   
        # descDic[cogn].append(descLi)
    
    
    return descDic , descLi
            
    
def help_embed(ctx, cog):
    prefix = guildprefix.check_prefix(ctx.guild.id)
    cogO = ctx.bot.get_cog(cog)
    embed = discord.Embed()
    embed.set_author(name=f"{ctx.bot.user.name} | Help", icon_url=ctx.guild.icon.url)
    embed.set_footer(text=f"Team Tatsui", icon_url=ctx.bot.user.avatar.url)
    embed.set_thumbnail(url=ctx.author.avatar.url)
    desc = f""
    n = 1
    descLi = []
    for command in ctx.bot.walk_commands():
        if not len(desc) >= 1022:
            if command.cog_name is None:
                pass
            elif command.cog_name.lower() == cog.lower():
                if command.usage is None: 
                    desc += f"ꕤ `{command.name}`\n<:amyReply:944636367881797683> {command.description}\n"
                else:
                    desc += f"ꕤ `{command.name}` {command.usage}\n<:amyReply:944636367881797683> {command.description}\n"
                n += 1
        else:
            print(desc)
            descLi.append(desc)
            desc = f""
    descEmb = []
    if not len(descLi) == 0:
        for desc in descLi:
            descEmb.append(ButHelp(ctx,cog,desc))
    else:
        descEmb.append(embed)

    return descEmb
    
    

class HelpView(View):
    def __init__(self, ctx):
        super().__init__(timeout=60)
        self.ctx=ctx


    @discord.ui.select(
        placeholder="Select any Category",
        min_values=1,
        max_values=1,
        options=options,
    )
    async def callback(self, select, interaction):
        emb = help_embed(self.ctx,select.values[0])
        for sel in options:
            if sel.label == select.values[0]:
                sel.default = True
            else:
                sel.default= False
        await interaction.response.edit_message(
            embed=emb, view=self
        )
        #for sel in options:
            #sel.default = False



class MyHelp(commands.HelpCommand):
    async def send_bot_help(self, mapping):
        prefix = guildprefix.check_prefix(self.context.guild.id)
        embed = discord.Embed()
        embed.set_author(name=f"{self.context.bot.user.name} | Help", icon_url=self.context.guild.icon.url)
        embed.set_footer(text=f"Team Tatsui", icon_url=self.context.bot.user.avatar.url)
        embed.set_thumbnail(url=self.context.author.avatar.url)
        ctx = self.context
        usable = 0 
        bot = self.context.bot
        
        
        

        for cog, commands in mapping.items(): #iterating through our mapping of cog: commands
            if filtered_commands := await self.filter_commands(commands): 
                # if no commands are usable in this category, we don't want to display it
                amount_commands = len(filtered_commands)
                usable += amount_commands
                if cog:
                    if cog.hidden : pass
                    emoji = cog.emoji
                    command_signatures = [c.name for c in commands]
                    desc = "`"+"` , `".join(command_signatures) + "`"
                    name = cog.qualified_name
                    description = desc
                else:
                    name = "No Category"
                    description = "Commands with no category"
                    pass
                if not name == "No Category":
                    embed.add_field(name=f"{emoji} {name} Category [{amount_commands}]", value=description, inline=False)
                else: pass

        embed.description = f"Use `{prefix}help [command]` to get more help!\nExample: `{prefix}help pat`.\n\n> {len(bot.commands)} commands | {usable} usable" 
        destination = self.get_destination()
        
        view=HelpView(ctx)
        dic , pages = getDesc(ctx)
        pages = [elem for sublist in dic.values() for elem in sublist]
        
        btn1 = Button(label="Invite", style=discord.ButtonStyle.url, url="https://discord.com/api/oauth2/authorize?client_id=850243448724127754&permissions=140076435526&scope=bot", emoji=discord.PartialEmoji(name="invite", id=939483316367802418))
        btn3 = Button(label="Support Server", style=discord.ButtonStyle.url, url="https://discord.gg/eZFKMmS6vz", emoji=discord.PartialEmoji(name="head", id=939483469426360400))
        btn2 = Button(label="Vote Me", style=discord.ButtonStyle.url, url="https://top.gg/bot/850243448724127754/vote", emoji=discord.PartialEmoji(name="head", id=939483469426360400))
        view.add_item(btn1)
        view.add_item(btn3)
        view.add_item(btn2)
        # PreviousButton = discord.ui.Button(...)
        # NextButton = discord.ui.Button(...)
        # PageCounterStyle = discord.ButtonStyle(...) # Only accepts ButtonStyle instead of Button
        # InitialPage = 0 # Page to start the paginator on.
        # timeout = 42069 # Seconds to timeout. Default is 60
        pa = []
        for d in pages:
            a = ButHelp(ctx, "All", d )
            pa.append(a)
        pa.pop()
        pa.insert(0, embed)
        msg = await destination.send(embed=embed)
        a = await HelpPaginator.Simple().start(ctx, pages=pa, message=msg)
        
        
        # msg = await destination.send(embed=embed, view=view)
        async def timeout():
            for dd in view.children:
                if not isinstance(dd, Button):
                    dd.disabled=True
            await msg.edit(view=view)
        view.on_timeout = timeout
        

    async def send_command_help(self, command):
        """triggers when a `<prefix>help <command>` is called"""
        prefix = guildprefix.check_prefix(self.context.guild.id)
        signature = self.get_command_signature(command) # get_command_signature gets the signature of a command in <required> [optional]
        embed = discord.Embed(title=signature, description=command.description or "No help found...",color=self.context.bot.user.color)
        h = command.help or "No help found..."
        embed = discord.Embed(description=f"```diff\n- [] = optional argument\n- <> = required argument```\n>>> {h}")
        embed.set_author(name=f"{command.name.title()} Info", icon_url= self.context.bot.user.avatar.url)
        if cog := command.cog:
            embed.add_field(name="Category", value=cog.qualified_name,inline=False)

        can_run = "No"
        # command.can_run to test if the cog is usable
        with contextlib.suppress(commands.CommandError):
            if await command.can_run(self.context):
                can_run = "Yes"
            
        embed.add_field(name="Usable", value=can_run,inline=False)
        if command.aliases:
            embed.add_field(name="Aliases", value="`"+"` , `".join(command.aliases) + "`",inline=False)
        embed.add_field(name=f"Usage", value=f"`{command.usage}`",inline=False)

        if command._buckets and (cooldown := command._buckets._cooldown): # use of internals to get the cooldown of the command
            embed.add_field(
                name="Cooldown",
                value=f"{cooldown.rate} per {cooldown.per:.0f} seconds",inline=False
            )
        destination = self.get_destination()
        await destination.send(embed=embed)

    async def send_help_embed(self, title, description, commands): # a helper function to add commands to an embed
        embed = discord.Embed(title=title, description=description or "No help found...")

        if filtered_commands := await self.filter_commands(commands):
            for command in filtered_commands:
                embed.add_field(name=self.get_command_signature(command), value=command.help or "No help found...")
           
        destination = self.get_destination()
        await destination.send(embed=embed)

    async def send_group_help(self, group):
        """triggers when a `<prefix>help <group>` is called"""
        title = self.get_command_signature(group)
        await self.send_help_embed(title, group.help, group.commands)

    async def send_cog_help(self, cog):
        """triggers when a `<prefix>help <cog>` is called"""
        title = cog.qualified_name or "No"
        await self.send_help_embed(f'{title} Category', cog.description, cog.get_commands())

class Help(commands.Cog):
    def __init__(self, bot):
       self.bot = bot
       self.emoji = "ℹ"
       self.hidden = True
        
       help_command = MyHelp()
       
       help_command.cog = self.bot.get_cog("Utility")
       bot.help_command = help_command

    


def setup(bot):
    bot.add_cog(Help(bot))