class Player:

    def __init__(self, data):
        self.id = data["data"]["data"]["id"]
        self.name = data["data"]["data"]["name"]
        self.position = data["data"]["data"]["position"]
        self.price = data["data"]["data"]["price"]
        self.points = data["data"]["data"]["points"]
        self.points_last_season = data["data"]["data"]["pointsLastSeason"]
        self.status = data["data"]["data"]["status"]

    def __str__(self):
        return self.name

    @staticmethod
    def get_players_from_player_ids(cli, player_ids):
        players = []
        for player_id in player_ids:
            player = Player(cli.do_get("getPlayerById", {"id": player_id}))
            players.append(player)
        return players
