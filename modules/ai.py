import discord
from discord.ext import commands
import requests
import os

BRAINSHOP_URL = os.environ.get('BRAINSHOP_URL')

class AI(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.brainshop_api_url = BRAINSHOP_URL

    @commands.command()
    async def ai(self, ctx, *, question):
        """Ask a question to the AI"""
        try:
            if self.brainshop_api_url is None:
                await ctx.send("BRAINSHOP_URL environment variable not set.")
                return

            params = {
                'uid': ctx.author.id,
                'msg': question,
            }

            response = requests.get(self.brainshop_api_url, params=params)

            if response.status_code == 200:
                data = response.json()
                answer = data.get('cnt', 'No response from AI.')
                await ctx.send(answer)
            else:
                await ctx.send("Error fetching response from AI.")
        except requests.exceptions.RequestException as e:
            await ctx.send(f"Error making request to AI: {e}")

def setup(bot):
    bot.add_cog(AI(bot))
