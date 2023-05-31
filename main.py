from dotenv import load_dotenv
import os
import discord
from discord import app_commands, ui

load_dotenv()
token = os.environ.get("api-token")
NSI_GUILD_ID = int(os.environ.get("guild-id"))

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

tree = app_commands.CommandTree(client)


class TestModal(ui.Modal, title='Modal de test !'):
    name = ui.TextInput(label='Du texte ! mais ca sert pas à grand chose...')

    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.send_message(content=f"{interaction.user.display_name} a fini le modal ! WOUAW",
                                                silent=True)


class Testview(ui.View):

    # Define the actual button
    # When pressed, this increments the number displayed until it hits 5.
    # When it hits 5, the counter button is disabled and it turns green.
    # note: The name of the function does not matter to the library
    @discord.ui.button(label='Ouvrir un modal', style=discord.ButtonStyle.gray)
    async def count(self, interaction: discord.Interaction, button: discord.ui.Button):
        button.disabled = True
        button.label = "Modal déjà ouvert !"

        # Make sure to update the message with our updated selves
        await interaction.response.send_modal(TestModal())
        await interaction.edit_original_response(view=self)



@client.event
async def on_ready():
    await tree.sync(guild=discord.Object(id=NSI_GUILD_ID))
    print("command gaming")
    print(f'We have logged in as {client.user}')


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('ping'):
        await message.channel.send('pong!')


@tree.command(name="salut",
              description="Dit salut au bot ! C'est pas cool ca ?",
              guild=discord.Object(id=689164993924825192))
# Add the guild ids in which the slash command will appear. If it should be in all, remove the
# argument, but note that it will take some time (up to an hour) to register the command if it's for all guilds.
async def first_command(interaction: discord.Interaction):
    await interaction.response.send_message(f"Salut {interaction.user.display_name} !", ephemeral=True, view=Testview())


client.run(token)
