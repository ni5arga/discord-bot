import discord
from discord.ext import commands
import pyowm
import os

from dotenv import load_dotenv  
load_dotenv()

OWM_API_KEY = os.environ[OWM_API_KEY]

class Weather(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.owm = pyowm.OWM(OWM_API_KEY)

    @commands.command()
    async def weather(self, ctx, *, location):
        """Get current weather information. Usage- !weather location"""
        try:
            observation = self.owm.weather_at_place(location)
            w = observation.get_weather()

            temperature = w.get_temperature('celsius')['temp']
            status = w.get_status()
            humidity = w.get_humidity()
            wind_speed = w.get_wind()['speed']

            embed = discord.Embed(color=discord.Color.blue())
            embed.title = f"Weather in {location}"
            embed.add_field(name="Temperature", value=f"{temperature}°C", inline=True)
            embed.add_field(name="Status", value=status.capitalize(), inline=True)
            embed.add_field(name="Humidity", value=f"{humidity}%", inline=True)
            embed.add_field(name="Wind Speed", value=f"{wind_speed} m/s", inline=True)

            await ctx.send(embed=embed)
        except Exception as e:
            await ctx.send(f"Error: {e}")

def setup(bot):
    bot.add_cog(Weather(bot))
