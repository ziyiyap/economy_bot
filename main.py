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

@bot.slash_command(guild_ids=testservers, name='load', description='Loads the selected cogs')
async def load(ctx, extension):
    bot.load_extension(f"cogs.{extension}")

@bot.slash_command(guild_ids=testservers, name='unload', description='Unloads the selected cogs')
async def unload(ctx, extension):
    bot.unload_extension(f"cogs.{extension}")

for filename in os.listdir("economy_bot\cogs"):
    if filename.endswith(".py"):
        bot.load_extension(f"cogs.{filename[:-3]}")  

bot.run(os.environ['token'])