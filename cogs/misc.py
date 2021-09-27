from discord.ext import commands
import discord
import yaml

class misc(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    with open('config.yaml', 'r') as config_file:
        config = yaml.load(config_file, Loader=yaml.BaseLoader)
    global channel_ids
    channel_ids = config['channel_ids']
    global role_ids
    role_ids = config['role_ids']

    @commands.command()
    async def alert(self, ctx, *args):
        if args:
            alert = ' '.join(args)
        else:
            alert = "A description was not provided."
        embed = discord.Embed(title="Moderator Alert", description=f"[Jump to message]({ctx.message.jump_url})\n{alert}", color=discord.Color.red())
        embed.add_field(name="Alert Author", value=ctx.message.author, inline=True)
        embed.add_field(name="User ID", value=ctx.message.author.id, inline=True)
        channel = self.bot.get_channel(int(channel_ids['modtalk']))
        await channel.send(f"<@&{role_ids['moderator']}> <@&{role_ids['trial_mod']}>", embed=embed)
        await ctx.send("The moderators have been alerted.")

    @commands.command()
    async def suggest(self, ctx, *args):
        if not args:
            await ctx.send("Please provide a suggestion.")
            return
        embed = discord.Embed(description=f"**Suggestion:** {' '.join(args)}", color=discord.Color.lighter_grey())
        embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
        embed.add_field(name="Status", value="Pending")
        channel = self.bot.get_channel(int(channel_ids['suggestions_list']))
        await channel.send(embed=embed)
        await ctx.message.add_reaction("✅")

    @commands.command()
    async def d(self, ctx):
        return

def setup(bot):
    bot.add_cog(misc(bot))
