import discord
from discord.ext import commands
from discord import app_commands
import random

GIFS = {
    "hug": [
        "https://media.tenor.com/9e1aE-SegBkAAAAd/hug.gif",
        "https://media.tenor.com/MYh6HqFGcBMAAAAd/anime-hug.gif",
        "https://media.tenor.com/MsoRLLN9xHwAAAAd/love-anime.gif",
        "https://media.tenor.com/7JYQLU0L6BIAAAAC/anime-hug.gif",
        "https://media.tenor.com/7BsPVMcIjWYAAAAd/hug.gif",
        "https://media.tenor.com/nt2fI7JeDkUAAAAd/cute-hug.gif",
    ],
    "kiss": [
        "https://media.tenor.com/qlGqjRR-1ikAAAAd/kiss-anime.gif",
        "https://media.tenor.com/YTdP9YERT0AAAAAd/anime-kiss.gif",
        "https://media.tenor.com/20sLq5rH3JIAAAAC/anime-kiss.gif",
        "https://media.tenor.com/4n8dUmJ_HHwAAAAd/anime-kiss.gif",
        "https://media.tenor.com/7WkMYnSgGDQAAAAd/love-anime.gif",
    ],
    "pat": [
        "https://media.tenor.com/N41zTEqMYEMAAAAd/head-pat.gif",
        "https://media.tenor.com/VwMGr6sBPboAAAAd/anime-head-pat.gif",
        "https://media.tenor.com/3LDmRTO1tCYAAAAd/anime-pat.gif",
        "https://media.tenor.com/MrMihveOYcgAAAAd/anime-head-pat.gif",
        "https://media.tenor.com/xpYSWMHMgOsAAAAd/pat-anime.gif",
    ],
    "slap": [
        "https://media.tenor.com/Ws6Dm1ZR4AIAAAAC/anime-slap.gif",
        "https://media.tenor.com/-RHjGLRJzKUAAAAd/slap-anime.gif",
        "https://media.tenor.com/pOLEMsZnkBsAAAAd/anime-slap.gif",
        "https://media.tenor.com/wMk1Op1MHM0AAAAd/anime-slap.gif",
        "https://media.tenor.com/EmhtHPXp4sgAAAAd/slap-anime.gif",
    ],
}

MESSAGES = {
    "hug": {
        "self": [
            "{user} hugs themselves... self-love is important! 🥺💖",
            "{user} wraps their own arms around themselves. We all need that sometimes. 🫂",
        ],
        "other": [
            "{user} gives {target} a big warm hug! 🤗💖",
            "{user} hugs {target} tightly! So wholesome! 🫂✨",
            "{user} squeezes {target} with love! 🥰",
            "{user} runs up and hugs {target}! Never letting go! 💕",
        ],
    },
    "kiss": {
        "self": [
            "{user} blows a kiss to the mirror. Self-love era! 💋✨",
            "{user} kisses the air... main character moment 💅",
        ],
        "other": [
            "{user} kisses {target}! 💋💖",
            "{user} gives {target} a sweet kiss! Mwah! 😘",
            "{user} plants a smooch on {target}! 💕",
        ],
    },
    "pat": {
        "self": [
            "{user} pats themselves on the head. You deserve it! 🥺",
            "{user} gives themselves a pat. Good job bestie! ✨",
        ],
        "other": [
            "{user} pats {target} on the head! Good job! ✨",
            "{user} gives {target} headpats! So cute! 🥰",
            "{user} gently pats {target}! There there~ 💖",
        ],
    },
    "slap": {
        "self": [
            "{user} slaps themselves... are you okay bestie? 😭",
            "{user} hits themselves with a reality check 💀",
        ],
        "other": [
            "{user} slaps {target}! OUCH! 💥",
            "{user} smacks {target} across the face! Drama! 😱",
            "{user} gives {target} a big slap! That's gotta hurt! 🫣",
        ],
    },
}

COLORS = {
    "hug": discord.Color.from_str("#FF8FAB"),
    "kiss": discord.Color.from_str("#FF6B9D"),
    "pat": discord.Color.from_str("#A78BFA"),
    "slap": discord.Color.from_str("#EF4444"),
}

TITLES = {
    "hug": "Hug! 🫂",
    "kiss": "Kiss! 💋",
    "pat": "Headpat! ✨",
    "slap": "Slap! 💥",
}


class Interactions(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def _do_interaction(self, interaction: discord.Interaction, action: str, user: discord.Member = None):
        target = user or interaction.user
        is_self = target.id == interaction.user.id

        message_pool = MESSAGES[action]["self" if is_self else "other"]
        text = random.choice(message_pool).format(
            user=interaction.user.mention,
            target=target.mention,
        )

        embed = discord.Embed(
            title=TITLES[action],
            description=text,
            color=COLORS[action],
        )
        embed.set_image(url=random.choice(GIFS[action]))

        if not is_self:
            embed.set_footer(text=f"From {interaction.user.display_name} to {target.display_name}")

        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="hug", description="Give someone a warm hug! 🫂")
    async def hug(self, interaction: discord.Interaction, user: discord.Member = None):
        await self._do_interaction(interaction, "hug", user)

    @app_commands.command(name="kiss", description="Give someone a kiss! 💋")
    async def kiss(self, interaction: discord.Interaction, user: discord.Member = None):
        await self._do_interaction(interaction, "kiss", user)

    @app_commands.command(name="pat", description="Give someone a headpat! ✨")
    async def pat(self, interaction: discord.Interaction, user: discord.Member = None):
        await self._do_interaction(interaction, "pat", user)

    @app_commands.command(name="slap", description="Slap someone! 💥")
    async def slap(self, interaction: discord.Interaction, user: discord.Member = None):
        await self._do_interaction(interaction, "slap", user)


async def setup(bot):
    await bot.add_cog(Interactions(bot))
