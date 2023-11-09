import discord
from discord.ext import commands

class commands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def help(self, ctx, command_name: str = None):
        """Display help for all commands or a specific command."""
        if command_name is None:
            # Display help for all commands
            help_embed = discord.Embed(
                title="Command Help",
                color=discord.Color.blue()
            )
            for cog in self.bot.cogs:
                cog_commands = self.bot.get_cog(cog).get_commands()
                commands_str = "\n".join([f"**{cmd.name}**: {cmd.short_doc}" for cmd in cog_commands])
                help_embed.add_field(name=cog, value=commands_str[:1024], inline=False)

            help_embed.add_field(name="Repository", value="[GitHub Repository](https://github.com/yourusername/yourrepository)", inline=False)
            help_embed.set_footer(text="Use !help <command> for more details on a specific command.")
            await ctx.send(embed=help_embed)
        else:
            # Display help for a specific command
            command = self.bot.get_command(command_name)
            if command:
                command_embed = discord.Embed(
                    title=f"Command: {command.name}",
                    color=discord.Color.blue()
                )
                command_embed.add_field(name="Description", value=command.short_doc, inline=False)
                command_embed.add_field(name="Usage", value=f"!{command.name} {command.signature}", inline=False)

                await ctx.send(embed=command_embed)
            else:
                await ctx.send("Command not found.")

def setup(bot):
    bot.add_cog(commands(bot))
