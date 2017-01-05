from oil.game import Game
import websockets
import asyncio
import json
import uuid


class Session:
    def __init__(self, websocket):
        self.websocket = websocket
        self.name = None
        self.uuid = uuid.uuid4()
        self.player = None

    async def send(self, action, data):
        await self.websocket.send(
            json.dumps(
                dict(
                    action=action,
                    data=data
                )
            )
        )


class App:
    def __init__(self):
        self.sessions = dict()
        self.games = []

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

    async def set_name(self, session, data):
        assert(not session.player)

        session.name = data["name"]
        await session.send("games", [x.api_data() for x in self.games if not x.started])
        print("Session {} changed name to {}.".format(session.uuid, session.name))

    async def create_game(self, session, data):
        assert(not session.player)
        assert(session.name)
        assert(isinstance(data["initial_balance"], int))
        assert(data["initial_balance"] >= 0)

        game = Game(initial_balance=data["initial_balance"])
        game.owner = session.player
        self.games.append(game)

        session.player = game.create_player(name=session.name)
        game.owner = session.player

        await session.send("me", session.player.api_data())
        await session.send("game", game.api_data())

        print("Session {} created game {}.".format(session.uuid, game.uuid))

    async def join_game(self, session, data):
        assert(not session.player)
        assert(session.name)

        games = [x for x in self.games if str(x.uuid) == data["uuid"]]
        assert(len(games) == 1)
        game = games[0]

        session.player = game.create_player(name=session.name)

        await session.send("me", session.player.api_data())
        await self.game_broadcast(game, "game", game.api_data())

    async def start_game(self, session, data):
        assert(session.player)
        assert(session.name)

        await self.game_broadcast(
            game=session.player.game,
            action="estates",
            data=[x.api_data() for x in session.player.game.estates]
        )

        session.player.game.started = True
        await session.send("game", session.player.game.api_data())
        print("Session {} started game {}.".format(session.uuid, session.player.game.uuid))

    async def consumer(self, session, data):
        if data["action"] == "set_name":
            await self.set_name(session, data["data"])
        elif data["action"] == "create_game":
            await self.create_game(session, data["data"])
        elif data["action"] == "join_game":
            await self.join_game(session, data["data"])
        elif data["action"] == "start_game":
            await self.start_game(session, data["data"])

    async def handler(self, websocket, path):
        session = Session(websocket)
        self.sessions[websocket] = session

        try:
            while True:
                data = json.loads(await websocket.recv())
                await self.consumer(session, data)
        finally:
            self.sessions.pop(websocket, None)
