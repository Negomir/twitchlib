import httpx
import logging

from twitch.twitch import Twitch

class Eventsub:
    def __init__(self, tt: Twitch, callback_url: str):
        self.tt = tt
        self.callback_url = callback_url

    def subscribe(self, type: str, broadcaster_id: str, version: int = 1):
        body = {
            "type": type,
            "version": version,
            "condition": {
                "broadcaster_user_id": broadcaster_id
            },
            "transport": {
                "method": "webhook",
                "callback": self.callback_url,
                "secret": self.tt.client_secret
            }
        }

        headers = {
            "Authorization": "Bearer " + self.tt.user_auth.get_token(),
            "Client-Id": self.tt.client_id,
            "Content-Type": "application/json"
        }

        try:
            resp = httpx.post(url="https://api.twitch.tv/helix/eventsub/subscriptions", headers=headers, json=body)
            resp.raise_for_status()
        except Exception as ex:
            logging.error(ex)

    def unsubscribe(self):
        pass

    def list_subscription(self):
        pass

    def unsubscribe_all(self):
        pass
