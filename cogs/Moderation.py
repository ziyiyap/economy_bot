import discord  
import os
import random

testservers = [1066309324604977182, 701770264752422926, 1070322431203487785]

class Moderation(discord.Cog):

    def __init__(self, bot):
        self.bot = bot

    @discord.slash_command(guild_ids=testservers, name='purge', description='Purges the current chat')
    async def purge(self, ctx, limit: int):
        await ctx.channel.purge(limit=limit)
        await ctx.respond(f"I have deleted {limit} messages")

def setup(bot):
    bot.add_cog(Moderation(bot))   