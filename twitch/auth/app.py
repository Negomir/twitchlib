from auth.token_store import TokenStore

class AppAuth:
    def __init__(self, session: str, token_store: TokenStore):
        self.token_store = token_store
        self.session = session

    def get_token(self):
        try:
            self.token_store.load(id=self.session)
        except KeyError:
            ### Implement re-getting token
            pass

    def save_token(self, token: str):
        self.token_store.save(id=self.session, token=token)
