import discord
from discord.ext import commands
import os
from dotenv import load_dotenv  
load_dotenv()
# Module probably contains some bugs, wil fix in the future.

class Logging(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def log_action(self, ctx, action_type, target, reason=None):
        log_channel_id = os.environ['LOGGING_CHANNEL_ID']  # Logging Channel ID
        log_channel = ctx.guild.get_channel(log_channel_id)

        if log_channel:
            embed = discord.Embed(
                title=f"Moderation Action: {action_type}",
                color=discord.Color.dark_red()
            )
            embed.add_field(name="Moderator", value=ctx.author.display_name)
            embed.add_field(name="Target", value=target.display_name)
            if reason:
                embed.add_field(name="Reason", value=reason, inline=False)

            await log_channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        await self.log_action(member, "Member Removed", member)

    @commands.Cog.listener()
    async def on_member_ban(self, guild, user):
        await self.log_action(guild, "Member Banned", user)

    @commands.Cog.listener()
    async def on_member_unban(self, guild, user):
        await self.log_action(guild, "Member Unbanned", user)

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        await self.log_action(message, "Message Deleted", message.author)

def setup(bot):
   bot.add_cog(Logging(bot))
