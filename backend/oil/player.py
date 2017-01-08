from oil.observer import ObservableEntity
from oil.estate import Estate
import uuid


class Player(ObservableEntity):
    def __init__(self, name):
        super().__init__()

        self.uuid = uuid.uuid4()
        self.name = name
        self.balance = 0
        self.oil = 0
        self.estates = []
        self.game = None

    def estates_by_type(self, type=None):
        return (x for x in self.estates if isinstance(x, type))

    def buy(self, estate):
        assert(isinstance(estate, Estate))
        assert(self.balance > estate.price)

        self.balance -= estate.price
        estate.owner = self

    @property
    def api_data(self):
        return dict(
            uuid=str(self.uuid),
            name=self.name,
            balance=self.balance,
            oil=self.oil
        )
