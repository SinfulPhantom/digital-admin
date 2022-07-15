from datetime import datetime
from typing import List, Tuple

import calendar
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


@tree.command(
    guild=GUILD,
    name="get_yes_reactions",
    description="Get all messages from the previous month"
)
async def get_sum_of_yes_reactions(interaction: discord.Interaction, year: str, month: str):
    counter = await get_reaction_counter(month, year)
    await interaction.response.send_message(counter)


async def get_reaction_counter(month, year):
    counter = 0
    channel = client.get_channel(994427431228289034)
    first_day, last_day = get_first_and_last_day(int(year), month)
    messages = [message.reactions async for message in channel.history(limit=300, before=last_day, after=first_day)]
    for message in messages:
        if message is not None:
            for reaction in message:
                if reaction.emoji.name == 'yes':
                    counter += 1
    return counter


def get_first_and_last_day(year: int, month: str) -> Tuple[datetime, datetime]:
    month_number = datetime.strptime(month, "%B").month
    first_day = datetime(year, month_number, 1)
    last_day = datetime(year, month_number, calendar.monthrange(year, month_number)[1])

    return first_day, last_day


@get_sum_of_yes_reactions.autocomplete('year')
async def auto_complete_year(interaction: discord.Interaction, year: str) -> List[app_commands.Choice[str]]:
    years = ["2019", "2020", "2021", "2022"]
    return [
        app_commands.Choice(name=year, value=year)
        for year in years
    ]


@get_sum_of_yes_reactions.autocomplete('month')
async def auto_complete_month(interaction: discord.Interaction, month: str) -> List[app_commands.Choice[str]]:
    months = calendar.month_name[1:]
    return [
        app_commands.Choice(name=month, value=month)
        for month in months
    ]

client.run(bot_token)
