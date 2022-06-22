import discord
from discord import ui

from battlemetrics import send_bm_player_note


class CreatePlayerNote(ui.Modal, title="Create Player Note"):
    rules = {
        "rule1": {
            "label": "Rule #1",
            "description": "No Toxic, Offensive, Derogatory, or Racist language of any kind."
        },
        "rule2": {
            "label": "Rule #2",
            "description": "No camping of HQ spawns. Artillery can be engaged. Squads should Defend Artillery if being used. Do not destroy unoccupied vehicles in HQ."
        },
        "rule3": {
            "label": "Rule #3",
            "description": "Do not intentionally teamkill or revenge teamkill."
        },
        "rule4": {
            "label": "Rule #4",
            "description": "Do not lock one man squads for Armor or Recon."
        },
        "rule5": {
            "label": "Rule #5",
            "description": "Streamers are required to have an overlay to cover their maps."
        },
        "rule6": {
            "label": "Rule #6",
            "description": "Cheating of any kind is not allowed and may result in a Permanent Ban."
        },
        "rule7": {
            "label": "Rule #7",
            "description": "Commanders and Squad Leaders must have a Microphone and Communicate/Contribute to the team effort."
        },
        "rule8": {
            "label": "Rule #8",
            "description": "Do not troll, grief, or deliberately waste any vehicles or assets."
        },
        "rule9": {
            "label": "Rule #9",
            "description": "Do not impersonate EASY Members or Staff, or use [EASY] tags without being a member."
        },
        "rule10": {
            "label": "Rule #10",
            "description": "Do not spam voice chat or text chat. No political or religious trolling."
        },
        "rule11": {
            "label": "Rule #11",
            "description": "Do not advertise any non-EASY content or links."
        },
        "rule12": {
            "label": "Rule #12",
            "description": "No Armor Squads until the lobby is 10 vs 10 or greater. Do not cap beyond midpoint (Warfare) until the lobby is 20 v 20 or greater."
        },
        "rule13": {
            "label": "Rule #13",
            "description": "EASY Company staff can punish players at their discretion."
        }
    }
    player_url = ui.TextInput(
        label="Player Battle Metrics url",
        style=discord.TextStyle.short,
        placeholder="BattleMetrics url",
        required=True,
        max_length=124
    )
    rules_broken = ui.Select(
        options=[],
        placeholder="Select rule that was broken"
    )
    for i in range(len(rules)):
        index = i + 1
        rules_broken.add_option(
            label=rules[f"rule{index}"]["label"],
            value=f"rule{index}",
            default=False
        )
    summary = ui.TextInput(
        label="Summary of Incident",
        style=discord.TextStyle.long,
        placeholder="Please provide as much detailed information as possible about the issue that is going on.",
        required=True,
    )
    logs = ui.TextInput(
        label="Additional Information (ex. BM Logs)",
        style=discord.TextStyle.long,
        placeholder="2022-06-17\n----------\n\n12:45 PM (Team) Example Player: $%@# you!",
        required=False,
    )
    action = ui.TextInput(
        label="Actions Taken",
        style=discord.TextStyle.short,
        placeholder="Verbal Warning, Requesting Flag",
        required=True,
    )

    async def on_submit(self, interaction: discord.Interaction) -> None:
        player_id = str(self.player_url).split("/")[-1]
        logs = f"\n\n{self.logs}" if self.logs else None
        rule = self.rules[self.rules_broken.values[0]]
        try:
            await send_bm_player_note(player_id, logs, rule, self.summary)
            embed = await self.embed_report()
            await interaction.response.send_message(embed=embed)
        except Exception as exc:
            print(exc)
            await interaction.response.send_message("Something went wrong")

    async def embed_report(self):
        return discord.Embed(
            title=f"{self.player_url} - {self.action}",
            color=discord.Color.og_blurple()
        )
