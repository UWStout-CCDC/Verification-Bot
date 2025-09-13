import discord
from discord.ext import commands
from discord import app_commands
import random
import sqlite3
import time
import os
from email_sender import send_verification_email
from dotenv import load_dotenv
import logging

# Load environment variables
load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")
VERIFY_ROLE_NAME = os.getenv("VERIFY_ROLE_NAME", "Verified")
OWNER_USERID = int(os.getenv("OWNER_USERID")) 
APPLICATION_ID = int(os.getenv("APPLICATION_ID"))

# Enable all intents or only what you need
intents = discord.Intents.default()
intents.members = True   # Needed for role assignment
intents.guilds = True
intents.message_content = True  # Required for reading message text like !verify

# Initialize the bot with intents
bot = commands.Bot(command_prefix="/", intents=intents, application_id=APPLICATION_ID)

# Initialize SQLite
DB_PATH = "/app/data/database.sqlite"

os.makedirs("/app/data", exist_ok=True)  # Ensure folder exists
conn = sqlite3.connect(DB_PATH)
c = conn.cursor()

# Create tables
c.execute("""
CREATE TABLE IF NOT EXISTS verifications (
    discord_id TEXT NOT NULL,
    guild_id TEXT NOT NULL,
    email TEXT NOT NULL,
    code TEXT NOT NULL,
    expires_at INTEGER NOT NULL
)
""")

# Create table for guild whitelist domains
c.execute("""
CREATE TABLE IF NOT EXISTS guild_whitelist_domains (
    guild_id TEXT NOT NULL,
    domain TEXT NOT NULL,
    PRIMARY KEY (guild_id, domain)
)
""")

c.execute("""
CREATE TABLE IF NOT EXISTS verified_users (
    discord_id TEXT NOT NULL,
    guild_id TEXT NOT NULL,
    email TEXT NOT NULL,
    verified_at INTEGER NOT NULL,
    PRIMARY KEY (discord_id, guild_id)
)
""")

# Create table for guild roles
c.execute("""
CREATE TABLE IF NOT EXISTS guild_verified_roles (
    guild_id TEXT PRIMARY KEY,
    role_id TEXT NOT NULL
)
""")

conn.commit()

# Create a CommandTree for slash commands
tree = bot.tree

def generate_code():
    """Generate a random 6-digit code."""
    return str(random.randint(100000, 999999))

# Slash command to set the whitelist email domain
@bot.tree.command(name="set_whitelist_domain", description="Set the email domain to whitelist")
@app_commands.describe(domain="Email domain to whitelist (e.g. example.com)")
async def set_whitelist_domain(interaction: discord.Interaction, domain: str):
    # Check if the command was ran in a dm
    if interaction.guild is None:
        await interaction.response.send_message(
            "❌ This command can only be used in a server.", ephemeral=True
        )
        return

    # Only allow server admins
    if not interaction.user.guild_permissions.administrator:
        await interaction.response.send_message(
            "❌ You must be an administrator to use this command.", ephemeral=True
        )
        return

    try:
        # Store the whitelist domain in the database
        c.execute(
            "INSERT INTO guild_whitelist_domains (guild_id, domain) VALUES (?, ?)"
            "ON CONFLICT(guild_id, domain) DO NOTHING",
            (str(interaction.guild.id), domain)
        )
        conn.commit()
    except sqlite3.Error as e:
        logging.error(f"Failed to write to database: {e}")
        await interaction.response.send_message(
            f"❌ Failed to set whitelist domain due to a database error.", ephemeral=True
        )
        return
    

    await interaction.response.send_message(
        f"✅ Whitelist domain set to **{domain}** for this server.", ephemeral=True
    )

# Slash command to remove the whitelist email domain
@bot.tree.command(name="remove_whitelist_domain", description="Remove the email domain whitelist")
@app_commands.describe(domain="Email domain to remove from whitelist")
async def remove_whitelist_domain(interaction: discord.Interaction, domain: str):
    # Check if the command was ran in a dm
    if interaction.guild is None:
        await interaction.response.send_message(
            "❌ This command can only be used in a server.", ephemeral=True
        )
        return

    # Only allow server admins
    if not interaction.user.guild_permissions.administrator:
        await interaction.response.send_message(
            "❌ You must be an administrator to use this command.", ephemeral=True
        )
        return

    # Remove the whitelist domain from the database
    try:
        c.execute("DELETE FROM guild_whitelist_domains WHERE guild_id = ? AND domain = ?", (str(interaction.guild.id), domain))
        conn.commit()
    except sqlite3.Error as e:
        logging.error(f"Failed to remove whitelist domain: {e}")
        await interaction.response.send_message(
            f"❌ Failed to remove whitelist domain due to a database error.", ephemeral=True
        )
        return

    await interaction.response.send_message(
        "✅ Whitelist domain removed for this server.", ephemeral=True
    )

# Slash command to view the current whitelist email domain
@bot.tree.command(name="view_whitelist_domain", description="View the current email domain whitelist")
async def view_whitelist_domain(interaction: discord.Interaction):
    # Check if the command was ran in a dm
    if interaction.guild is None:
        await interaction.response.send_message(
            "❌ This command can only be used in a server.", ephemeral=True
        )
        return

    # Only allow server admins
    if not interaction.user.guild_permissions.administrator:
        await interaction.response.send_message(
            "❌ You must be an administrator to use this command.", ephemeral=True
        )
        return

    # Retrieve the whitelist domain from the database
    try:
        c.execute("SELECT domain FROM guild_whitelist_domains WHERE guild_id = ?", (str(interaction.guild.id),))
        row = c.fetchall()
    except sqlite3.Error as e:
        logging.error(f"Failed to retrieve whitelist domains: {e}")
        await interaction.response.send_message(
            "❌ Failed to retrieve whitelist domains due to a database error.", ephemeral=True
        )
        return
    if not row:
        await interaction.response.send_message(
            "ℹ️ No whitelist domain is set for this server. All email domains are allowed.", ephemeral=True
        )
    else:
        domains = [r[0] for r in row]
        await interaction.response.send_message(
            f"ℹ️ Current whitelist domains for this server: {', '.join(domains)}", ephemeral=True
        )

# Slash command to set the verified role
@bot.tree.command(name="set_verified_role", description="Set the role given to verified users")
@app_commands.describe(role="Role to assign after verification")
async def set_verified_role(interaction: discord.Interaction, role: discord.Role):
    # Check if the command was ran in a dm
    if interaction.guild is None:
        await interaction.response.send_message(
            "❌ This command can only be used in a server.", ephemeral=True
        )
        return

    # Only allow server admins
    if not interaction.user.guild_permissions.administrator:
        await interaction.response.send_message(
            "❌ You must be an administrator to use this command.", ephemeral=True
        )
        return

    # Check if the bot has previously set a verified role for this guild if so, migrate all users with the old role to the new role
    try:
        c.execute("SELECT role_id FROM guild_verified_roles WHERE guild_id = ?", (str(interaction.guild.id),))
        row = c.fetchone()
    except sqlite3.Error as e:
        logging.error(f"Failed to fetch previous verified role: {e}")
        await interaction.response.send_message(
            "❌ Failed to fetch previous verified role due to a database error.", ephemeral=True
        )
        return
    if row:
        old_role_id = int(row[0])
        old_role = interaction.guild.get_role(old_role_id)
        if old_role:
            # Migrate users from old role to new role
            for member in interaction.guild.members:
                if old_role in member.roles:
                    await member.remove_roles(old_role, reason="Migrating to new verified role")
                    await member.add_roles(role, reason="Migrating to new verified role")

    # Store guild_id and role_id in the database
    try:
        c.execute(
            "INSERT INTO guild_verified_roles (guild_id, role_id) VALUES (?, ?) "
            "ON CONFLICT(guild_id) DO UPDATE SET role_id=excluded.role_id",
            (str(interaction.guild.id), str(role.id))
        )
        conn.commit()
    except sqlite3.Error as e:
        logging.error(f"Failed to set verified role: {e}")
        await interaction.response.send_message(
            "❌ Failed to set verified role due to a database error.", ephemeral=True
        )
        return

    await interaction.response.send_message(
        f"✅ Verified role set to **{role.name}** for this server.", ephemeral=True
    )

# Example: assigning the role to a verified user
async def assign_verified_role(user: discord.User, guild_id=None):
    guild = bot.get_guild(int(guild_id))
    member = guild.get_member(user.id)
    if not guild:
        logging.warning(f"Guild ID {guild_id} not found.")
        return
    
    c.execute(
        "SELECT role_id FROM guild_verified_roles WHERE guild_id = ?",
        (str(guild_id),)
    )
    row = c.fetchone()
    if row:
        role_id = int(row[0])
        role = guild.get_role(role_id)
        if role:
            await member.add_roles(role, reason="User verified")
            logging.info(f"Assigned role {role.name} to {member.display_name}")
        else:
            logging.warning(f"Role ID {role_id} not found in guild {guild.name}")
    else:
        logging.info(f"No verified role set for guild {guild.name}")

@bot.tree.command(name="verify", description="Start the email verification process")
@app_commands.describe(email="Your email address to verify")
async def verify(interaction: discord.Interaction, email: str):
    # Check if the command was ran in a dm
    if interaction.guild is None:
        await interaction.response.send_message(
            "❌ This command can only be used in a server.", ephemeral=True
        )
        return

    # Acknowledge interaction immediately
    await interaction.response.defer(ephemeral=True)  # Shows “thinking...” to user

    """Start the verification process."""
    
    # Check if the user is already verified
    c.execute("SELECT email FROM verified_users WHERE discord_id = ? AND guild_id = ?", (str(interaction.user.id), str(interaction.guild.id)))
    already_verified = c.fetchone()
    if already_verified:
        await interaction.followup.send(f"✅ You are already verified with the email `{already_verified[0]}`.")
        return

    # Check if the email is already used by another Discord user
    c.execute("SELECT discord_id FROM verified_users WHERE email = ? AND guild_id = ?", (email, str(interaction.guild.id)))
    existing = c.fetchone()
    if existing:
        await interaction.followup.send(f"❌ The email `{email}` is already linked to another Discord account.")
        return

    # Check if the email domain is in the whitelist (There may be multiple domains) for the guild. If there are no whitelist domains set, allow all.
    domain = email.split('@')[-1]
    c.execute("SELECT domain FROM guild_whitelist_domains WHERE guild_id = ?", (str(interaction.guild.id),))
    rows = c.fetchall()
    if rows:
        whitelisted_domains = [row[0] for row in rows]
        if domain not in whitelisted_domains:
            await interaction.followup.send(f"❌ The email domain `{domain}` is not allowed. Please use an email with one of the following domains: {', '.join(whitelisted_domains)}")
            return


    # Generate code and expiration timestamp
    code = generate_code()
    expires = int(time.time()) + 600  # 10-minute expiry

    # Remove any old pending verification for this user
    c.execute("DELETE FROM verifications WHERE discord_id = ?", (str(interaction.user.id),))
    conn.commit()

    # Store the pending verification
    c.execute("INSERT INTO verifications (discord_id, guild_id, email, code, expires_at) VALUES (?, ?, ?, ?, ?)",
              (str(interaction.user.id), str(interaction.guild.id), email, code, expires))
    conn.commit()

    # Send email with code
    send_verification_email(email, code)
    await interaction.user.send(
        f"📧 A verification code has been sent to **{email}**.\n"
        "Use `/code <your_code>` here to complete verification."
    )
    await interaction.followup.send("I've sent you an email with a verification code! Please check your email.")

@bot.tree.command(name="code", description="Verify using the code received via email")
@app_commands.describe(code="Your verification code")
async def code(interaction: discord.Interaction, code: str):
    # Acknowledge interaction immediately
    await interaction.response.defer(ephemeral=True)  # Shows “thinking...” to user

    """Verify using the code received via email."""
    now = int(time.time())

    # Find matching pending verification
    c.execute("""
        SELECT email FROM verifications 
        WHERE discord_id = ? AND code = ? AND expires_at > ?
    """, (str(interaction.user.id), code, now))
    result = c.fetchone()

    if not result:
        await interaction.followup.send("❌ Invalid or expired code. Please run `/verify` again.")
        return

    email = result[0]

    # Get guild ID from verifications table
    c.execute("SELECT guild_id FROM verifications WHERE discord_id = ? AND code = ?", (str(interaction.user.id), code))
    guild_row = c.fetchone()
    if not guild_row:
        await interaction.followup.send("❌ An error occurred. Please try again.")
        return

    logging.info(f"User {interaction.user.display_name} verified with email {email} in guild ID {guild_row[0]}")
    await assign_verified_role(interaction.user, guild_id=guild_row[0])

    # Store permanent verification
    c.execute("""
        INSERT INTO verified_users (discord_id, guild_id, email, verified_at)
        VALUES (?, ?, ?, ?)
    """, (str(interaction.user.id), guild_row[0], email, now))
    conn.commit()

    # Clean up temporary verification
    c.execute("DELETE FROM verifications WHERE discord_id = ?", (str(interaction.user.id),))
    conn.commit()

    await interaction.followup.send(f"✅ {interaction.user.mention}, you have been verified and linked to `{email}`!")

@tree.command(name="whois", description="Check which email a user is linked to (Admin only)")
@app_commands.describe(user="The user to check")
async def whois(interaction: discord.Interaction, user: discord.Member):
    # Check if the command was ran in a dm
    if interaction.guild is None:
        await interaction.response.send_message(
            "❌ This command can only be used in a server.", ephemeral=True
        )
        return

    # Acknowledge interaction immediately
    await interaction.response.defer(ephemeral=True)  # Shows “thinking...” to user

    """Admin command to check which email a user is linked to."""
    if not interaction.user.guild_permissions.administrator:
        await interaction.followup.send("❌ You do not have permission to use this command.")
        return

    c.execute("SELECT email, verified_at FROM verified_users WHERE discord_id = ? AND guild_id = ?", (str(user.id), str(interaction.guild.id)))
    result = c.fetchone()
    if not result:
        await interaction.followup.send(f"ℹ️ {user.mention} is not verified.")
    else:
        email, timestamp = result
        verified_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(timestamp))
        await interaction.followup.send(f"🔹 {user.mention} is verified with email: `{email}` (since {verified_time})")

# bot = commands.Bot(command_prefix="/", intents=intents,
                #    case_insensitive=False,)

@bot.command()
async def sync(ctx):
    print("sync command")
    if ctx.author.id == OWNER_USERID:
        bot.tree.clear_commands(guild=ctx.guild)
        await bot.tree.sync(guild=ctx.guild)
        await ctx.send('Command tree synced.')
    else:
        await ctx.send('You must be the owner to use this command!')


@bot.event
async def on_ready():
    await bot.tree.sync()  # Sync commands to the test guild
    print(f"Bot is online as {bot.user}!")

# --- Run the bot ---
if __name__ == "__main__":
    print("Starting bot...")
    bot.run(TOKEN)