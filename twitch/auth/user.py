from twitch.auth.token_store import TokenStore

class UserAuth:
    def __init__(self, client_id: str, token_store: TokenStore):
        self.token_store = token_store
        self.client_id = client_id

    def get_token(self):
        try:
            self.token_store.load(id=self.client_id)
        except KeyError:
            ### Implement re-getting token
            pass

    def save_token(self, token: str):
        self.token_store.save(id=self.client_id, token=token)
