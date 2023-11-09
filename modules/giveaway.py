import discord
from discord.ext import commands, tasks
import random
import asyncio
import datetime

class Giveaway(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.giveaways = []

    @commands.command()
    async def startgiveaway(self, ctx, duration: int, winners: int, *, prize: str):
        """Start a giveaway."""
        end_time = datetime.datetime.utcnow() + datetime.timedelta(seconds=duration)

        embed = discord.Embed(
            title="🎉 Giveaway",
            description=f"React with 🎉 to enter!\nPrize: {prize}\nEnds: {end_time.strftime('%Y-%m-%d %H:%M:%S')}",
            color=discord.Color.gold()
        )
        embed.set_footer(text=f"{winners} winner(s)")

        message = await ctx.send(embed=embed)
        await message.add_reaction("🎉")

        self.giveaways.append({
            "message_id": message.id,
            "channel_id": ctx.channel.id,
            "end_time": end_time,
            "winners": winners,
            "prize": prize,
            "participants": set()
        })

        self.check_giveaways.start()

    @commands.command()
    async def endgiveaway(self, ctx, message_id: int):
        """End a giveaway and pick winners."""
        for giveaway in self.giveaways:
            if giveaway["message_id"] == message_id and giveaway["channel_id"] == ctx.channel.id:
                winners = random.sample(giveaway["participants"], k=giveaway["winners"])
                winner_mentions = [f"<@{winner}>" for winner in winners]

                await ctx.send(f"🎉 Congratulations {', '.join(winner_mentions)}! You won the {giveaway['prize']} giveaway!")

                self.giveaways.remove(giveaway)
                self.check_giveaways.stop()
                break
        else:
            await ctx.send("No active giveaway with that message ID.")

    @tasks.loop(seconds=10)
    async def checkgiveaways(self):
        """Check active giveaways and pick winners when they end."""
        now = datetime.datetime.utcnow()

        for giveaway in self.giveaways:
            if now >= giveaway["end_time"]:
                winners = random.sample(giveaway["participants"], k=giveaway["winners"])
                winner_mentions = [f"<@{winner}>" for winner in winners]

                channel = self.bot.get_channel(giveaway["channel_id"])
                message = await channel.fetch_message(giveaway["message_id"])

                await channel.send(f"🎉 Congratulations {', '.join(winner_mentions)}! You won the {giveaway['prize']} giveaway!")

                self.giveaways.remove(giveaway)
                break

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        """Add participants to the giveaway."""
        for giveaway in self.giveaways:
            if reaction.message.id == giveaway["message_id"] and reaction.emoji == "🎉":
                giveaway["participants"].add(user.id)
                break

def setup(bot):
    bot.add_cog(Giveaway(bot))
