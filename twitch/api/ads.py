import httpx
from twitch.twitch import Twitch

class Ads:
    def __init__(self, tt: Twitch):
        self.tt = tt

    def start_commercial(self, broadcaster_id: str, length: int) -> dict:
        """
        Requires the user access token with the channel:edit:commercial scope.
        Parameters:
        - broadcaster_id: the id of the channel on which you are playing the ad.
        - length: length (in seconds) for the ad to play. Maximum should be 180.
        Twitch tries to serve a commercial with the requested length, but the ad might be shorter or longer.
        """

        body = {
            "broadcaster_id": broadcaster_id,
            "length": length
        }

        headers = {
            "Authorization": "Bearer "+self.tt.user_auth.get_token(),
            "Client-Id": self.tt.client_id,
            "Content-Type": "application/json"
        }

        try:
            res = httpx.post("https://api.twitch.tv/helix/channels/commercial", headers=headers, json=body)
            res.raise_for_status()

            return res.json()
        except:
            raise
