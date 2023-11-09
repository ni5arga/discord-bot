import discord
from discord.ext import commands
import asyncio

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def cog_check(self, ctx):
        return ctx.guild is not None

    async def get_member(self, ctx, user_input):
        try:
            # Check if the user input is a mention
            if user_input.startswith('<@') and user_input.endswith('>'):
                user_id = user_input[2:-1]
            else:
                user_id = user_input

            member = await ctx.guild.fetch_member(int(user_id))
            return member
        except discord.NotFound:
            return None
        except ValueError:
            return None

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def kick(self, ctx, user, *, reason=None):
        """Kick a user. Usage: !kick @user reason or !kick user_id reason"""
        try:
            member = await self.get_member(ctx, user)

            if member is not None:
                await member.kick(reason=reason)
                await ctx.send(f'Kicked {member.mention} for {reason}')
            else:
                await ctx.send("User not found.")
        except discord.Forbidden:
            await ctx.send("I don't have permission to kick members.")

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, user, *, reason=None):
        """Ban a user. Usage: !ban @user reason or !ban user_id reason"""
        try:
            member = await self.get_member(ctx, user)

            if member is not None:
                await member.ban(reason=reason)
                await ctx.send(f'Banned {member.mention} for {reason}')
            else:
                await ctx.send("User not found.")
        except discord.Forbidden:
            await ctx.send("I don't have permission to ban members or the user you want to ban is more/as powerful as me.")

    @commands.command()
    @commands.has_permissions(manage_roles=True)
    async def mute(self, ctx, member: discord.Member, duration: int = 0, *, reason=""):
        """Timeout/Mute a member. You need to specify duration in minutes like !mute @user 20"""
        try:
            if duration <= 0:
                # If duration is not mentioned or 0, permamute the user
                await self.apply_mute_role(ctx, member, reason)
            else:
                await self.apply_mute_role(ctx, member, reason)

                # Remove the Muted role after the specified duration
                await asyncio.sleep(duration * 60)
                await self.remove_mute_role(ctx, member, "Timeout expired")

        except commands.CheckFailure:
            await ctx.send("You do not have the required permission to use this command.")
        except Exception as e:
            await ctx.send(f"Error: {e}")

    @commands.command()
    @commands.has_permissions(manage_roles=True)
    async def unmute(self, ctx, member: discord.Member, *, reason=""):
        """Untimeout/Unmute a member"""
        try:
            await self.remove_mute_role(ctx, member, reason)
        except commands.CheckFailure:
            await ctx.send("You do not have the required permission to use this command.")
        except Exception as e:
            await ctx.send(f"Error: {e}")

    async def apply_mute_role(self, ctx, member, reason):
        muted_role = discord.utils.get(ctx.guild.roles, name="Muted")

        if not muted_role:
            # Create the Muted role if it doesn't exist
            muted_role = await ctx.guild.create_role(name="Muted", reason="Timeout command")
            
            # Apply the role permissions (adjust as needed)
            permissions = discord.PermissionOverwrite(send_messages=False, speak=False)
            for channel in ctx.guild.channels:
                await channel.set_permissions(muted_role, overwrite=permissions)

        await member.add_roles(muted_role, reason=f"Muted: {reason}")
        await ctx.send(f"{member.mention} has been muted. Reason: {reason}")

    async def remove_mute_role(self, ctx, member, reason):
        muted_role = discord.utils.get(ctx.guild.roles, name="Muted")

        if muted_role in member.roles:
            await member.remove_roles(muted_role, reason=f"Unmuted: {reason}")
            await ctx.send(f"{member.mention} has been unmuted. Reason: {reason}")
        else:
            await ctx.send(f"{member.mention} is not currently muted.")

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, user_id: int, *, reason=""):
        """Unban a user by user ID."""
        try:
            banned_users = await ctx.guild.bans()
            target_user = discord.utils.get(banned_users, user__id=user_id)

            if target_user:
                await ctx.guild.unban(target_user.user, reason=f"Unbanned: {reason}")
                await ctx.send(f"User with ID {user_id} has been unbanned. Reason: {reason}")
            else:
                await ctx.send("User not found in the ban list.")

        except commands.CheckFailure:
            await ctx.send("You do not have the required permission to use this command.")
        except Exception as e:
            await ctx.send(f"Error: {e}")

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def warn(self, ctx, user, *, reason=None):
        """Warn a user. 
        Usage : !warn @user reason or !warn user_id reason"""
        member = await self.get_member(ctx, user)

        if member is not None:
            try:
                await member.send(f"You've been warned in {ctx.guild.name} for: {reason}")
                await ctx.send(f'{member.mention} has been warned for: {reason}')
            except discord.Forbidden:
                await ctx.send("I couldn't send a DM to the user. They might have DMs disabled.")
        else:
            await ctx.send("User not found.")

    @kick.error
    @ban.error
    async def moderation_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("You don't have the required permissions to use this command.")
        elif isinstance(error, commands.BadArgument):
            await ctx.send("Invalid user provided.")
        else:
            await ctx.send(f"An error occurred: {error}")


    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def purge(self, ctx, limit: int):
        """Delete a specified number of messages in the current channel."""
        try:
            await ctx.channel.purge(limit=limit + 1)  # +1 to include the purge command message
            await ctx.send(f"Deleted {limit} messages.", delete_after=5)
        except discord.Forbidden:
            await ctx.send("I don't have permission to delete messages.")
        except discord.HTTPException:
            await ctx.send("An error occurred while deleting messages.")

    @purge.error
    async def purge_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("You don't have the required permissions to use this command.")
        else:
            await ctx.send(f"An error occurred: {error}")

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def delete(self, ctx, message_id: int):
        """Delete a specific message by its ID in the current channel."""
        try:
            message = await ctx.channel.fetch_message(message_id)
            await message.delete()
            await ctx.send("Message deleted.", delete_after=5)
        except discord.NotFound:
            await ctx.send("Message not found.")
        except discord.Forbidden:
            await ctx.send("I don't have permission to delete the message.")
        except discord.HTTPException:
            await ctx.send("An error occurred while deleting the message.")

    @delete.error
    async def delete_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("You don't have the required permissions to use this command.")
        else:
            await ctx.send(f"An error occurred: {error}")         

def setup(bot):
    bot.add_cog(Moderation(bot))
