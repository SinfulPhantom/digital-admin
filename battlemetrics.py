import requests
from dotenv import load_dotenv
from os import getenv

load_dotenv()
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {getenv('BM_TOKEN')}"
}


async def send_bm_player_note(player_id, logs, rule, summary):
    requests.post(
        url=f"https://api.battlemetrics.com/players/{player_id}/relationships/notes",
        json={
            "data": {
                "type": "playerNote",
                "attributes": {
                    "note": f"{rule['label']}: {rule['description']}\n\n{summary}{logs}",
                    "shared": False,
                }
            }
        },
        headers=headers
    )


async def get_server_player_count(server_info):
    player_count = []
    for server in server_info.values():
        server_attributes = requests.get(
            url=f"https://api.battlemetrics.com/servers/{server['id']}",
            headers=headers
        ).json()['data']['attributes']
        player_count.append((
            server_attributes['players'],
            server_attributes['maxPlayers'],
            server['name'],
            server['direct_connect']
            ))
    return player_count
