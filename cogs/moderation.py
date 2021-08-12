from discord.ext import commands
import discord
import yaml

class moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    with open('config.yaml', 'r') as config_file:
        config = yaml.load(config_file, Loader=yaml.BaseLoader)
    global role_ids
    role_ids = config['role_ids']
    global channel_ids
    channel_ids = config['channel_ids']

    @commands.command()
    async def purge(self, ctx, arg=None):
        guild = ctx.message.guild
        mod_role = guild.get_role(int(role_ids['moderator']))
        if not mod_role in ctx.message.author.roles:
            await ctx.send("You do not have permission to run this command.")
            return

        if not arg:
            await ctx.send("Please mention a number of messages to purge.")
            return
        elif arg.isdigit():
            arg = int(arg)
        else:
            await ctx.send("Not a valid number of messages")
            return

        if arg > 100:
            await ctx.send("You can only delete 100 or fewer messages at once.")
            return

        await ctx.channel.purge(limit=arg)
        embed=discord.Embed(title=str(arg) + " Messages Deleted", color=0x00a0a0)
        embed.set_thumbnail(url=ctx.message.author.avatar_url)
        embed.add_field(name="Deleted by", value=ctx.message.author, inline=True)
        embed.add_field(name="In channel", value=ctx.message.channel.mention, inline=True)
        channel = self.bot.get_channel(int(channel_ids['staff_logs']))
        await channel.send(embed=embed)

    @commands.command()
    async def userinfo(self, ctx, arg=None):
        guild = ctx.message.guild
        mod_role = guild.get_role(int(role_ids['moderator']))
        if not mod_role in ctx.message.author.roles:
            await ctx.send("You do not have permission to run this command.")
            return

        if not arg:
            id = ctx.message.author.id

        elif "<@" in arg:
            id = arg
            id = id.replace("<", "")
            id = id.replace(">", "")
            id = id.replace("@", "")
            id = id.replace("!", "")
            id = int(id)

        elif arg.isdigit():
            id = int(arg)

        else:
            await ctx.send("Users have to be in the form of an ID or a mention.")
            return

        if guild.get_member(id) is None:
            await ctx.send("User is not in the server.")
            return

        member = guild.get_member(id)
        embed=discord.Embed(title=member, color=0x00a0a0)
        embed.set_thumbnail(url=member.avatar_url)
        embed.add_field(name="User ID", value=id, inline=False)
        if member.name != member.display_name:
            embed.add_field(name="Nickname", value=member.display_name, inline=False)
        embed.add_field(name="Account Created:", value=member.created_at.strftime("%-d %B %Y at %-H:%M"), inline=True)
        embed.add_field(name="Joined Server:", value=member.joined_at.strftime("%-d %B %Y at %-H:%M"), inline=True)
        mention = []
        for role in member.roles:
            if role.name != "@everyone":
                mention.append(role.mention)
        roles = ", ".join(mention)
        embed.add_field(name="Roles", value=roles, inline=False)
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(moderation(bot))
