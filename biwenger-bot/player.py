WEIGHT_MARKET_VALUE = 0.4
WEIGHT_POINTS = 0.5
WEIGHT_POINTS_LAST_SEASON = 0.1

MAX_POINTS_LAST_SEASON = 473
MAX_POINTS_MEAN_LAST_SEASON = 13.9


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
        self.played_home = data["data"]["data"]["playedHome"]
        self.played_away = data["data"]["data"]["playedAway"]
        self.points_home = data["data"]["data"]["pointsHome"]
        self.points_away = data["data"]["data"]["pointsAway"]

        self.played_matches = self.played_home + self.played_away
        self.points_mean = self.get_points_mean(self.points, self.played_matches)
        self.bot_points = Player.get_bot_points_for_player(self)

    def __str__(self):
        return self.name

    @staticmethod
    def get_points_mean(points, played_matches):
        if played_matches == 0:
            return 0
        else:
            return points / played_matches

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

    @staticmethod
    def get_bot_points_for_player(player):
        if player.status == 'ok':
            return Player.get_bot_points_player_ok(player)
        elif player.status == 'doubt':
            return -0.5
        elif player.status == 'injured' or 'suspended':
            return -1

    @staticmethod
    def get_bot_points_player_ok(player):
        normalized_price = Player.normalize_price(player.price)
        normalized_points = Player.normalize_points_mean(player.points_mean)
        normalized_points_last_season = Player.normalize_points(player.points_last_season)
        return round(
            WEIGHT_MARKET_VALUE * normalized_price +
            WEIGHT_POINTS * normalized_points +
            WEIGHT_POINTS_LAST_SEASON * normalized_points_last_season
            , 4)

    @staticmethod
    def normalize_price(price):
        return min(price / 10000000, 1)

    @staticmethod
    def normalize_points(points):
        return min(points / MAX_POINTS_LAST_SEASON, 1)

    @staticmethod
    def normalize_points_mean(points_mean):
        return min(points_mean / MAX_POINTS_MEAN_LAST_SEASON, 1)
