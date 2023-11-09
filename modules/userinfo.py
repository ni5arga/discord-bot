import discord
from discord.ext import commands
from datetime import datetime

class UserInfo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["userinfo", "user", "info"])
    """ Get an user's info """
    async def user_info(self, ctx, user: discord.Member = None):
        user = user or ctx.author

        embed = discord.Embed(color=user.color, timestamp=datetime.utcnow())
        embed.set_author(name=f"User Info - {user.name}", icon_url=user.avatar_url)
        embed.set_thumbnail(url=user.avatar_url)
        
        embed.add_field(name="User ID", value=user.id, inline=False)
        embed.add_field(name="Account Created", value=user.created_at.strftime("%Y-%m-%d %H:%M:%S"), inline=False)
        embed.add_field(name="Joined Server", value=user.joined_at.strftime("%Y-%m-%d %H:%M:%S"), inline=False)
        
        if user.nick:
            embed.add_field(name="Nickname", value=user.nick, inline=False)

        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(UserInfo(bot))
