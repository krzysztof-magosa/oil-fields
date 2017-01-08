from oil.game import Game
from oil.player import Player
from oil.estate import Estate
from oil.observer import Observer, Group
import websockets
import asyncio
import json
import uuid


class Session(Observer):
    def __init__(self, app, websocket):
        self.app = app
        self.websocket = websocket
        self.name = None
        self.uuid = uuid.uuid4()
        self.send_queue = asyncio.Queue()
        self._player = None
        self.group = None  # observer group

    async def loop(self):
        try:
            while True:
                listener_task = asyncio.ensure_future(self.websocket.recv())
                producer_task = asyncio.ensure_future(self.producer())
                done, pending = await asyncio.wait(
                    [listener_task, producer_task],
                    return_when=asyncio.FIRST_COMPLETED
                )

                if listener_task in done:
                    message = listener_task.result()
                    await self.consumer(message)
                else:
                    listener_task.cancel()

                if producer_task in done:
                    message = producer_task.result()
                    await self.websocket.send(message)
                else:
                    producer_task.cancel()
        finally:
            self.app.unregister_session(self)

    async def producer(self):
        return await self.send_queue.get()

    async def consumer(self, message):
        if self.group:
            self.group.begin()

        message_data = json.loads(message)
        action = message_data["action"]
        data = message_data["data"]

        if action == "set_name":
            await self.set_name(data)
        elif action == "create_game":
            await self.create_game(data)
        elif action == "join_game":
            await self.join_game(data)
        elif action == "start_game":
            await self.start_game(data)
        elif action == "next_player":
            self.game.next_player()
        elif action == "buy_oilfield":
            self.buy_oilfield(data)
        elif action == "buy_factory":
            self.buy_factory(data)

        if self.group:
            self.group.commit()

    async def set_name(self, data):
        self.name = data["name"]
        self.send("games", [x for x in self.app.games if not x.started])

    async def create_game(self, data):
        game, group = self.app.create_game(**data)
        self.group = group
        self.player = game.create_player(name=self.name)

    async def join_game(self, data):
        games = list(filter(lambda x: str(x.uuid) == data["uuid"], self.app.games))
        assert(len(games) == 1)
        game = games[0]
        self.group = self.app.game_group(game)

        self.player = game.create_player(name=self.name)

    async def start_game(self, data):
        assert(self.player)
        assert(self.name)

        self.player.game.start()

    def buy_oilfield(self, data):
        estate = [x for x in self.game.estates if str(x.uuid) == data["uuid"]][0]
        self.player.buy(estate)

        self.game.next_player()

    def buy_factory(self, data):
        estate = [x for x in self.game.estates if str(x.uuid) == data["uuid"]][0]
        estate.equipment_price = data["equipment_price"]
        self.player.buy(estate)

        self.game.next_player()

    @property
    def game(self):
        return self.player.game

    @property
    def player(self):
        return self._player

    @player.setter
    def player(self, player):
        self._player = player

        self.group.assign(self.game)
        self.group.assign_many(self.game.estates)
        self.group.assign_many(self.game.players)

        self.observe(self.game)
        self.observe_many(self.game.estates)
        self.observe_many(self.game.players)

    def notify(self, messages):
        if any(isinstance(x[0], Player) for x in messages):
            self.send("players", self.game.players)
            self.send("me", self.player)

        if any(isinstance(x[0], Estate) for x in messages):
            self.send("estates", self.game.estates)

        # There is one game, so no point in checking instance.
        if any(isinstance(x[0], Game) for x in messages):
            self.send("game", self.player.game)

    def api_dump(self, data):
        if isinstance(data, list):
            return [self.api_dump(item) for item in data]
        else:
            if hasattr(data, "api_data"):
                return data.api_data
            else:
                return data

    def send(self, action, data):
        message = json.dumps(
            dict(
                action=action,
                data=self.api_dump(data)
            )
        )
        self.send_queue.put_nowait(message)

    def broadcast(self, action, data):
        # @TODO: Rework this ugly monster.
        sessions = [x for x in self.app.sessions.values() if x.player in self.player.game.players]
        for session in sessions:
            session.send(action=action, data=data)


class App(Observer):
    def __init__(self):
        self.sessions = dict()
        self.games = []
        self.game2group = dict()

    def run(self):
        start_server = websockets.serve(self.handler, 'localhost', 8001)
        asyncio.get_event_loop().run_until_complete(start_server)
        asyncio.get_event_loop().run_forever()

    async def handler(self, websocket, path):
        session = Session(app=self, websocket=websocket)
        self.sessions[websocket] = session
        await session.loop()

    def create_game(self, **kwargs):
        game = Game(**kwargs)
        self.games.append(game)

        group = Group()
        group.begin()  # @@@
        group.assign(game)
        self.game2group[game] = group

        return (game, group)

    def game_group(self, game):
        return self.game2group[game]

    def unregister_session(self, session):
        self.sessions.pop(session.websocket, None)
