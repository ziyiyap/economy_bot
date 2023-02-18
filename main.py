import discord
import os
from dotenv import load_dotenv

load_dotenv()
intents = discord.Intents.all()
bot = discord.Bot(intents=intents)

@bot.event
async def on_ready():
    print('Bot is ready.')
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="/help"))

testservers = [1066309324604977182, 701770264752422926]

@bot.slash_command(guild_ids=testservers, name='ping', description='Checks the bot latency')
async def ping(ctx):
    embed = discord.Embed(title="Pong! 🏓", description=f"Latency is `{round(bot.latency*1000)}ms`",color=discord.Colour.random())
    await ctx.respond(embed=embed, ephemeral=True)

bot.run(os.environ['token'])