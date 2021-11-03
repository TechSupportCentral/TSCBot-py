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
    async def alert(self, ctx, *, description):
        if description:
            alert = description
        else:
            alert = "A description was not provided."
        embed = discord.Embed(title="Moderator Alert", description=f"[Jump to message]({ctx.message.jump_url})\n{alert}", color=discord.Color.red())
        embed.add_field(name="Alert Author", value=ctx.message.author, inline=True)
        embed.add_field(name="User ID", value=ctx.message.author.id, inline=True)
        channel = self.bot.get_channel(int(channel_ids['modtalk']))
        await channel.send(f"<@&{role_ids['moderator']}> <@&{role_ids['trial_mod']}>", embed=embed)
        await ctx.send("The moderators have been alerted.")

    @commands.command()
    async def suggest(self, ctx, *, suggestion):
        if not suggestion:
            await ctx.send("Please provide a suggestion.")
            return
        embed = discord.Embed(description=f"**Suggestion:** {suggestion}", color=discord.Color.lighter_grey())
        embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
        embed.add_field(name="Status", value="Pending")
        channel = self.bot.get_channel(int(channel_ids['suggestions_list']))
        await channel.send(embed=embed)
        await ctx.message.add_reaction("✅")

    @commands.command()
    async def d(self, ctx):
        return

    @commands.Cog.listener(name="on_message")
    async def matrix_moderation(self, message):

        async def userinfo(self, message):
            guild = message.guild

            if len(message.content.split(" ")) >= 2:
                arg = message.content.split(" ")[1]
            else:
                await message.channel.send("You can't do a userinfo on yourself, since you're a Matrix user.")
                return

            if "<@" in arg:
                id = arg
                id = id.replace("<", "")
                id = id.replace(">", "")
                id = id.replace("@", "")
                id = id.replace("!", "")
                id = int(id)
            elif arg.isdigit():
                id = int(arg)
            else:
                await message.channel.send("Users have to be in the form of an ID or a mention.")
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
            await message.channel.send(embed=embed)

        if message.content.startswith("d!userinfo"):
            await userinfo(self, message)

def setup(bot):
    bot.add_cog(misc(bot))
