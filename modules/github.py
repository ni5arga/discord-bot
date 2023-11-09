import discord
from discord.ext import commands
import requests

class GitHub(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def github(self, ctx, username):
        """Get GitHub user information."""
        try:
            user_url = f"https://api.github.com/users/{username}"
            user_headers = {"User-Agent": "Mozilla/5.0"}
            user_response = requests.get(user_url, headers=user_headers)

            if user_response.status_code == 200:
                user_data = user_response.json()

                embed = discord.Embed(color=discord.Color.green())
                embed.title = f"GitHub User: {user_data.get('login', 'Unknown')}"
                embed.add_field(name="Name", value=user_data.get('name', 'Not available'), inline=True)
                embed.add_field(name="Bio", value=user_data.get('bio', 'Not available'), inline=True)
                embed.add_field(name="Followers", value=user_data.get('followers', 0), inline=True)
                embed.add_field(name="Following", value=user_data.get('following', 0), inline=True)
                embed.add_field(name="Public Repositories", value=user_data.get('public_repos', 0), inline=True)
                embed.add_field(name="Created at", value=user_data.get('created_at', 'Unknown'), inline=True)
                embed.set_thumbnail(url=user_data.get('avatar_url', ''))

                await ctx.send(embed=embed)
            elif user_response.status_code == 404:
                await ctx.send(f"GitHub user '{username}' not found.")
            else:
                await ctx.send(f"Oops! Failed to fetch GitHub user information.")
        except Exception as e:
            await ctx.send(f"Error: {e}")

    @commands.command()
    async def repo(self, ctx, username, repo_name):
        """Get GitHub repository information."""
        try:
            repo_url = f"https://api.github.com/repos/{username}/{repo_name}"
            repo_headers = {"User-Agent": "Mozilla/5.0"}
            repo_response = requests.get(repo_url, headers=repo_headers)

            if repo_response.status_code == 200:
                repo_data = repo_response.json()

                embed = discord.Embed(color=discord.Color.blue())
                embed.title = f"GitHub Repository: {repo_data.get('full_name', 'Unknown')}"
                embed.add_field(name="Description", value=repo_data.get('description', 'Not available'), inline=False)
                embed.add_field(name="Language", value=repo_data.get('language', 'Not available'), inline=True)
                embed.add_field(name="Stars", value=repo_data.get('stargazers_count', 0), inline=True)
                embed.add_field(name="Forks", value=repo_data.get('forks_count', 0), inline=True)
                embed.add_field(name="Watchers", value=repo_data.get('watchers_count', 0), inline=True)
                embed.add_field(name="Open Issues", value=repo_data.get('open_issues_count', 0), inline=True)
                embed.add_field(name="Created at", value=repo_data.get('created_at', 'Unknown'), inline=True)
                embed.add_field(name="Last Updated", value=repo_data.get('updated_at', 'Unknown'), inline=True)
                embed.set_thumbnail(url=repo_data.get('owner', {}).get('avatar_url', ''))

                await ctx.send(embed=embed)
            elif repo_response.status_code == 404:
                await ctx.send(f"GitHub repository '{username}/{repo_name}' not found.")
            else:
                await ctx.send(f"Oops! Failed to fetch GitHub repository information.")
        except Exception as e:
            await ctx.send(f"Error: {e}")

def setup(bot):
    bot.add_cog(GitHub(bot))
