import httpx
from httpx._exceptions import HTTPStatusError
from urllib import parse
from twitch.auth.token_store import TokenStore, TokenNotExists
class AuthorizeInvalidCallbackURL(Exception):
    pass

class AuthorizeCallbackException(Exception):
    pass

class AuthorizeInvalidState(Exception):
    pass

class UserAuth:
    def __init__(self, client_id: str, client_secret: str, token_store: TokenStore):
        self.token_store = token_store
        self.client_id = client_id
        self.client_secret = client_secret

    def get_token(self) -> str:
        try:
            return self.token_store.load(id=self.client_id)
        except TokenNotExists:
            raise
        except:
            ### refresh token
            return None

    def get_refresh(self) -> str:
        return self.token_store.get_refresh(id=self.client_id)

    def save_tokens(self, token: str, refresh: str, ttl: int = 0):
        self.token_store.save(id=self.client_id, token=token, ttl=ttl)
        self.token_store.save_refresh(id=self.client_id, token=refresh)

    def generate_authorization_url(self, redirect_uri: str, scopes: list) -> str:
        params = {
            "response_type": "code",
            "client_id": self.client_id,
            "redirect_uri": redirect_uri,
            "scope": "+".join(scopes),
            "state": "state_check"
        }

        return "https://id.twitch.tv/oauth2/authorize?" + parse.urlencode(params)

    def handle_callback_url(self, callback_url: str) -> str:
        try:
            query = callback_url.split("?")[1]
            kvs = query.split("&")
            data = {}
            for kv in kvs:
                key_val = kv.split("=")
                val = ""
                if len(key_val) == 2:
                    val = key_val[1]
                data[key_val[0]]=val
        except Exception as ex:
            raise AuthorizeInvalidCallbackURL("invalid_url", ex)

        if "state" not in data:
            raise AuthorizeInvalidState("state_error", "state parameter is missing")

        if data["state"] != "state_check":
            raise AuthorizeInvalidState("state_error", "state parameter does not match")

        if "error" in data:
            raise AuthorizeCallbackException(data["error"], data["error_description"])

        if "code" not in data:
            raise AuthorizeCallbackException("code_error", "code parameter is missing")

        return data["code"]

    def __get_token(self, code: str, redirect_uri: str) -> str:
        body = {
            "client_id": self.client_id,
            "client_secret": self.client_id,
            "code": code,
            "grant_type": "authorization_code",
            "redirect_uri": redirect_uri
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
            refresh = r["refresh_token"]
            self.save_tokens(token=token, refresh=refresh, ttl=expires)
        except HTTPStatusError as ex:
            print(ex)
            print(res.content)
            raise
