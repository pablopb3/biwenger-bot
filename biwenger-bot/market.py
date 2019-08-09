from player import Player
from prices_predictor import PricesPredictor

class Market:

    def __init__(self, cli):
        self.cli = cli
        self.prices_predictor = PricesPredictor()
        self.received_offers_from_computer = self.get_received_offers_from_computer()
        self.days_to_next_round = self.get_days_to_next_round()
        self.players_in_market_from_computer = Player.get_players_from_player_ids(
            self.cli, self.get_players_ids_from_players_in_market_from_computer()
        )
        self.available_money = self.get_my_money()
        self.max_bid = self.get_max_bid()
        self.market_evolution = self.get_market_evolution()

    def place_offers_for_players_in_market(self):
        for player_in_market in self.players_in_market_from_computer:
            print("studying to make a bid for " + player_in_market.name)
            player_price = player_in_market.price
            predicted_price = self.prices_predictor.predict_price(player_in_market)
            if self.should_place_offer(player_price, predicted_price):
                bid_price = self.calculate_bid_price(player_price, predicted_price)
                print("decided to make a bid for " + player_in_market.name + " for " + str(bid_price) + "$")
                self.place_offer(player_in_market.id, bid_price)

    def study_offers_for_my_players(self):
        if self.received_offers_from_computer:
            for received_offer in self.received_offers_from_computer:
                player_id = received_offer["idPlayer"]
                player = Player.get_player_from_player_id(self.cli, player_id)
                current_price = player.price
                prediction_price = self.prices_predictor.predict_price(player)
                offer_price = received_offer["ammount"]
                if self.should_accept_offer(current_price, prediction_price, offer_price):
                    self.accept_offer(received_offer["idOffer"])

    def place_all_my_players_to_market(self, price):
        place_players_to_market = PlacePlayersToMarket(price)
        self.cli.do_post("sendPlayersToMarket", place_players_to_market)

    def should_accept_offer(self, player_price, predicted_price, offer_price):
        if predicted_price < 0.85*player_price and offer_price > player_price:
            return True
        return False

    def should_place_offer(self, player_price, predicted_price):
        return predicted_price > 1.15*player_price and player_price < 5000000

    def calculate_bid_price(self, player_price, predicted_price):
        diff_price = predicted_price - player_price
        corrected_diff_price = diff_price*0.3
        return int(player_price + corrected_diff_price)

    def accept_offer(self, offer_id):
        return self.cli.do_get("acceptReceivedOffer?id=" + offer_id)["data"]

    def place_offer(self, player_id, bid_price):
        offer = PlaceOffer(bid_price, [player_id], None, "purchase")
        return self.cli.do_post("placeOffer", offer)["data"]

    def get_days_to_next_round(self):
        return self.cli.do_get("getDaysToNextRound")["data"]

    def get_received_offers(self):
        return self.cli.do_get("getReceivedOffers")["data"]

    def get_received_offers_from_computer(self):
        received_offers = self.get_received_offers()
        if received_offers is not None:
            return[x for x in received_offers if x["idUser"] == 0]

    def get_players_ids_from_players_in_market_from_computer(self):
        return [p['idPlayer'] for p in self.get_players_in_market_from_computer_with_price()]

    def get_players_in_market_with_price(self):
        return self.cli.do_get("getPlayersInMarket")["data"]

    def get_players_in_market_from_computer_with_price(self):
        return [p for p in self.get_players_in_market_with_price() if p["idUser"] == 0]

    def get_my_money(self):
        return self.cli.do_get("getMyMoney")["data"]

    def get_max_bid(self):
        return self.cli.do_get("getMaxBid")["data"]

    def get_market_evolution(self):
        return self.cli.do_get("getMarketEvolution")["data"]


class PlacePlayersToMarket:

    def __init__(self, price):
        self.price = price


class PlaceOffer:

    def __init__(self, amount, requested_players, to, type):
        self.amount = amount
        self.requestedPlayers = requested_players
        self.to = to
        self.type = type

