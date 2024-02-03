class Session:
    def __init__(self, is_active: bool):
        self.is_active = is_active

    def __repr__(self):
        return f"<Session is_active:{self.is_active}>"

    def __eq__(self, __value):
        return self.is_active == __value.is_active

    @classmethod
    def no_session(cls):
        return cls(is_active=False)
