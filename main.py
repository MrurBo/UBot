import discord, os
import discord.app_commands as app_commands
from discord.ext import tasks
import dbman
import logging
import asyncio
from dotenv import load_dotenv

logger = logging.getLogger("discord")
logger.setLevel(logging.DEBUG)

# check if a .env file exists
if not os.path.exists("./.env"):
    logger.fatal("No .env file found, please modify it and rerun.")
    with open("./.env", "x") as f:
        env = """TOKEN=
SECRET_KEY=
DISCORD_CLIENT_ID=
DISCORD_CLIENT_SECRET=
DISCORD_REDIRECT_URI=
"""
        f.write(env)
    exit(1)

import json

load_dotenv()

intents = discord.Intents.all()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

settings = json.load(open("./settings.json", "r"))

guild = discord.Object(int(settings.get("guildId")))

admins = dbman.Workspace("admins")
passwords = dbman.Workspace("passwords")
games = dbman.Workspace("games")
playerData = dbman.Workspace("playerData")
currentGame = dbman.Workspace("currentGame")

# look through all channels for settings["boardID"]
board = None


async def find_message_by_id(client: discord.Client, message_id: int):
    """
    Search for a message by ID across all servers the bot is in

    Args:
        client: Your discord.Client instance
        message_id: The message ID to search for

    Returns:
        discord.Message if found, None otherwise
    """
    # Iterate through all guilds
    for guild in client.guilds:
        try:
            # Check all text channels
            for channel in guild.text_channels:
                try:
                    # Check if we have permissions to read message history
                    if channel.permissions_for(guild.me).read_message_history:
                        message = await channel.fetch_message(message_id)
                        return message
                except discord.NotFound:
                    continue  # Message not in this channel
                except discord.Forbidden:
                    continue  # No permissions
        except Exception as e:
            print(f"Error searching guild {guild.name}: {e}")

    return None


async def find_board():
    global board

    board = await find_message_by_id(client, settings["boardID"])
    if board == None:
        return
    settings["boardID"] = board.id
    json.dump(settings, open("./settings.json", "w"), indent=4)
    print(board)


@tree.command(name="hi", description="Say hi", guild=guild)
async def hi(interaction: discord.Interaction):
    await interaction.response.send_message(f"Hello! <@{interaction.user.id}>")


@app_commands.choices(
    choices=[
        app_commands.Choice(name="Axis", value="1350588272988131398"),
        app_commands.Choice(name="Allies", value="1350588296966705152"),
    ]
)
@tree.command(name="join", description="Join a Team", guild=guild)
async def join(interaction: discord.Interaction, choices: app_commands.Choice[str]):
    await interaction.user.remove_roles(discord.Object(1350588296966705152))
    await interaction.user.remove_roles(discord.Object(1350588272988131398))

    await interaction.user.add_roles(discord.Object(int(choices.value)))
    await interaction.response.send_message(
        f"Added you to the {choices.name} team!", ephemeral=True
    )


@tree.command(name="add_admin", description="Admin command", guild=guild)
async def scores(interaction: discord.Interaction, admin: discord.Member):
    if admins.get(str(interaction.user.id)) == None:
        await interaction.response.send_message(
            "You do not have the permsissions to use this command.", ephemeral=True
        )
        return

    if admins.get(str(admin.id)) == {}:
        await interaction.response.send_message(
            "This person is already an admin.", ephemeral=True
        )
        return

    admins.set(str(admin.id), {})
    passwords.set(str(admin.name), "password")
    await interaction.response.send_message(
        f"Added <@{admin.id}> to the Admins team, Welcome aboard!"
    )


# remove admin
@tree.command(name="remove_admin", description="Admin command", guild=guild)
async def remove_admin(interaction: discord.Interaction, admin: discord.Member):
    if admins.get(str(interaction.user.id)) == None:
        await interaction.response.send_message(
            "You do not have the permsissions to use this command.", ephemeral=True
        )
        return
    if admins.get(str(admin.id)) != {}:
        await interaction.response.send_message(
            "This person is not an admin.", ephemeral=True
        )
        return

    admins.set(str(admin.id), None)
    passwords.set(str(admin.name), None)
    await interaction.response.send_message(
        f"Removed <@{admin.id}> from the Admins team, Walk the plank!"
    )


@tree.command(
    name="setstat", description="Change a persons stats to cheat :D", guild=guild
)
@app_commands.choices(
    stat=[
        app_commands.Choice(name="wins", value="wins"),
        app_commands.Choice(name="losses", value="losses"),
        app_commands.Choice(name="draws", value="draws"),
        app_commands.Choice(name="kills", value="kills"),
        app_commands.Choice(name="torps", value="torps"),
        app_commands.Choice(name="charges", value="charges"),
    ]
)
async def setstat(
    interaction: discord.Interaction,
    user: discord.Member,
    stat: app_commands.Choice[str],
    value: int,
):
    if admins.get(str(interaction.user.id)) == None:
        await interaction.response.send_message(
            "You do not have the permsissions to use this command.", ephemeral=True
        )
        return

    if not playerData.get(str(user.id)):
        playerData.set(
            str(user.id),
            {"wins": 0, "losses": 0, "draws": 0, "kills": 0, "torps": 0, "charges": 0},
        )

    data = playerData.get(str(user.id))
    data[stat.value] = value
    playerData.set(str(user.id), data)
    await interaction.response.send_message(
        "The stats have been set!, Hopefully this was for a good cause."
    )


@tree.command(name="stats", description="View your stats!", guild=guild)
async def join(interaction: discord.Interaction, user: discord.Member):
    embed = discord.Embed(
        title=str(user.display_name) + "'s Stats",
        description="This is where you can view your stats!",
    )
    # make sure user has data
    if not playerData.get(str(user.id)):
        playerData.set(
            str(user.id),
            {"wins": 0, "losses": 0, "draws": 0, "kills": 0, "torps": 0, "charges": 0},
        )

    data = playerData.get(str(user.id))
    embed.add_field(name="Wins ", value=str(data["wins"]), inline=False)
    embed.add_field(name="Losses", value=str(data["losses"]), inline=False)
    embed.add_field(name="Draws", value=str(data["draws"]), inline=False)
    embed.add_field(name="Kills", value=str(data["kills"]), inline=False)
    embed.add_field(name="Torpedos launched", value=str(data["torps"]), inline=False)
    embed.add_field(name="Depth Charges Used", value=str(data["charges"]), inline=False)
    await interaction.response.send_message(embed=embed)


async def set_board(end=False):
    global board
    embed = discord.Embed(
        title="Info Board",
        description="Current Teams and Vehicles",
    )
    if board == None:
        return
    if not end:
        keys = currentGame.get("players").keys()
        data = currentGame.get("players")
        crews = currentGame.get("crews")
        if crews == None:
            crews = {}
            currentGame.set("crews", crews)
        for i, steamid in enumerate(keys):
            if data[steamid]["crewID"] == None:
                continue
            embed.add_field(
                name=data[steamid]['name'],
                value=f"Crew: {crews[data[steamid]['crewID']]}\nTorpedo Hits: {data[steamid]['torpedo_hits']}\nShips Disabled: {data[steamid]['ships_disabled']}\nShips Sunk: {data[steamid]['ships_sunk']}",
                inline=False,
            )
    else:
        embed.add_field(
            name="Game Over",
            value="The game has ended, good luck at the next one!",
        )
    msg = await board.edit(
        embed=embed,
        content="",
    )
    board = msg


@tree.command(
    name="board", description="Creates a info board (Admins only)", guild=guild
)
async def join2(interaction: discord.Interaction):
    global board
    if board == None:

        board = await interaction.response.send_message("board")
        board = await interaction.channel.fetch_message(board.message_id)
    await set_board()

@tree.command(name="ping", description="Ping the sonar", guild=guild)
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message(
        "Pong! " + str(round(client.latency, 2)) + "ms, You just got pinged by U-BOT!",
        ephemeral=True,
    )
    if interaction.user.id == 726904686036123689:
        await tree.sync(guild=guild)


@client.event
async def on_ready():
    print("U-BOT, REPORTING FOR DUTY!")
    await find_board()
    await update_board_loop.start()
    # loop update board every 30 seconds


@tasks.loop(seconds=10)
async def update_board_loop():
    if board != None:
        await set_board()
    else:
        await find_board()


if __name__ == "__main__":
    client.run(os.environ["TOKEN"])
