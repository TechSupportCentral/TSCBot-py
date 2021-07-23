from discord.ext import commands
import discord
import yaml

class infos(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ping(self, ctx):
        await ctx.send(f"Pong! {round(self.bot.latency * 1000)}ms")

    @commands.command()
    async def commands(self, ctx, arg=None):
        with open('commands.yaml', 'r') as commands_file:
            commands = yaml.load(commands_file, Loader=yaml.BaseLoader)

        if not arg:
            embed = discord.Embed(title="Command List", description="Commands come in categories. Here is a list of categories, run `!commands <category>` to see the commands in a certain category.", color=0x00a0a0)
            embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
            for category in commands:
                if not '_desc' in category:
                    embed.add_field(name=category + ':', value=commands[category + '_desc'], inline=True)
            await ctx.send(embed=embed)
        elif arg in commands:
            embed = discord.Embed(title="Command List", description=f"Commands in the {arg} category:", color=0x00a0a0)
            embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
            for command in commands[arg]:
                embed.add_field(name=command + ':', value=commands[arg].get(command), inline=False)
            await ctx.send(embed=embed)
        else:
            await ctx.send('Please send a valid category')

def setup(bot):
    bot.add_cog(infos(bot))
