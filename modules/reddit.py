import discord
from discord.ext import commands
import requests
from datetime import datetime

class Reddit(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def reddit(self, ctx, subreddit_name):
        """Get a random post from the specified subreddit."""
        try:
            url = f"https://www.reddit.com/r/{subreddit_name}/random.json"
            headers = {"User-Agent": "Mozilla/5.0"}
            response = requests.get(url, headers=headers)

            if response.status_code == 200:
                data = response.json()
                post_data = data[0]["data"]["children"][0]["data"]
                post_title = post_data["title"]
                post_url = post_data["url"]
                post_author = post_data.get('author', 'Unknown')

                message = f"**Title:** {post_title}\n**Author:** {post_author}\n**Link:** {post_url}"
                await ctx.send(message)
            else:
                await ctx.send(f"Oops! Failed to fetch a random post from r/{subreddit_name}.")
        except Exception as e:
            await ctx.send(f"Error: {e}")

    @commands.command()
    async def reddituser(self, ctx, reddit_username):
        """Get information about a Reddit user."""
        try:
            url = f"https://www.reddit.com/user/{reddit_username}/about.json"
            headers = {"User-Agent": "Mozilla/5.0"}
            response = requests.get(url, headers=headers)

            if response.status_code == 200:
                data = response.json().get("data", {})
                user_name = data.get("name", 'Unknown')
                comment_karma = data.get("comment_karma", 0)
                link_karma = data.get("link_karma", 0)
                overall_karma = comment_karma + link_karma
                post_karma = comment_karma + link_karma
                created_utc = data.get("created_utc", 0)
                icon_img = data.get("icon_img", '')
                user_description = data.get("subreddit", {}).get("public_description", "No description available")

                # Convert created_utc to a readable date
                created_date = datetime.utcfromtimestamp(created_utc).strftime('%Y-%m-%d %H:%M:%S')

                profile_url = f"https://www.reddit.com/user/{reddit_username}"

                embed = discord.Embed(
                    title=f"Reddit User: {user_name}",
                    description=user_description,
                    color=discord.Color.blue()
                )

                # Set the user's icon_img as the thumbnail
                if icon_img:
                    embed.set_thumbnail(url=icon_img)

                # Add user information to the embed
                embed.add_field(name="Username", value=user_name, inline=True)
                embed.add_field(name="Comment Karma", value=comment_karma, inline=True)
                embed.add_field(name="Link Karma", value=link_karma, inline=True)
                embed.add_field(name="Overall Karma", value=overall_karma, inline=True)
                embed.add_field(name="Joining Date", value=created_date, inline=True)
                embed.add_field(name="Profile Link", value=f"[{reddit_username}]({profile_url})", inline=False)

                await ctx.send(embed=embed)
            else:
                await ctx.send(f"Oops! Failed to fetch information for the Reddit user {reddit_username}.")
        except Exception as e:
            await ctx.send(f"Error: {e}")

    @commands.command()
    async def subreddit(self, ctx, subreddit_name):
        """Get information about a subreddit."""
        try:
            url = f"https://www.reddit.com/r/{subreddit_name}/about.json"
            headers = {"User-Agent": "Mozilla/5.0"}
            response = requests.get(url, headers=headers)

            if response.status_code == 200:
                data = response.json().get("data", {})
                subreddit_name = data.get("display_name", 'Unknown')
                subscriber_count = data.get("subscribers", 0)
                active_user_count = data.get("active_user_count", 0)
                description = data.get("public_description", "No description available")
                created_utc = data.get("created_utc", 0)

                # Convert created_utc to a readable date
                created_date = datetime.utcfromtimestamp(created_utc).strftime('%Y-%m-%d %H:%M:%S')

                subreddit_url = f"https://www.reddit.com/r/{subreddit_name}"

                message = f"**Subreddit Name:** {subreddit_name}\n**Total Member Count (Subscribers):** {subscriber_count}\n**Online Users:** {active_user_count}\n**Description:** {description}\n**Creation Date:** {created_date}\n[Subreddit Link]({subreddit_url})"
                
                embed = discord.Embed(
                    title=f"Subreddit: {subreddit_name}",
                    description=message,
                    color=discord.Color.green()
                )

                await ctx.send(embed=embed)
            else:
                await ctx.send(f"Oops! Failed to fetch information for the subreddit r/{subreddit_name}.")
        except Exception as e:
            await ctx.send(f"Error: {e}")

def setup(bot):
    bot.add_cog(Reddit(bot))
