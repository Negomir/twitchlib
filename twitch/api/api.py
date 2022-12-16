from twitch.twitch import Twitch
from twitch.api.ads import Ads
from twitch.api.users import Users

class API:
    def __init__(self, tt: Twitch):
        self.tt = tt

        self.ads = Ads(tt)
        self.users = Users(tt)
