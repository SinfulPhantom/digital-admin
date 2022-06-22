import discord

from battlemetrics import get_server_player_count


class PlayerCount:
    direct_connect_url = "steam://connect/"
    server_info = {
        "server1": {
            "id": 11955377,
            "name": "Server #1",
            "direct_connect": f"{direct_connect_url}172.107.182.168:28200",
        },
        "server2": {
            "id": 9926105,
            "name": "Server #2",
            "direct_connect": f"{direct_connect_url}172.107.197.126:28100",
        },
        "server3": {
            "id": 12254334,
            "name": "Server #3",
            "direct_connect": f"{direct_connect_url}172.107.179.10:28000",
        },
        "server4": {
            "id": 5086054,
            "name": "Server #4",
            "direct_connect": f"{direct_connect_url}45.35.98.4:28200",
        },
        "server5": {
            "id": 9925915,
            "name": "Server #5",
            "direct_connect": f"{direct_connect_url}172.107.182.160:28000",
        },
        "server6": {
            "id": 14500472,
            "name": "Server #6",
            "direct_connect": f"{direct_connect_url}172.107.182.168:28200",
        },
    }

    async def player_count(self):
        server_list = await get_server_player_count(server_info=self.server_info)
        embed = discord.Embed(
            title="Servers needing seeded:",
            color=discord.Color.brand_green(),
            description="<@&989258001443594322>"
        )
        for server in server_list:
            current_players, max_players, name, url = server
            if int(current_players) <= 40:
                ratio = f"`{current_players}:{max_players}`"
                embed.add_field(name=f"__{name}__ - {ratio}", value=url, inline=False)
        return embed
