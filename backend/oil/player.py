import uuid


class Player:
    def __init__(self, name):
        self.uuid = uuid.uuid4()
        self.name = name
        self.balance = 0
        self.oil = 0
        self.estates = []
        self.game = None

    def estates_by_type(self, type=None):
        return (x for x in self.estates if isinstance(x, type))

    def api_data(self):
        return dict(
            uuid=str(self.uuid),
            name=self.name
        )
