import discord
from discord.ext import commands
import requests
# may contain some bugs
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

def setup(bot):
    bot.add_cog(Reddit(bot))
