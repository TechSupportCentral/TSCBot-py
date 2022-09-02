from discord.ext import commands
import discord
import yaml
from main import get_database
mongodb = get_database()

class custom_commands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    global collection
    collection = mongodb['custom-commands']
    _custom_commands = {}

    with open('config.yaml', 'r') as config_file:
        config = yaml.load(config_file, Loader=yaml.BaseLoader)
    global channel_ids
    channel_ids = config['channel_ids']

    @commands.Cog.listener()
    async def on_ready(self):
        async def add_command(self, name, value, description):
            self._custom_commands[name] = value

            @commands.command(name=name)
            async def cmd(self, ctx):
                await ctx.send(value)

            cmd.cog = self
            self.__cog_commands__ += (cmd,)
            self.bot.add_command(cmd)

            @discord.app_commands.command(name=name, description=description)
            async def appcmd(interaction: discord.Interaction):
                await interaction.response.send_message(value)

            self.bot.tree.add_command(appcmd)

        for command in collection.find():
            await add_command(self, command['name'], command['value'], command['description'])
        await self.bot.tree.sync()

    @discord.app_commands.command(name="add-custom", description="Add a new custom command")
    @discord.app_commands.guild_only()
    @discord.app_commands.default_permissions()
    @discord.app_commands.describe(
        name="Name of the command",
        value="Response from the bot when the command is used",
        description="Description of the command"
    )
    async def add_custom(self, interaction: discord.Interaction, name: str, value: str, description: str):
        async def add_command(self, name, value, description):
            self._custom_commands[name] = value

            @commands.command(name=name)
            async def cmd(self, ctx):
                await ctx.send(value)

            cmd.cog = self
            self.__cog_commands__ += (cmd,)
            self.bot.add_command(cmd)

            @discord.app_commands.command(name=name, description=description)
            async def appcmd(interaction: discord.Interaction):
                await interaction.response.send_message(value)

            self.bot.tree.add_command(appcmd)
            await self.bot.tree.sync()

        if name in self._custom_commands or self.bot.get_command(name) or self.bot.tree.get_command(name):
            await interaction.response.send_message(f"The command `{name}` already exists.", ephemeral=True)
            return

        collection.insert_one({"name": name, "value": value, "description": description})
        await add_command(self, name, value, description)

        embed = discord.Embed(title="Custom Command Added", color=discord.Color.green())
        embed.set_thumbnail(url=interaction.user.display_avatar)
        embed.add_field(name="Added by", value=interaction.user, inline=False)
        embed.add_field(name="Command Name", value=name, inline=False)
        embed.add_field(name="Command Response", value=value, inline=False)
        channel = self.bot.get_channel(int(channel_ids['staff_news']))
        await channel.send(embed=embed)
        await interaction.response.send_message(f"Command `{name}` added successfully.")

    @discord.app_commands.command(name="remove-custom", description="Remove a custom command")
    @discord.app_commands.guild_only()
    @discord.app_commands.default_permissions()
    async def remove_custom(self, interaction: discord.Interaction, name: str):
        if name not in self._custom_commands:
            if self.bot.get_command(name) or self.bot.tree.get_command(name):
                await interaction.response.send_message("You cannot remove a built-in command.", ephemeral=True)
                return
            else:
                await interaction.response.send_message(f"The command `{name}` does not exist.", ephemeral=True)
                return
        else:
            value = self._custom_commands[name]

        collection.delete_one({"name": name})
        del self._custom_commands[name]
        self.bot.remove_command(name)
        self.bot.tree.remove_command(name)

        embed = discord.Embed(title="Custom Command Removed", color=discord.Color.red())
        embed.set_thumbnail(url=interaction.user.display_avatar)
        embed.add_field(name="Removed by", value=interaction.user, inline=False)
        embed.add_field(name="Command Name", value=name, inline=False)
        embed.add_field(name="Command Response", value=value, inline=False)
        channel = self.bot.get_channel(int(channel_ids['staff_news']))
        await channel.send(embed=embed)
        await interaction.response.send_message(f"Command `{name}` removed successfully.")

    @commands.hybrid_command(name="custom-list", description="Get a list of custom commands")
    async def custom_list(self, ctx):
        embed = discord.Embed(title="Custom Commands", color=0x00a0a0)
        for command in collection.find():
            embed.add_field(name=command['name'], value=command['description'], inline=False)
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(custom_commands(bot))
