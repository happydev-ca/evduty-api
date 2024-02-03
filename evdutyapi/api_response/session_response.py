from evdutyapi import Session


class SessionResponse:
    def __init__(self, is_active):
        self.is_active = is_active

    @classmethod
    def from_json(cls, data):
        return Session(is_active=data.get('isActive'))

    def to_json(self):
        return {
            "isActive": self.is_active
        }
