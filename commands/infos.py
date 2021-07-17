from discord.ext import commands
import discord
import yaml

class infos(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ping(self, ctx: commands.Context):
        await ctx.send(f"Pong! {round(self.bot.latency * 1000)}ms")

    @commands.command()
    async def commands(self, ctx: commands.Context):
        with open('commands.yaml', 'r') as commands_file:
            commands = yaml.load(commands_file, Loader=yaml.BaseLoader)

        embed = discord.Embed(title="Command List", color=0x00a0a0)
        for command in commands:
            embed.add_field(name=command, value=commands[command], inline=False)
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(infos(bot))
