import discord
from discord.ext import commands
import os

class Sudo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.sudo_user_id = os.environ['SUDO_USER_ID']  

    def is_sudo_user(self, user):
        return user.id == self.sudo_user_id

    @commands.command()
    async def sudo(self, ctx, *, command):
        """Execute a command as the sudo user (only sudo users can use this)"""
        if not self.is_sudo_user(ctx.author):
            return await ctx.send("You do not have permission to use sudo.")

        context = await self.bot.get_context(ctx.message)
        context.message.content = f"!{command}"
        
        try:
            await self.bot.invoke(context)
        except commands.CommandError as e:
            await ctx.send(f"Error: {e}")

def setup(bot):
    bot.add_cog(Sudo(bot))
