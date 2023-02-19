import discord  
import random

class Economy(discord.Cog):

    def __init__(self, bot):
        self.bot = bot

    @discord.slash_command(name='bank', description='Checks your current balance in your bank')
    async def bank(self, ctx):
        await ctx.respond("You are broke")
        command_payload = {
            "name": "bank",
            "description": "Checks your current balance in your bank"
            }
        await self.http.request(discord.Route("PUT",'/applications/1076536828422782987/commands'), json=command_payload)

def setup(bot):
    bot.add_cog(Economy(bot))  