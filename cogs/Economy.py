import discord  
import os
import praw
import random

testservers = [1066309324604977182, 701770264752422926, 1070322431203487785]

class Economy(discord.Cog):

    def __init__(self, bot):
        self.bot = bot

@discord.slash_command(guild_ids=testservers, name='bank', description='Still under development')
async def bank(self, ctx):
    await ctx.respond("You are broke")

def setup(bot):
    bot.add_cog(Economy(bot))  