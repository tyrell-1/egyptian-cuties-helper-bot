import discord
from discord.ext import commands
from discord import app_commands
import os
import asyncio

class TicketView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
    
    @discord.ui.button(label="Open Ticket", style=discord.ButtonStyle.secondary, custom_id="open_verification_ticket", emoji="<:1337843137359515752:1494451080636010587>")
    async def open_ticket(self, interaction: discord.Interaction, button: discord.ui.Button):
        guild = interaction.guild
        
        # Safely parse IDs from env
        cat_id_str = os.getenv("TICKET_CATEGORY_ID", "")
        category_id = int(cat_id_str) if cat_id_str.isdigit() else 0
        category = discord.utils.get(guild.categories, id=category_id)
        
        staff_id_str = os.getenv("STAFF_ROLE_ID", "")
        staff_role_id = int(staff_id_str) if staff_id_str.isdigit() else 0

        
        # Check if user already has a ticket
        existing_channel = discord.utils.get(guild.text_channels, name=f"ticket-{interaction.user.name.lower()}")
        if existing_channel:
            await interaction.response.send_message(f"You already have a ticket open at {existing_channel.mention}.", ephemeral=True)
            return
            
        
        # Build Overwrites securely
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False),
            interaction.user: discord.PermissionOverwrite(read_messages=True, send_messages=True, attach_files=True),
            guild.me: discord.PermissionOverwrite(read_messages=True, send_messages=True, manage_channels=True)
        }
        
        staff_role = guild.get_role(staff_role_id)
        if staff_role:
            overwrites[staff_role] = discord.PermissionOverwrite(read_messages=True, send_messages=True)
        
        ticket_channel = await guild.create_text_channel(
            name=f"ticket-{interaction.user.name.lower()}",
            category=category,
            overwrites=overwrites
        )
        
        embed = discord.Embed(
            title=f"🎫 {interaction.user.name}'s Ticket",
            description=f"👋 Welcome {interaction.user.mention} — Let's Get You Verified اهلا بيك!\n\n"
                        f"Thanks for joining! To get access to the server, please answer the questions that will appear below.\n"
                        f"Staff will review your answers and get back to you shortly.\n\n"
                        f"شكراً إنك انضميت لينا! عشان تقدر تدخل السيرفر، ياريت تجاوب على الأسئلة اللي هتظهر تحت.\n"
                        f"الستاف (الإدارة) هيراجعوا إجاباتك وهيردوا عليك في أقرب وقت.",
            color=discord.Color.from_str("#f45142")
        )
        embed.set_author(name="Egyptian Cuties | Helper")
        
        await ticket_channel.send(content=f"{interaction.user.mention}", embed=embed, view=TicketControlView())
        await interaction.response.send_message(f"Ticket created! Go to {ticket_channel.mention}", ephemeral=True)

        questions = [
            "**1. How old are you?**\n١. عندك كام سنة؟",
            "**2. How did you find the server?**\n٢. عرفت السيرفر منين؟",
            "**3. Why do you want to join?**\n٣. ليه حابب تنضم لينا؟",
            "**4. Do you have any issues with LGBT identities, relationships, or discussions being openly present here?**\n٤. هل عندك أي مشكلة إن هويات، علاقات، أو نقاشات مجتمع الميم (LGBT) تكون موجودة ومفتوحة هنا؟"
        ]
        
        answers = []
        
        def check(m):
            return m.author == interaction.user and m.channel == ticket_channel

        try:
            for q in questions:
                await ticket_channel.send(q)
                msg = await interaction.client.wait_for('message', check=check, timeout=86400.0) # 1 day timeout
                answers.append(msg.content)
        except asyncio.TimeoutError:
            await ticket_channel.send("Verification timed out. Please open a new ticket or ping a staff member.")
            return
            
        summary_embed = discord.Embed(title="Verification Answers", color=discord.Color.dark_grey())
        if interaction.user.display_avatar:
            summary_embed.set_thumbnail(url=interaction.user.display_avatar.url)
            
        for i, q_title in enumerate(["Age", "Source", "Reason", "LGBTQ+ Stance"]):
            summary_embed.add_field(name=q_title, value=answers[i], inline=False)
            
        flags = ", ".join([flag.name.replace('_', ' ').title() for flag in interaction.user.public_flags.all()]) or "None"
        roles = ", ".join([role.mention for role in interaction.user.roles if role.name != "@everyone"]) or "None"
        
        summary_embed.add_field(
            name="Account Info", 
            value=f"**User ID:** {interaction.user.id}\n"
                  f"**Username: @{interaction.user.name}**\n"
                  f"**Created:** <t:{int(interaction.user.created_at.timestamp())}:f> (<t:{int(interaction.user.created_at.timestamp())}:R>)\n"
                  f"**Joined:** <t:{int(interaction.user.joined_at.timestamp())}:f> (<t:{int(interaction.user.joined_at.timestamp())}:R>)\n"
                  f"**Profile Badges:** {flags}\n"
                  f"**Roles:** {roles}", 
            inline=False
        )
        
        staff_role_id_str = os.getenv("STAFF_ROLE_ID", "")
        # Fallback to empty if it evaluates false in int conversion later
        staff_mention = f"<@&{staff_role_id_str}>" if staff_role_id_str.isdigit() and guild.get_role(int(staff_role_id_str)) else "@here"
        
        await ticket_channel.send(
            content=f"Thank you {interaction.user.mention}! {staff_mention} will review your application soon.",
            embed=summary_embed,
            view=TicketSummaryView()
        )

class TicketControlView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        
    @discord.ui.button(label="Close Ticket", style=discord.ButtonStyle.danger, custom_id="close_ticket", emoji="<:1361100801585582120:1494454549669478530>")
    async def close_ticket(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        
        overwrites = interaction.channel.overwrites
        user = None
        for target in overwrites:
            if isinstance(target, discord.Member):
                user = target
                break
                
        if user:
            await interaction.channel.set_permissions(user, send_messages=False, read_messages=True)
            
        button.disabled = True
        await interaction.message.edit(view=self)
        
        embed = discord.Embed(
            title="Ticket Closed", 
            description="This ticket has been closed by staff. It can now be safely deleted.", 
            color=discord.Color.red()
        )
        await interaction.channel.send(embed=embed, view=TicketClosedView())

class TicketSummaryView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        
    @discord.ui.button(label="Quick Verify", style=discord.ButtonStyle.success, custom_id="quick_verify", emoji="<:1345884737377665064:1494454247348113459>")
    async def quick_verify(self, interaction: discord.Interaction, button: discord.ui.Button):
        verified_role_id_str = os.getenv("VERIFIED_ROLE_ID", "")
        verified_role = interaction.guild.get_role(int(verified_role_id_str)) if verified_role_id_str.isdigit() else None
        
        unverified_role_id_str = os.getenv("UNVERIFIED_ROLE_ID", "")
        unverified_role = interaction.guild.get_role(int(unverified_role_id_str)) if unverified_role_id_str.isdigit() else None

        overwrites = interaction.channel.overwrites
        user = None
        for target in overwrites:
            if isinstance(target, discord.Member):
                user = target
                break

        if verified_role and unverified_role and user:
            await user.add_roles(verified_role)
            await user.remove_roles(unverified_role)
            await interaction.response.send_message(f"✅ Successfully verified {user.mention}!", ephemeral=False)
            
            button.disabled = True
            if interaction.message.embeds:
                embed = interaction.message.embeds[0]
                embed.color = discord.Color.green()
                await interaction.message.edit(embed=embed, view=self)
            else:
                await interaction.message.edit(view=self)
        else:
            await interaction.response.send_message("Failed to verify user. Please check role configuration or member presence.", ephemeral=True)
            
    @discord.ui.button(label="Close Ticket", style=discord.ButtonStyle.danger, custom_id="summary_close_ticket", emoji="<:1361100801585582120:1494454549669478530>")
    async def close_ticket(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        
        overwrites = interaction.channel.overwrites
        user = None
        for target in overwrites:
            if isinstance(target, discord.Member):
                user = target
                break
                
        if user:
            await interaction.channel.set_permissions(user, send_messages=False, read_messages=True)
            
        # Disable both buttons
        for child in self.children:
            child.disabled = True
        await interaction.message.edit(view=self)
        
        embed = discord.Embed(
            title="Ticket Closed", 
            description="This ticket has been closed by staff. It can now be safely deleted.", 
            color=discord.Color.red()
        )
        await interaction.channel.send(embed=embed, view=TicketClosedView())

class TicketClosedView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Delete Ticket", style=discord.ButtonStyle.danger, custom_id="delete_ticket", emoji="<:1345884823545450556:1494455783503433808>")
    async def delete_ticket(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("Deleting ticket in 5 seconds...", ephemeral=True)
        import asyncio
        await asyncio.sleep(5)
        try:
            await interaction.channel.delete()
        except discord.NotFound:
            pass

class Verification(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @app_commands.command(name="setup_verification", description="Creates the verification panel")
    @app_commands.checks.has_permissions(administrator=True)
    async def setup_verification(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title="🔐 Server Verification",
            description="<@&" + os.getenv("UNVERIFIED_ROLE_ID", "0") + "> | **To gain access to the server, you'll need to go through a quick verification process.**\n\n"
                        "Click the button below to open a ticket and answer a few short questions.\n"
                        "Staff will review your answers and grant you access.\n\n"
                        "افتح تيكت عشان تشوف التشانلز.\n\n",
            color=discord.Color.from_str("#f45142")
        )
        embed.set_author(name="Egyptian Cuties | Helper")
        embed.set_footer(text="Note: THIS SERVER IS SFW (البيت ده طاهر)")
        embed.set_thumbnail(url="https://images-ext-1.discordapp.net/external/hTu2ZvyS_xc_WQne9-eGqwSU2OjbIL14z_e8YKEY5FE/%3Fformat%3Dwebp%26quality%3Dlossless%26width%3D450%26height%3D450/https/cdn.discordapp.com/avatars/1421462612390055956/adc84fd2ce4462b6ef640360755c2e23.png?format=webp&quality=lossless&width=192&height=192")
        
        await interaction.channel.send(embed=embed, view=TicketView())
        await interaction.response.send_message("Verification panel setup complete.", ephemeral=True)
        
    @app_commands.command(name="verify", description="Verify a user and grant them the verified role")
    @app_commands.checks.has_permissions(manage_roles=True)
    async def verify_user(self, interaction: discord.Interaction, member: discord.Member):
        verified_role_id_str = os.getenv("VERIFIED_ROLE_ID", "")
        verified_role = interaction.guild.get_role(int(verified_role_id_str)) if verified_role_id_str.isdigit() else None
        
        unverified_role_id_str = os.getenv("UNVERIFIED_ROLE_ID", "")
        unverified_role = interaction.guild.get_role(int(unverified_role_id_str)) if unverified_role_id_str.isdigit() else None
        
        if verified_role and unverified_role:
            await member.add_roles(verified_role)
            await member.remove_roles(unverified_role)
            await interaction.response.send_message(f"Successfully verified {member.mention}!", ephemeral=False)
        else:
            await interaction.response.send_message("Roles are not set up correctly in the config.", ephemeral=True)

    @app_commands.command(name="purge_tickets", description="Admin command to securely purge all open/closed ticket channels")
    @app_commands.checks.has_permissions(administrator=True)
    async def purge_tickets(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=False)
        deleted_count = 0
        for channel in interaction.guild.text_channels:
            if channel.name.startswith("ticket-"):
                try:
                    await channel.delete()
                    deleted_count += 1
                except Exception as e:
                    print(f"Failed to delete channel {channel.name}: {e}")
        await interaction.followup.send(f"🧹 Purged {deleted_count} ticket channel(s) successfully.", ephemeral=False)

    @commands.Cog.listener()
    async def on_member_remove(self, member: discord.Member):
        guild = member.guild
        ticket_channel_name = f"ticket-{member.name.lower()}"
        ticket_channel = discord.utils.get(guild.text_channels, name=ticket_channel_name)
        
        if ticket_channel:
            embed = discord.Embed(
                title="Member Left",
                description=f"{member.mention} has left the server. Ticket has been automatically closed.",
                color=discord.Color.red()
            )
            await ticket_channel.send(embed=embed, view=TicketClosedView())
            # Close permissions for the member just in case they return before the ticket is deleted
            await ticket_channel.set_permissions(member, send_messages=False, read_messages=True)

async def setup(bot):
    await bot.add_cog(Verification(bot))
    # Registering persistent views when bot starts
    bot.add_view(TicketView())
    bot.add_view(TicketControlView())
    bot.add_view(TicketSummaryView())
    bot.add_view(TicketClosedView())
