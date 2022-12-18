import os
from twitch.twitch import Twitch
from twitch.auth.token_store import MemoryTokenClient
from twitch.api.api import API

client_id = os.environ["CLIENT_ID"]
client_secret = os.environ["CLIENT_SECRET"]

tt = Twitch(client_id=client_id, client_secret=client_secret, token_client=MemoryTokenClient())
# api = API(tt=tt)
# res = api.users.get_users(logins = ["negomir99"])
# print(res)

# print(tt.user_auth.generate_authorization_url(redirect_uri="http://localhost:5000/oauth/callback", scopes=["scope:one", "scope:two:three"]))
# print(tt.user_auth.handle_callback_url(""))

tt.user_auth.save_tokens("token", "refresh")
print(tt.user_auth.get_token())
print(tt.user_auth.get_refresh())
