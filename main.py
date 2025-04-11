import discord, os
import discord.app_commands as app_commands
import dbman

from dotenv import load_dotenv

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
    await interaction.response.send_message(f"Added <@{admin.id}> to the Admins team.")


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

    admins.set(str(admin.id), {})
    passwords.set(str(admin.name), None)
    await interaction.response.send_message(
        f"Removed <@{admin.id}> from the Admins team."
    )


@tree.command(name="ping", description="Ping the radar", guild=guild)
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message(
        "Pong! " + str(round(client.latency, 2)) + "ms", ephemeral=True
    )
    if interaction.user.id == 726904686036123689:
        await tree.sync(guild=guild)


@client.event
async def on_ready():
    print("Hi!!")


if __name__ == "__main__":
    client.run(os.environ["TOKEN"])
