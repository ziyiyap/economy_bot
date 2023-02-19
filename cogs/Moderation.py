import discord  
import os
import random

class Moderation(discord.Cog):

    def __init__(self, bot):
        self.bot = bot

    @discord.slash_command(name='purge', description='Purges the current chat')
    async def purge(self, ctx, limit: int):
        await ctx.channel.purge(limit=limit)
        await ctx.respond(f"I have deleted {limit} messages")
        command_payload = {
        "name": "purge",
        "description": "Purges the current chat"
        }
        await self.http.request(discord.Route("PUT",'/applications/1076536828422782987/commands'), json=command_payload)

def setup(bot):
    bot.add_cog(Moderation(bot))   