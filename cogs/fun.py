import discord
from discord.ext import commands
from discord import app_commands

class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @app_commands.command(name="pride", description="Get a random pride flag and its meaning!")
    async def pride(self, interaction: discord.Interaction):
        import random
        flags = [
            ("🏳️‍🌈 Rainbow", "Represents the diverse LGBTQ+ community (Life, Healing, Sunlight, Nature, Harmony, Spirit)."),
            ("🏳️‍⚧️ Transgender", "Represents the transgender community (Light blue for boys, pink for girls, white for those transitioning or outside the binary)."),
            ("💖💜💙 Bisexual", "Represents attraction to multiple genders (Pink for same gender, blue for different genders, purple for the blend)."),
            ("💛🤍💜🖤 Non-binary", "Represents genders outside the male/female binary (Yellow for outside binary, white for many genders, purple for blend of male/female, black for agender).")
        ]
        chosen = random.choice(flags)
        
        embed = discord.Embed(title=f"Pride Flag: {chosen[0]}", description=f"**Meaning:** {chosen[1]}", color=discord.Color.random())
        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(Fun(bot))
