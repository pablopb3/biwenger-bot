class Player:

    def __init__(self, data):
        self.id = data["data"]["data"]["id"]
        self.name = data["data"]["data"]["name"]
        self.position = data["data"]["data"]["position"]
        self.price = data["data"]["data"]["price"]
        self.points = data["data"]["data"]["points"]
        self.points_last_season = data["data"]["data"]["pointsLastSeason"]
        self.status = data["data"]["data"]["status"]
        self.price_increment = data["data"]["data"]["priceIncrement"]
        self.prices = data["data"]["data"]["prices"]

    def __str__(self):
        return self.name

    @staticmethod
    def get_players_from_player_ids(cli, player_ids):
        players = []
        for player_id in player_ids:
            player = Player.get_player_from_player_id(cli, player_id)
            players.append(player)
        return players

    @staticmethod
    def get_player_from_player_id(cli, player_id):
        return Player(cli.do_get("getPlayerById", {"id": player_id}))
