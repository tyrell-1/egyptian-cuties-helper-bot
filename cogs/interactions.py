import os
import random
import glob

import discord
from discord.ext import commands
from discord import app_commands

# Base path for GIF assets
GIFS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets", "gifs")

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


def get_random_gif(action: str) -> str:
    """Get a random GIF file path for the given action."""
    folder = os.path.join(GIFS_DIR, action)
    gifs = glob.glob(os.path.join(folder, "*.gif"))
    if not gifs:
        return None
    return random.choice(gifs)


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

        gif_path = get_random_gif(action)

        embed = discord.Embed(
            title=TITLES[action],
            description=text,
            color=COLORS[action],
        )

        file = None
        if gif_path:
            filename = f"{action}.gif"
            file = discord.File(gif_path, filename=filename)
            embed.set_image(url=f"attachment://{filename}")

        if not is_self:
            embed.set_footer(text=f"From {interaction.user.display_name} to {target.display_name}")

        await interaction.response.send_message(embed=embed, file=file)

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
