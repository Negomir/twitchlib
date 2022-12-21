import httpx
from httpx._exceptions import HTTPStatusError
from twitch.auth.token_store import TokenStore, TokenNotExists

class AppAuth:
    def __init__(self, client_id: str, client_secret: str, token_store: TokenStore):
        self.token_store = token_store
        self.client_id = client_id
        self.client_secret = client_secret

    def get_token(self):
        try:
            return self.token_store.load(id=self.client_id)
        except TokenNotExists:
            print("getting new token")
            try:
                token = self.__get_token()
                return token
            except Exception as ex:
                print(token)
                print(ex)
                raise ex

    def save_token(self, token: str, ttl: int = 0):
        self.token_store.save(id=self.client_id, token=token, ttl=ttl)

    def __get_token(self) -> str:
        body = {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "grant_type": "client_credentials"
        }

        headers = {
            "Content-Type": "application/x-www-form-urlencoded"
        }

        try:
            res = httpx.post("https://id.twitch.tv/oauth2/token", headers=headers, data=body)
            res.raise_for_status()

            r = res.json()
            token = r["access_token"]
            expires = r["expires_in"]
            self.save_token(token=token, ttl=expires)
            print(token)
            return token
        except HTTPStatusError as ex:
            print(ex)
            print(res.content)
            raise ex
        except Exception as ex:
            print(ex)
            raise ex
