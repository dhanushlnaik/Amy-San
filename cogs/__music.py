import discord
from requests_toolbelt import ImproperBodyPartContentException
import asyncio
from discord.ext import commands
import pafy
import youtube_dl

class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.song_queue = {}

        self.setup()

        def setup(Self):
            for guild in self.bot.guilds:
                self.song_queue[guild.id] = []

        async def check_queue(self, ctx):
            if len(self.song_queue[ctx.guild.id]) > 0:
                ctx.voice_client.stop()
                await self.play_song(ctx, self.song_queue[ctx.guild.id][0])
                self.song_queue[ctx.guild.id].pop()

        async def search_song(self, amount, song, get_url=False):
            info = await self.bot.loop.run_in_executor(None, lambda: youtube_dl.YoutubeDL({"format": "bestaudio", "quiet": True}).extract_info(f'ytsearch{amount}:{song}'), download=False, ie_key="YoutubeSearch")
            if len(info["entries"]) == 0: return None

            return [entry["webpage_url"] for entry in info["entries"]] if get_url else info

        async def play_song(self, ctx, song):
            url = pafy.new(song).getbestaudio().url
            ctx.voice_client.play(discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(url)), after=)

        @commands.command()
        async def join(self,ctx):
            voice_channel = ctx.author.voice.channel
            if voice_channel is None:
                return await ctx.send("Connect to a voice channel!")
            if ctx.voice_client is not None:
                await ctx.voice_client.disconnect()
            
            await ctx.author.voice.channel.connect()
    
        @commands.command()
        async def dc(self,ctx):
            if ctx.voice_client is not None:
                return await ctx.voice_client.disconnect()
            
        


def setup(bot):
    bot.add_cog(Music(bot))