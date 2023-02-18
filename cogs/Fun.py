import discord  
import os
import praw
import random

testservers = [1066309324604977182, 701770264752422926, 1070322431203487785]

reddit = praw.Reddit(client_id = "R-VC2Ng-g4enqyWQJf78pA",
                     client_secret = os.environ['reddit_secret'],
                     username = "ItzShqdos",
                     password = os.environ['reddit_password'],
                     user_agent = "shqdospraw")

class Fun(discord.Cog):

    def __init__(self, bot):
        self.bot = bot


    @discord.Cog.listener()
    async def on_ready(self):
        print("Cogs are loaded.")           

    @discord.slash_command(guild_ids=testservers, name='meme', description='Sends a meme')
    async def meme(self, ctx):
        subreddit = reddit.subreddit('memes')
        all_subs = []

        hot = subreddit.hot(limit = 50)

        for submission in hot:
            all_subs.append(submission)

        random_sub = random.choice(all_subs)
        name = random_sub.title
        url = random_sub.url
        embed = discord.Embed(title = name, color=discord.Colour.random())
        embed.set_image(url=url)
        await ctx.respond(embed=embed)


def setup(bot):
    bot.add_cog(Fun(bot))   