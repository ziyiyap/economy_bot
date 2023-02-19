import discord
import os
import sys
from discord.ui import Select, View
from dotenv import load_dotenv

load_dotenv()
intents = discord.Intents.all()
bot = discord.Bot(intents=intents)
token = os.getenv('TOKEN') 

@bot.event
async def on_ready():
    print('Bot is ready.')
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="/help"))

@bot.slash_command(name="help", description="Shows all the commands of the bot")
async def help(ctx):
    select = Select(placeholder = "Choose an option.", options=[
        discord.SelectOption(label="Fun", emoji="🤪", description="Shows all the commands in the Fun section"),
        discord.SelectOption(label="Music", emoji="🎵", description="Shows all the commands in the Music section"),
        discord.SelectOption(label="Economy", emoji="💰", description="Shows all the commands in the Economy section"),
        discord.SelectOption(label="Moderation", emoji="🛡️", description="Shows all the commands in the Moderation section"),
    ])
    async def my_callback(interaction):
        if select.values[0] == "Fun":
            await interaction.response.send_message("https://tenor.com/view/clash-royale-gif-5535732")
        elif select.values[0] == "Music":
            await interaction.response.send_message("https://tenor.com/view/clash-royale-clashroyale-angry-gif-5302587")
        elif select.values[0] == "Economy":
            await interaction.response.send_message("https://tenor.com/view/thumbs-up-youre-awesome-good-job-gif-7939553")
        elif select.values[0] == "Moderation":
            await interaction.response.send_message("https://tenor.com/view/clash-royale-cry-tears-king-crown-gif-5302586")
    select.callback = my_callback
    view = View()
    view.add_item(select)
    await ctx.respond("Help command", view=view, ephemeral=True)
    command_payload = {
    "name": "help",
    "description": "Shows all the commands of the bot"
}
    await bot.http.request(discord.Route("PUT",'/applications/1076536828422782987/commands'), json=command_payload)

@bot.slash_command(name='ping', description='Checks the bot latency')
async def ping(ctx):
    embed = discord.Embed(title="Pong! 🏓", description=f"Latency is `{round(bot.latency*1000)}ms`",color=discord.Colour.random())
    await ctx.respond(embed=embed, ephemeral=True)
    command_payload = {
    "name": "ping",
    "description": "Checks the bot latency"
}
    await bot.http.request(discord.Route("PUT",'/applications/1076536828422782987/commands'), json=command_payload)

@bot.slash_command(name='load', description='Loads the selected cogs')
async def load(ctx, extension):
    bot.load_extension(f"cogs.{extension}")
    command_payload = {
    "name": "load",
    "description": "Loads the selected cogs"
}
    await bot.http.request(discord.Route("PUT",'/applications/1076536828422782987/commands'), json=command_payload)

@bot.slash_command(name='unload', description='Unloads the selected cogs')
async def unload(ctx, extension):
    bot.unload_extension(f"cogs.{extension}")
    command_payload = {
    "name": "unload",
    "description": "Unloads the selected cogs"
}
    await bot.http.request(discord.Route("PUT",'/applications/1076536828422782987/commands'), json=command_payload)

for filename in os.listdir("economy_bot\cogs"):
    if filename.endswith(".py"):
        bot.load_extension(f"cogs.{filename[:-3]}")  

bot.run(token)
