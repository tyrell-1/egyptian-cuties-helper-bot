import discord
from discord.ext import commands
from discord import app_commands
import random

GIFS = {
    "hug": [
        "https://media1.tenor.com/m/SYsRdiK-T7gAAAAC/hug-anime.gif",
        "https://media1.tenor.com/m/4A9BTa_QLVUAAAAC/hug.gif",
        "https://media1.tenor.com/m/J7eGDvGeP9IAAAAC/enage-kiss-anime-hug.gif",
        "https://media1.tenor.com/m/2HxamDEy7XAAAAAC/yukon-child-form-embracing-ulquiorra.gif",
        "https://media1.tenor.com/m/TYvVBj3Fi5AAAAAC/hug.gif",
    ],
    "kiss": [
        "https://media1.tenor.com/m/kmxEaVuW8AoAAAAC/kiss-gentle-kiss.gif",
        "https://media1.tenor.com/m/BZyWzw2d5tAAAAAC/hyakkano-100-girlfriends.gif",
        "https://media1.tenor.com/m/YhGc7aQAI4oAAAAC/megumi-kato-kiss.gif",
        "https://media1.tenor.com/m/Z6_zOnLp8XUAAAAC/kiss.gif",
        "https://media1.tenor.com/m/S97_H69fVpYAAAAC/kiss-anime.gif",
    ],
    "pat": [
        "https://media1.tenor.com/m/CH6SUnuH17MAAAAC/lily-yami.gif",
        "https://media1.tenor.com/m/6yN8UfEALy8AAAAC/lawrence-wolf-girl.gif",
        "https://media1.tenor.com/m/rtHwrLRPlAkAAAAC/class-no-daikirai-na-joshi-to-kekkon-suru-koto-ni-natta-i'm-getting-married-to-a-girl-i-hate-in-my-class.gif",
        "https://media1.tenor.com/m/6MT_YvX996EAAAAC/pat-pat-head-thats-okay.gif",
        "https://media1.tenor.com/m/LLc0DzIEHEQAAAAC/fern-headpat-stark-fern-headpats-stark.gif",
    ],
    "slap": [
        "https://media1.tenor.com/m/p_S3Zl0Fv7MAAAAC/girl-slap-anime.gif",
        "https://media1.tenor.com/m/Sv8LQZAoQmgAAAAC/chainsaw-man-csm.gif",
        "https://media1.tenor.com/m/f69NRm3vS_IAAAAC/no-angry-anime.gif",
        "https://media1.tenor.com/m/X9ZkX_vI_mMAAAAC/anime-slap.gif",
        "https://media1.tenor.com/m/7FOnIksI6YQAAAAC/chikku-neesan-girl.gif",
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
