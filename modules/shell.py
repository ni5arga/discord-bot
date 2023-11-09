import discord
from discord.ext import commands
import subprocess
import os

class Shell(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.allowed_user_id = os.environ['SUDO_USER_ID']

    def is_allowed_user(self, user_id):
        return user_id == self.allowed_user_id

    @commands.command()
    async def shell(self, ctx, *, command):
        """Run a shell command (available to developer only)."""
        if not self.is_allowed_user(ctx.author.id):
            await ctx.send("You are not authorized to use this command.")
            return

        try:
            result = subprocess.check_output(command, shell=True, text=True)
            await ctx.send(f"Command executed successfully:\n```\n{result}\n```")
        except Exception as e:
            await ctx.send(f"Error executing command: {e}")

def setup(bot):
    bot.add_cog(Shell(bot))
