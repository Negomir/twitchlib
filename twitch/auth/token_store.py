class TokenStoreClient:
    def load(self, id: str) -> str:
        pass

    def save(self, id: str, token: str, ttl: int = 0):
        pass

class TokenStore:
    def __init__(self, cl: TokenStoreClient):
        self.cl = cl

    def load(self, id: str) -> str:
        return self.cl.load(id)

    def save(self, id: str, token: str, ttl: int = 0):
        return self.cl.save(id, token, ttl=ttl)
class MemoryTokenClient:
    def __init__(self):
        self.tokens = {}

    def load(self, id: str) -> str:
        if id not in self.tokens:
            raise KeyError("token not found under id: " + id)

        return self.tokens[id]

    def save(self, id: str, token: str, ttl: int = 0):
        if not self.tokens:
            self.tokens = {}

        self.tokens[id] = token
