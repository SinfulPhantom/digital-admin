import os
from datetime import datetime, timedelta
from typing import List, Tuple

import calendar
import discord
from discord import app_commands
from dotenv import load_dotenv
from os import getenv

import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import style
style.use("fivethirtyeight")

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
    name="get_admin_metrics",
    description="Get metrics from specific year and month"
)
async def get_admin_metrics(interaction: discord.Interaction, year: str, month: str):
    if os.path.exists("adminmetrics.csv"):
        os.remove("adminmetrics.csv")
        print("Deleted existing admin metrics file")

    await get_reaction_counter(month, year)
    graph_png = "metrics.png"

    file = discord.File(graph_png, filename=graph_png)
    await interaction.response.send_message(graph_png, file=file)


async def get_reaction_counter(month, year):
    channel = client.get_channel(994427431228289034)
    first_day, last_day = get_first_and_last_day(int(year), month)
    messages = [message async for message in channel.history(limit=300, before=last_day, after=first_day)]

    return await get_monthly_report(messages)


async def get_monthly_report(messages):
    yes_counter = 0
    no_counter = 0
    neutral_counter = 0
    no_reaction_counter = 0
    total_counter = 0
    metrics_file = "adminmetrics.csv"

    for message in messages:
        current_day = message.created_at.day
        if len(message.reactions) == 0:
            no_reaction_counter += 1
        for reaction in message.reactions:
            if reaction.emoji.name == 'yes':
                yes_counter += 1
            elif reaction.emoji.name == 'no':
                no_counter += 1
            elif reaction.emoji.name == 'check_neutral_yellow':
                neutral_counter += 1
        total_counter += 1
        with open(metrics_file, "a") as f:
            f.write(
                f"{current_day},{yes_counter},{no_counter},{neutral_counter},{no_reaction_counter},{total_counter}\n"
            )

    plt.clf()
    df = pd.read_csv(metrics_file, names=['day', 'yes', 'no', 'neutral', 'no_reaction', 'total'])
    df.set_index('day', inplace=True)
    df['yes'].plot()
    df['no'].plot()
    df['neutral'].plot()
    df['no_reaction'].plot()
    df['total'].plot()
    plt.legend()
    plt.savefig("metrics.png")


def get_first_and_last_day(year: int, month: str) -> Tuple[datetime, datetime]:
    month_number = datetime.strptime(month, "%B").month
    first_day = datetime(year, month_number, 1)
    last_day = datetime(year, month_number, calendar.monthrange(year, month_number)[1])

    return first_day, last_day


@get_admin_metrics.autocomplete('year')
async def auto_complete_year(interaction: discord.Interaction, year: str) -> List[app_commands.Choice[str]]:
    years = ["2019", "2020", "2021", "2022"]
    return [
        app_commands.Choice(name=year, value=year)
        for year in years
    ]


@get_admin_metrics.autocomplete('month')
async def auto_complete_month(interaction: discord.Interaction, month: str) -> List[app_commands.Choice[str]]:
    months = calendar.month_name[1:]
    return [
        app_commands.Choice(name=month, value=month)
        for month in months
    ]

client.run(bot_token)
