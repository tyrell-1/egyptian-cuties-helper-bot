import os
import discord
from discord.ext import commands
from discord import app_commands
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("TOKEN")

class EgyptianCutiesBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        intents.members = True

        super().__init__(
            command_prefix=commands.when_mentioned_or("!"),
            intents=intents,
            help_command=commands.DefaultHelpCommand()
        )

    async def setup_hook(self):
        # Load all cogs in the cogs directory
        for filename in os.listdir("./cogs"):
            if filename.endswith(".py"):
                await self.load_extension(f"cogs.{filename[:-3]}")
                print(f"Loaded cog: {filename}")
        
        # Sync slash commands to the specific guild (instant, no rate limit)
        guild_id = os.getenv("GUILD_ID")
        if guild_id:
            guild = discord.Object(id=int(guild_id))
            self.tree.copy_global_to(guild=guild)
            await self.tree.sync(guild=guild)
            print(f"Slash commands synced to guild {guild_id}!")
        else:
            # Fallback to global sync if no guild ID is set
            await self.tree.sync()
            print("Slash commands synced globally!")

    async def on_ready(self):
        print(f"Logged in as {self.user} (ID: {self.user.id})")
        print("------")
        await self.change_presence(activity=discord.Streaming(name="I KISS BOYS", url="https://twitch.tv/discord"))

if __name__ == "__main__":
    bot = EgyptianCutiesBot()

    @bot.tree.error
    async def on_app_command_error(interaction: discord.Interaction, error: app_commands.AppCommandError):
        if isinstance(error, app_commands.MissingPermissions):
            await interaction.response.send_message("❌ You don't have permission to do that.", ephemeral=True)
        elif isinstance(error, app_commands.CommandOnCooldown):
            await interaction.response.send_message(f"⏳ Slow down! Try again in {error.retry_after:.1f}s.", ephemeral=True)
        else:
            await interaction.response.send_message("Something went wrong. 😿", ephemeral=True)
            print(f"Unhandled app command error: {error}")

    bot.run(TOKEN)
