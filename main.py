import os
import discord
from discord.ext import commands
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
        
        # Sync slash commands with Discord
        await self.tree.sync()
        print("Slash commands synced!")

    async def on_ready(self):
        print(f"Logged in as {self.user} (ID: {self.user.id})")
        print("------")
        await self.change_presence(activity=discord.Streaming(name="I KISS BOYS", url="https://twitch.tv/discord"))

if __name__ == "__main__":
    bot = EgyptianCutiesBot()
    bot.run(TOKEN)
