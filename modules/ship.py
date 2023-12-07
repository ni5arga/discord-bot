import discord
from discord.ext import commands
import random

class Ship(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ship(self, ctx, user1: discord.Member = None, user2: discord.Member = None):
        """Ship two users and show their love percentage."""
        if user1 is None and user2 is None:
            member_list = ctx.guild.members
            user2 = random.choice(member_list)
            while user2 == ctx.author:
                user2 = random.choice(member_list)

        elif user1 is not None and user2 is None:
            user2 = ctx.author  
            
        percentage = random.randint(0, 100)
        ship_embed = discord.Embed(
            title=f"💖 Shipping {user1.display_name} and {user2.display_name}! 💖",
            color=discord.Color.magenta()
        )
        ship_embed.add_field(name="Love Percentage", value=f"{percentage}%")
        ship_embed.set_footer(text="UwU <3")

        await ctx.send(embed=ship_embed)

def setup(bot):
    bot.add_cog(Ship(bot))
