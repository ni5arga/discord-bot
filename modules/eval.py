import discord
from discord.ext import commands
import traceback
import os
from dotenv import load_dotenv

load_dotenv()

SUDO_USER_ID = int(os.environ.get("SUDO_USER_ID"))

class Eval(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="eval")
    async def _eval(self, ctx, *, code: str):
        """Evaluate python code (Available only to the developer)"""
        if ctx.author.id != SUDO_USER_ID:
            return

        code = code.strip("```").strip()

        try:
            result = eval(code)
            await ctx.send(f"```python\n{result}```")
        except Exception as e:
            await ctx.send(f"```python\nError: {e}```")
            traceback.print_exc()

def setup(bot):
    bot.add_cog(Eval(bot))
