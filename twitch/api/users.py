import httpx
from urllib import parse
from twitch.twitch import Twitch

class Users:
    def __init__(self, tt: Twitch):
        self.tt = tt

    def get_users(self, ids: list = [], logins: list = [], user_token: bool = False) -> dict:
        """
        Requires either an app or a user token.
        Returns information about one or more twitch users.
        Parameters:
        - ids: list of user ids.
        - logins: list of user logins.
        """
        queries = {}
        if len(ids) > 0:
            queries["id"] = ids

        if len(logins) > 0:
            queries["login"] = logins

        qstr = parse.urlencode(queries, doseq=True)

        token = ""
        if user_token:
            token = self.tt.user_auth.get_token()
        else:
            token = self.tt.app_auth.get_token()

        headers = {
            "Authorization": "Bearer "+token,
            "Client-Id": self.tt.client_id,
        }

        try:
            res = httpx.get("https://api.twitch.tv/helix/users", params=qstr, headers=headers)
            res.raise_for_status()

            return res.json()
        except Exception as ex:
            print(ex)
            print(res.content)
            raise ex
