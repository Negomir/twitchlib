from urllib import parse
from twitch.auth.token_store import TokenStore
class AuthorizeInvalidCallbackURL(Exception):
    pass

class AuthorizeCallbackException(Exception):
    pass

class AuthorizeInvalidState(Exception):
    pass

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

    def generate_authorization_url(self, redirect_uri: str, scopes: list) -> str:
        params = {
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
