import discord
import typing
import wavelink
import datetime
import asyncio

testservers = [1066309324604977182, 701770264752422926, 1070322431203487785]

class Music(discord.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.queue = []
        self.position = 0
        self.repeat = False
        self.repeatMode = "NONE"
        self.playingTextChannel = 0
        bot.loop.create_task(self.create_nodes())

    async def create_nodes(self):
        await self.bot.wait_until_ready()
        await wavelink.NodePool.create_node(bot=self.bot, host="127.0.0.1", port="2333", password="youshallnotpass", region="asia")

    async def on_wavelink_node_ready(self, node: wavelink.Node):
        print(f"Node {node.identifier} is ready.")

    @discord.Cog.listener()
    async def on_wavelink_track_start(self, player:wavelink.Player, track):
        try:
            self.queue.pop(0)
        except:
            pass

    @discord.Cog.listener()
    async def on_wavelink_track_end(self, player: wavelink.Player, track, reason):
        if str(reason) == "FINISHED":
            if not len(self.queue) == 0:
                next_track: wavelink.Track = self.queue[0]
                channel = self.bot.get_channel(self.playingTextChannel)

                try:
                    await player.play(next_track)
                except:
                    await channel.send(embed=discord.Embed(title=f"Something went wrong while playing `{next_track.title}` ", color=discord.Colour.red()))
                await channel.send(embed=discord.Embed(title=f"Now playing: {next_track.title}", color=discord.Colour.green()))
            else:
                pass
        else:
            print(reason)


    @discord.slash_command(guild_ids=testservers, name='join', description="Joins the channel you're in")
    async def join(self, ctx, channel: typing.Optional[discord.VoiceChannel]):
        if channel is None:
            channel = ctx.author.voice.channel

        node = wavelink.NodePool.get_node()
        player = node.get_player(ctx.guild)

        if player is not None:
            if player.is_connected():
                return await ctx.respond("I am already in a voice channel!")

        await channel.connect(cls=wavelink.Player)
        embed = discord.Embed(title=f"Connected to `#{channel.name}`.", color=discord.Colour.brand_green()) 
        await ctx.respond(embed=embed)

    @discord.slash_command(guild_ids=testservers, name='disconnect', description="Leaves the channel you're in")
    async def disconnect(self, ctx):
        node = wavelink.NodePool.get_node()
        player = node.get_player(ctx.guild)

        if player is None:
            if player.is_connected():
                return await ctx.respond("I am not connected to any voice channel.")

        await player.disconnect()
        embed = discord.Embed(title=f"Disconnected.", color=discord.Colour.red()) 
        await ctx.respond(embed=embed)

    @discord.slash_command(guild_ids=testservers, name='play', description="Play's a song")
    async def play(self, ctx, *, search: str):
        try:
            search = await wavelink.YouTubeTrack.search(query=search, return_first=True)
        except:
            return await ctx.respond(embed=discord.Embed(title="Something went wrong while searching for this track.", color=discord.Colour.red()))

        node = wavelink.NodePool.get_node()
        player = node.get_player(ctx.guild)
        if not ctx.voice_client:
            vc: wavelink.Player = await ctx.author.voice.channel.connect(cls=wavelink.Player)
        else:
            vc: wavelink.Player = ctx.voice_client
        if not vc.is_playing() and vc.is_connected():
            try:
                await vc.play(search)
                embed = discord.Embed(title=f"Now Playing: `{search}`", color=discord.Colour.yellow())
                await ctx.respond(embed=embed)
            except:
                return await ctx.respond(embed=discord.Embed(title="Something went wrong while playing this track", color=discord.Colour.red()))
        else:
            self.queue.append(search)

            embed = discord.Embed(title=f"Added `{search}` to the queue", color=discord.Colour.green())
            await ctx.respond(embed=embed) 
            
        vc.ctx = ctx
        setattr(vc, " loop", False)


    @discord.slash_command(guild_ids=testservers, name='stop', description="Stops a song")
    async def stop(self, ctx):
        node = wavelink.NodePool.get_node()
        player = node.get_player(ctx.guild)

        if player is None:
            if player.is_connected():
                return await ctx.respond("I am not connected to any voice channel.")
        self.queue.clear()

        if player.is_playing:
            await player.stop()
            embed = discord.Embed(title='Playback stopped', color=discord.Colour.red())
            return await ctx.respond(embed=embed)
        else:
            return await ctx.respond('Nothing is playing!')

    @discord.slash_command(guild_ids=testservers, name='pause', description="Pauses a song")
    async def pause(self, ctx):
        node = wavelink.NodePool.get_node()
        player = node.get_player(ctx.guild)

        if player is None:
            return await ctx.respond("I am not connected to any voice channel.")

        if not player.is_paused():
            if player.is_playing():
                await player.pause()
                embed = discord.Embed(title='Playback Paused', color=discord.Colour.orange())
                return await ctx.respond(embed=embed)
            else:
                return await ctx.respond('Nothing is playing!')
        else:
            return await ctx.respond('Playback is already paused.')
        
    @discord.slash_command(guild_ids=testservers, name='resume', description='Resumes a song')
    async def resume(self, ctx):
        node = wavelink.NodePool.get_node()
        player = node.get_player(ctx.guild)

        if player is None:
                return await ctx.respond("I am not connected to any voice channel.")

        if player.is_paused():
            await player.resume()
            embed = discord.Embed(title='Playback resumed', color=discord.Colour.green())
            return await ctx.respond(embed=embed)
        else:
            if not len(self.queue) == 0:
                return await ctx.respond('Playback is not paused.')

    @discord.slash_command(guild_ids=testservers, name='volume', description='Changes the volume of the song')
    async def volume(self, ctx, to: int):
        if to > 100:
            return await ctx.respond('Volume should be between 0 and 100')
        elif to < 1:
            return await ctx.respond('Volume should be between 0 and 100')


        node = wavelink.NodePool.get_node()
        player = node.get_player(ctx.guild)

        await player.set_volume(to)
        embed = discord.Embed(title=f'Changed volume to {to}', color=discord.Colour.yellow())
        await ctx.respond(embed=embed)

    @discord.slash_command(guild_ids=testservers, name='loop', description='Loops the song')
    async def loop(self, ctx):
        node = wavelink.NodePool.get_node()
        player = node.get_player(ctx.guild)
        if player is None:
            return await ctx.respond("I am not connected to any voice channel.")
        else:
            vc: wavelink.Player = ctx.voice_client
        try:
            vc.loop ^= True
        except Exception:
            setattr(vc, "loop", False)

        if vc.loop:
            loopembed = discord.Embed(title="Loop is now enabled", color=discord.Colour.green())
            return await ctx.respond(embed=loopembed)
        else:
            unloopembed = discord.Embed(title="Loop is now disabled", color=discord.Colour.red())
            return await ctx.respond(embed=unloopembed)

    @discord.slash_command(guild_ids=testservers, name="queue", description="Show's the queue")
    async def queue(self, ctx, search=None):
        node = wavelink.NodePool.get_node()
        player = node.get_player(ctx.guild)
        
        if search is None:
            if not len(self.queue) == 0:
                mbed = discord.Embed(
                    title=f"Now playing: `{player.track}`" if player.is_playing else "Queue: ",
                    description = "\n".join(f"**{i+1}. {track}**" for i, track in enumerate(self.queue[:10])) if not player.is_playing else "**Queue: **\n"+"\n".join(f"**{i+1}. `{track}`**" for i, track in enumerate(self.queue[:10])),
                    color=discord.Color.green())

                return await ctx.respond(embed=mbed)
            else:
                return await ctx.respond(embed=discord.Embed(title="The queue is empty", color=discord.Color.red()))
        else:
            try:
                track = await wavelink.YoutubeTrack.search(query=search, return_first=True)
            except:
                return await ctx.respond(embed=discord.Embed(title="Something went wrong while searching for this track", color=discord.Color.red()))
            
            if not ctx.voice_client:
                vc: wavelink.Player = await ctx.author.voice.channel(cls=wavelink.Player)
                await player.connect(ctx.author.voice.channel)
            else:
                vc: wavelink.Player = ctx.voice_client
            
            if not vc.isp_playing():
                try:
                    await vc.play(track)
                except:
                    return await ctx.respond(embed=discord.Embed(title="Something went wrong while playing this track", color=discord.Color.red()))
            else:
                self.queue.append(track)
            
            await ctx.respond(embed=discord.Embed(title=f"Added {track.title} to the queue", color=discord.Color.green()))

    @discord.slash_command(guild_ids=testservers, name="nowplaying", description="Show's the song that is currently playing")
    async def nowplaying(self, ctx):
        node = wavelink.NodePool.get_node()
        player = node.get_player(ctx.guild)

        if player is None:
            return await ctx.respond("I am not connected to any voice channel.")
        else:
            vc: wavelink.Player = ctx.voice_client

        embed = discord.Embed(title=f"Now Playing: {vc.track.title}", description=f'Artist: {vc.track.author}', color=discord.Colour.random())
        embed.add_field(name="Duration", value=f"{str(datetime.timedelta(seconds=vc.track.length))}")
        embed.add_field(name="Extra info", value=f"Song URL: [Click Me]({str(vc.track.uri)})")
        return await ctx.respond(embed=embed)

    @discord.slash_command(guild_ids=testservers, name="skip", description="Skips the current song")
    async def skip(self, ctx):
        node = wavelink.NodePool.get_node()
        player = node.get_player(ctx.guild)

        if not len(self.queue) == 0:
            next_track: wavelink.Track = self.queue[0]
            try:
                await player.play(next_track)
            except:
                return await ctx.respond(embed=discord.Embed(title="Something went wrong while playing this track", color=discord.Color.red()))

            await ctx.respond(embed=discord.Embed(title=f"Skipped to `{next_track.title}`", color=discord.Color.green()))
        else:
            await ctx.respond("The queue is empty")

def setup(bot):
    bot.add_cog(Music(bot)) 