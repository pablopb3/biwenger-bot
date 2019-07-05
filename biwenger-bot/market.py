from player import Player

class Market:

    def __init__(self, cli):
        self.cli = cli
        self.players_in_market = Player.get_players_from_player_ids(self.cli, self.get_players_ids_from_players_in_market())
        self.available_money = self.get_my_money()
        self.max_bid = self.get_max_bid()
        self.market_evolution = self.get_market_evolution()

    def place_offers_for_players_in_market(self):
        self.players_in_market

    def place_all_my_players_to_market(self, price):
        place_players_to_market = PlacePlayersToMarket(price)
        self.cli.do_post("sendPlayersToMarket", place_players_to_market)

    def get_players_ids_from_players_in_market(self):
        return [p['idPlayer'] for p in self.get_players_in_market_with_price()]

    def get_players_in_market_with_price(self):
        return self.cli.do_get("getPlayersInMarket")["data"]

    def get_my_money(self):
        return self.cli.do_get("getMyMoney")["data"]

    def get_max_bid(self):
        return self.cli.do_get("getMaxBid")["data"]

    def get_market_evolution(self):
        return self.cli.do_get("getMarketEvolution")["data"]


class PlacePlayersToMarket:

    def __init__(self, price):
        self.price = price


