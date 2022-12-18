class TokenNotExists(Exception):
    pass

class TokenStoreClient:
    def load(self, id: str) -> str:
        pass

    def save(self, id: str, token: str, ttl: int = 0):
        pass

    def get_refresh(self, id: str) -> str:
        pass

    def save_refresh(self, id: str, token: str):
        pass

class TokenStore:
    def __init__(self, cl: TokenStoreClient):
        self.cl = cl

    def load(self, id: str) -> str:
        return self.cl.load(id)

    def save(self, id: str, token: str, ttl: int = 0):
        return self.cl.save(id, token, ttl=ttl)

    def get_refresh(self, id: str) -> str:
        return self.cl.get_refresh(id)

    def save_refresh(self, id: str, token: str):
        return self.cl.save_refresh(id, token)

class MemoryTokenClient:
    def __init__(self):
        self.tokens = {}
        self.refresh = {}

    def load(self, id: str) -> str:
        if id not in self.tokens:
            raise TokenNotExists("token_error", "token not found under id: " + id)

        return self.tokens[id]

    def save(self, id: str, token: str, ttl: int = 0):
        if not self.tokens:
            self.tokens = {}
        self.tokens[id] = token

    def get_refresh(self, id: str) -> str:
        if id not in self.refresh:
            raise TokenNotExists("refresh_error", "refresh token not found under id: " + id)

        return self.refresh[id]

    def save_refresh(self, id: str, token: str):
        if not self.refresh:
            self.refresh = {}

        self.refresh[id] = token
