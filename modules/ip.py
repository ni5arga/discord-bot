import discord
from discord.ext import commands
import requests

class IP(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ip(self, ctx, ip_address=None):
        """Get information about an IP address."""
        try:
            if ip_address:
                url = f"http://ip-api.com/json/{ip_address}"
            else:
                url = "http://ip-api.com/json/"

            response = requests.get(url)

            if response.status_code == 200:
                data = response.json()

                embed = discord.Embed(color=discord.Color.purple())
                embed.title = "IP Information"
                embed.add_field(name="IP Address", value=data.get('query', 'Unknown'), inline=True)
                embed.add_field(name="Country", value=data.get('country', 'Unknown'), inline=True)
                embed.add_field(name="Country Code", value=data.get('countryCode', 'Unknown'), inline=True)
                embed.add_field(name="Region", value=data.get('region', 'Unknown'), inline=True)
                embed.add_field(name="Region Name", value=data.get('regionName', 'Unknown'), inline=True)
                embed.add_field(name="City", value=data.get('city', 'Unknown'), inline=True)
                embed.add_field(name="Zip", value=data.get('zip', 'Unknown'), inline=True)
                embed.add_field(name="Latitude", value=data.get('lat', 'Unknown'), inline=True)
                embed.add_field(name="Longitude", value=data.get('lon', 'Unknown'), inline=True)
                embed.add_field(name="Timezone", value=data.get('timezone', 'Unknown'), inline=True)
                embed.add_field(name="ISP", value=data.get('isp', 'Unknown'), inline=True)
                embed.add_field(name="Organization", value=data.get('org', 'Unknown'), inline=True)
                embed.add_field(name="AS", value=data.get('as', 'Unknown'), inline=True)

                await ctx.send(embed=embed)
            else:
                await ctx.send("Error fetching IP information.")
        except Exception as e:
            await ctx.send(f"Error: {e}")

def setup(bot):
    bot.add_cog(IP(bot))
