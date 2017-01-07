from oil.game import Game
from oil.player import Player
from oil.observer import Observer
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
        self.send_queue = []
        self._player = None

    async def loop(self):
        try:
            while True:
                data = json.loads(await self.websocket.recv())
                await self.consumer(data)
        finally:
            self.app.unregister_session(self)

    async def consumer(self, data):
        if data["action"] == "set_name":
            await self.set_name(data["data"])
        elif data["action"] == "create_game":
            await self.create_game(data["data"])
        elif data["action"] == "join_game":
            await self.join_game(data["data"])
        elif data["action"] == "start_game":
            await self.start_game(data["data"])

    async def set_name(self, data):
        self.name = data["name"]
        await self.send("games", self.app.games)

    async def create_game(self, data):
        game = Game(initial_balance=data["initial_balance"])
        self.app.register_game(game)

        self.player = game.create_player(name=self.name)
#        await session.send("me", session.player.api_data)
#        await session.send("game", game.api_data)

    async def join_game(self, data):
        games = filter(lambda x: x.uuid == data["uuid"], self.app.games)
        assert(len(games) == 1)
        game = games[0]

        self.player = game.create_player(name=self.name)
#
#        await session.send("me", session.player.api_data)
#        await self.game_broadcast(game, "game", game.api_data)

    @property
    def player(self):
        return self._player

    @player.setter
    def player(self, player):
        self._player = player
        self.observe(self._player)
        self.observe(self._player.game)

    def notify(self, observable, event):
        done, pending = yield from asyncio.wait(self._notify)

    async def _notify(self, observable, event):
        pass
    #    if isinstance(observable, Player):
    #        if observable == self.player:
    #            await self.send("me", self.player)

    def api_dump(self, data):
        if isinstance(data, list):
            return [self.api_dump(item) for item in data]
        else:
            if hasattr(data, "api_data"):
                return data.api_data()
            else:
                return data

    async def send(self, action, data):
        await self.websocket.send(
            json.dumps(
                dict(
                    action=action,
                    data=self.api_dump(data)
                )
            )
        )

    async def broadcast(self, action, data):
        # @TODO: Rework this ugly monster.
        sessions = [x for x in self.app.sessions.values() if x.player in self.player.game.players]
        for session in sessions:
            await session.send(action=action, data=data)


class App(Observer):
    def __init__(self):
        self.sessions = dict()
        self.games = []

    def notify(self, observable, event):
        if isinstance(observable, Game):
            pass

        print(event)

    async def game_broadcast(self, game, action, data):
        sessions = [x for x in self.sessions.values() if x.player in game.players]
        for session in sessions:
            await session.send(action=action, data=data)

    def game_by_uuid(self, uuid):
        return [x for x in self.games if str(x.uuid) == uuid][0]

    def run(self):
        start_server = websockets.serve(self.handler, 'localhost', 8001)
        asyncio.get_event_loop().run_until_complete(start_server)
        asyncio.get_event_loop().run_forever()

    async def start_game(self, session, data):
        assert(session.player)
        assert(session.name)

        await self.game_broadcast(
            game=session.player.game,
            action="estates",
            data=[x.api_data for x in session.player.game.estates]
        )

        session.player.game.started = True
        await self.game_broadcast(session.player.game, "game", session.player.game.api_data)
        print("Session {} started game {}.".format(session.uuid, session.player.game.uuid))

    async def handler(self, websocket, path):
        session = Session(app=self, websocket=websocket)
        self.sessions[websocket] = session
        await session.loop()

    def register_game(self, game):
        self.games.append(game)

    def unregister_session(self, session):
        self.sessions.pop(session.websocket, None)
