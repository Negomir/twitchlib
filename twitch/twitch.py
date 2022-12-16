from auth.token_store import TokenStoreClient, TokenStore
from auth.app import AppAuth
from auth.user import UserAuth

class Twitch:
    def __init__(self, client_id: str, client_secret: str, token_client: TokenStoreClient):
        token_store = TokenStore(token_client)
        self.client_id = client_id
        self.client_secret = client_secret
        self.app_auth = AppAuth(client_id, token_store)
        self.user_auth = UserAuth(client_id, token_store)
