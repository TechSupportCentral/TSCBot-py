from discord.ext import commands
import discord
import yaml

class infos(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def alert(self, ctx, *args):
        with open('config.yaml', 'r') as config_file:
            config = yaml.load(config_file, Loader=yaml.BaseLoader)
        channel_ids = config['channel_ids']
        role_ids = config['role_ids']

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

def setup(bot):
    bot.add_cog(misc(bot))
