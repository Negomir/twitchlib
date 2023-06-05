from dataclasses import dataclass

@dataclass
class Event:
    type: str
    status: str
    user_id: str
    user_login: str
    user_name: str
    broadcaster_user_id: str
    broadcaster_user_login: str
    broadcaster_user_name: str
    timestamp: str
