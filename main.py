import discord
from discord import app_commands
from dotenv import load_dotenv
from os import getenv

from player_note import CreatePlayerNote
from servers import PlayerCount

load_dotenv()
bot_token = getenv("TOKEN")
bm_token = getenv("BM_TOKEN")

intents = discord.Intents.default()
intents.members = True

GUILD = discord.Object(id=978803693820452874)


class Client(discord.Client):
    def __init__(self):
        super().__init__(intents=discord.Intents.default())
        self.synced = False
        self.button_added = False

    async def on_ready(self):
        await self.wait_until_ready()
        if not self.synced:
            await tree.sync(guild=GUILD)
            self.synced = True
        print(f"We have logged in as {self.user}")


client = Client()
tree = app_commands.CommandTree(client)


@tree.command(
    guild=GUILD,
    name="create_player_note",
    description="Creates a BM player note"
)
async def create_player_note(interaction: discord.Interaction):
    await interaction.response.send_modal(CreatePlayerNote())


@tree.command(
    guild=GUILD,
    name="get_seeding_servers",
    description="Grabs all servers that need seeded"
)
async def get_seeding_servers(interaction: discord.Interaction):
    embedded_message = await PlayerCount().player_count()
    await interaction.response.send_message(embed=embedded_message)

client.run(bot_token)
