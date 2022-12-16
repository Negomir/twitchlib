from twitch import Twitch
from ads import Ads
from users import Users

class API:
    def __init__(self, tt: Twitch):
        self.tt = tt

        self.ads = Ads(tt)
        self.users = Users(tt)
