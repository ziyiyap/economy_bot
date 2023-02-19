import discord  
import os
import random
import aiohttp

testservers = [1066309324604977182]

class ChatGPT(discord.Cog):

    def __init__(self, bot):
        self.bot = bot

    @discord.slash_command(guild_ids=testservers, name='gpt', description='Ask a question to the AI!')
    async def gpt(self, ctx, *, prompt:str):
        async with aiohttp.ClientSession() as session:
            payload = {
                "model": "text-davinci-003",
                "prompt": prompt,
                "temperature": 0.9,
                "max_tokens": 50,
                "presence_penalty": 0,
                "frequency_penalty": 0,
                "best_of": 1,
            }
            headers = {"Authorization": f"Bearer {os.environ['chatgpt_api_key']}"}
            async with session.post("https://api.openai.com/v1/completions", json=payload, headers=headers) as resp:
                response = await resp.json()
                embed = discord.Embed(title="ChatGPT's Response:", description=response["choices"][0]["text"])
                await ctx.respond(embed=embed)


def setup(bot):
    bot.add_cog(ChatGPT(bot))  