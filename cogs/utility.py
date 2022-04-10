import discord
import datetime
import json
from datetime import datetime
from discord.ext import commands
import time

class Utility(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.emoji = "꒰ <:AEmiThinkC:943366254243233822> ꒱"
        self.hidden = False
        self.description = "Includes Utility Related Commands."

    @commands.command(description=f"Shows Ping of Bot")
    @commands.guild_only()
    async def ping(self, ctx):
        '''Shows Ping of Bot'''
        before = time.monotonic()
        msg = await ctx.channel.send("\`🏓\` **- Getting my ping ...**")
        ping = (time.monotonic() - before) * 1000
        await msg.delete()
        emb = discord.Embed(color=discord.Color.blurple(), description=f":heartpulse: Command: `{round(ping)} ms` \n:stopwatch: Gateway: `{round(self.bot.latency * 1000)} ms`")
        emb.set_author(name=f"{self.bot.user.name}", icon_url=self.bot.user.avatar.url)
        await ctx.channel.send(embed=emb)
        
    @commands.command(description="Invite the Bot.")
    async def invite(self,ctx):
        emb = discord.Embed( description=f" [Click here](https://discord.com/api/oauth2/authorize?client_id=850243448724127754&permissions=939838544&scope=bot) to invite me :))")
        await ctx.send(embed=emb)

    @commands.command(description="Upvote the Bot.", aliases=[])
    async def upvote(self,ctx):
        emb = discord.Embed( description=f" [Click here](https://top.gg/bot/850243448724127754/vote) to upvote me :))")
        emb.set_footer(icon_url=self.bot.user.avatar.url, text=f"UwU")
        await ctx.send(embed=emb)
    # @commands.command()
    # @commands.guild_only()
    # async def uptime(self, ctx):
    #     delta_uptime = datetime.utcnow() - self.bot.launch_time
    #     hours, remainder = divmod(int(delta_uptime.total_seconds()), 3600)
    #     minutes, seconds = divmod(remainder, 60)
    #     days, hours = divmod(hours, 24)
    #     await ctx.reply(f"{days}d, {hours}h, {minutes}m, {seconds}s")
    @commands.command(usage=f"`< user >`", description=f"Shows UserInfo with Roles.")
    @commands.guild_only()
    async def userinfo(self, ctx, member: discord.Member=None):
        '''Shows UserInfo with Roles'''
        if member is None:
            member = ctx.author
        created_at = member.created_at.strftime("%b %d, %Y")
        joined_at = member.joined_at.strftime("%b %d, %Y")
        rolesMention = [role.mention for role in member.roles]
        rolesMention.pop(0)
        rolesMention.reverse()
        noPermList =  ['Create Instant Invite',  'Add Reactions',  'Priority Speaker', 'Stream', 'Read Messages', 'Send Messages', 'Send TTS Messages', 'Embed Links', 'Attach Files', 'Read Message History', 'Connect', 'Speak',  'Use Voice Activation',  'Use Slash Commands', 'Request To Speak']
        permList = [p[0].replace('_',' ').replace('guild', 'server').title().replace('Tts','TTS') for p in member.guild_permissions if p[1]]
        
        for perm in noPermList:
            if perm in permList:
                permList.remove(perm)
        admin = False
        mod = False
        manager = False
        memberA=False
        if  "Administrator" in permList:
            admin = True
        elif "Manage Server" in permList:
            manager = True
        elif "Mute Members" in permList:
            mod = True
        else:
            memberA = True
        text=', '.join(permList)
        
        embed = discord.Embed(description=f"{member.mention} `[{member.id}]`", color=ctx.author.color)
        embed.add_field(name="`📆` `Created`", value=f"**- `{created_at}`**\n\`")
        embed.add_field(name="`📅` `Joined`", value=f"**- `{joined_at}\`**\n\n")
        if member.avatar.is_animated():
            embed.add_field(name="`📱` `Avatar`", value=f"[Animated]({member.avatar.url})", inline=False)
        if not member.avatar.is_animated():
            embed.add_field(name="`📱` `Avatar`", value=f"[Non-Animated]({member.avatar.url})", inline=False)
        embed.add_field(name=f"`ℹ` `Roles [{len(rolesMention)}]`", value=" ".join(rolesMention), inline=False)
        if not memberA:
            embed.add_field(name="`📱` `Key Permissions`", value=text, inline=False)
        if admin:
            embed.add_field(name="`📱` `Acknowledgements`", value="**- `Server Admin`**\n\n", inline=False)
        if manager:
            embed.add_field(name="`📱` `Acknowledgements`", value="**- `Server Manager`**\n\n", inline=False)
        if mod:
            embed.add_field(name="`📱` `Acknowledgements`", value="**- `Server Moderator`**\n\n", inline=False)
        embed.set_author(icon_url=ctx.author.avatar.url, name=ctx.author)
        embed.set_thumbnail(url=member.avatar.url)
        embed.set_footer(text="Team Tatsui ❤️")
        embed.timestamp =  datetime.utcnow()
        await ctx.send(embed=embed)

    


def setup(bot):
    bot.add_cog(Utility(bot))