from twitch.auth.token_store import TokenStoreClient, TokenStore
from twitch.auth.app import AppAuth
from twitch.auth.user import UserAuth

class Twitch:
    def __init__(self, client_id: str, client_secret: str, token_client: TokenStoreClient):
        self.client_id = client_id
        self.client_secret = client_secret
        self.app_auth = AppAuth(client_id, client_secret, TokenStore(token_client, "app"))
        self.user_auth = UserAuth(client_id, client_secret, TokenStore(token_client, "user"))
