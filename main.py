import os
from twitch.twitch import Twitch
from twitch.auth.token_store import MemoryTokenClient
from twitch.api.api import API

client_id = os.environ["CLIENT_ID"]
client_secret = os.environ["CLIENT_SECRET"]

tt = Twitch(client_id=client_id, client_secret=client_secret, token_client=MemoryTokenClient())
api = API(tt=tt)
res = api.users.get_users(logins = ["negomir99"])
print(res)
