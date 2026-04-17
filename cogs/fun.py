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

    @app_commands.command(name="gaydar", description="A playful gaydar to test your friends!")
    async def gaydar(self, interaction: discord.Interaction, user: discord.Member = None):
        import random
        user = user or interaction.user
        percentage = random.randint(0, 100)
        
        if percentage <= 20:
            remark = "Straight as a ruler! 📏 (يا شارع)"
        elif percentage <= 40:
            remark = "A little bit fruity... 🍓 (يامي)"
        elif percentage <= 60:
            remark = "Halfway out of the closet! 🚪"
        elif percentage <= 80:
            remark = "Pretty gay, we love to see it! 💅"
        else:
            remark = "Maximum gayness achieved! 🌈✨ (شواذ بلدنا)"

        embed = discord.Embed(
            title="Gaydar Result 🏳️‍🌈",
            description=f"## {user.mention} is **{percentage}%** gay!\n\n-# *{remark}*",
            color=discord.Color.random()
        )
        embed.set_thumbnail(url=user.display_avatar.url)
        
        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(Fun(bot))
