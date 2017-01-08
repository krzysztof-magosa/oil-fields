from random import uniform, randint
from oil.estate import Oilfield, PumpFactory, WagonFactory, DrillFactory
from oil.player import Player
from oil.observer import ObservableEntity
from itertools import cycle
import uuid


class Game(ObservableEntity):
    def __init__(self, initial_balance):
        super().__init__()
        self.uuid = uuid.uuid4()
        self.estates = []
        self.players = []
        self.initial_balance = initial_balance
        self.oil_prices = cycle([round(uniform(0.1, 5.0), 2) for _ in range(10000)])
        self.oil_price = None
        self.owner = None
        self.started = False
        self.turn = None
        self.turns = None
        self.sentinel = object()

        self.generate()

    @property
    def api_data(self):
        return dict(
            uuid=str(self.uuid),
            initial_balance=self.initial_balance,
            started=self.started,
            owner=str(self.owner.uuid),
            turn=(str(self.turn.uuid) if self.turn else None),
            player_names=[p.name for p in self.players],
            oil_price=self.oil_price
        )

    def start(self):
        self.started = True
        self.turns = cycle([self.sentinel] + self.players)
        self.next_player()

    def next_player(self):
        who = next(self.turns)
        if who == self.sentinel:
            self.on_next_round()
            self.next_player()
        else:
            self.turn = who

    def on_next_round(self):
        self.oil_price = next(self.oil_prices)

        # try to produce equipments/oil on each estate
        for item in self.estates:
            item.produce()

        print("ROUND")

    def create_player(self, **args):
        player = Player(**args)
        player.game = self
        player.balance = self.initial_balance
        self.players.append(player)

        # First player is owner
        if not self.owner:
            self.owner = player

        # @@@
        self.notify_observers(event=dict(type="update", property="players"))

        return player

    def get_estates(self, type=None, uuid=None, owner=None):
        for item in self.estates:
            if type and not isinstance(item, type):
                continue

            if uuid and item.uuid != uuid:
                continue

            if item.owner != owner:
                continue

            yield item

    def generate(self):
        for i in range(10):
            self.estates.append(
                Oilfield(
                    name="Oil Field {}".format(i+1),
                    price=randint(100000, 300000),
                    efficiency=randint(1000, 5000),
                    capacity=randint(50000, 100000),
                    deposit_depth=randint(500, 1000),
                    drill_progress=randint(150, 300)
                )
            )

        for i in range(5):
            self.estates.append(
                PumpFactory(
                    name="Pump Factory {}".format(i+1),
                    price=randint(100000, 300000),
                    efficiency=randint(5, 50),
                    spec=dict(efficiency=randint(200, 1000))
                )
            )

        for i in range(5):
            self.estates.append(
                WagonFactory(
                    name="Wagon Factory {}".format(i+1),
                    price=randint(100000, 300000),
                    efficiency=randint(5, 50),
                    spec=dict(efficiency=randint(200, 1000))
                )
            )

        for i in range(5):
            self.estates.append(
                DrillFactory(
                    name="Drill Factory {}".format(i+1),
                    price=randint(100000, 300000),
                    efficiency=randint(5, 50),
                    spec=dict(efficiency=randint(25, 250))
                )
            )
