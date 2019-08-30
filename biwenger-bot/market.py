from player import Player
import math
from lineup import LineUp
from numpy import interp, mean
from prices_predictor import PricesPredictor
from lineup import MIN_PLAYERS_BY_POS

MAX_MONEY_AT_BANK = 20000000


class Market:

    def __init__(self, cli, line_up):
        self.cli = cli
        self.prices_predictor = PricesPredictor()
        self.my_squad = line_up.get_my_players()
        self.my_players_by_pos = line_up.get_players_by_pos(self.my_squad)
        self.min_players_by_pos = MIN_PLAYERS_BY_POS
        self.received_offers_from_computer = self.get_received_offers_from_computer()
        self.days_to_next_round = self.get_days_to_next_round()
        self.players_in_market_from_computer = Player.get_players_from_player_ids(
            self.cli, self.get_players_ids_from_players_in_market_from_computer()
        )
        self.available_money = self.get_my_money()
        self.max_bid = self.get_max_bid()
        self.market_evolution = self.get_market_evolution()
        self.bided_today = 0
        self.buying_aggressivity = self.calculate_buying_aggressivity()
        self.selling_aggressivity = 10 - self.buying_aggressivity
        self.max_player_price_to_bid_for = 5000000 + self.buying_aggressivity * 500000
        self.min_buying_points_to_bid = 15 - self.buying_aggressivity * 8 / 10
        self.percentage_to_set_bid_price = 0.2 + self.buying_aggressivity / 10
        self.percentage_to_accept_offer = 0.88 + self.selling_aggressivity * 0.04 / 10
        self.team_points_mean = round(mean([p.points_mean for p in self.my_squad]), 4)
        self.team_points_mean_per_million = round(mean([p.points_mean_per_million for p in self.my_squad]), 4)

    def place_offers_for_players_in_market(self):
        for player_in_market in self.players_in_market_from_computer:
            print("studying to make a bid for " + player_in_market.name)
            predicted_price = self.prices_predictor.predict_price(player_in_market)
            player_in_market.buying_points = self.get_buying_points(player_in_market, predicted_price)
            if self.should_place_offer(player_in_market):
                bid_price = self.calculate_bid_price(player_in_market)
                if self.do_i_have_money_to_bid(bid_price):
                    print("decided to make a bid for " + player_in_market.name + " for " + str(bid_price) + "$")
                    self.place_offer(player_in_market.id, bid_price)

    def study_offers_for_my_players(self):
        if self.received_offers_from_computer:
            for received_offer in self.received_offers_from_computer:
                player_id = received_offer["idPlayer"]
                player = Player.get_player_from_player_id(self.cli, player_id)
                print("studying to accept offer for " + player.name)
                if not self.is_min_players_by_pos_guaranteed(player):
                    continue
                prediction_price = self.prices_predictor.predict_price(player)
                player.buying_points = self.get_buying_points(player, prediction_price)
                offer_price = received_offer["ammount"]
                if self.should_accept_offer(player):
                    print("decided to accept offer for  " + player.name + " for " + str(offer_price) + "$")
                    self.accept_offer(received_offer["idOffer"])

    def place_all_my_players_to_market(self, price):
        place_players_to_market = PlacePlayersToMarket(price)
        self.cli.do_post("sendPlayersToMarket", place_players_to_market)

    def should_accept_offer(self, player):
        if player.buying_points is not None and player.buying_points < -20:
            return True
        return False

    def should_place_offer(self, player):
        return player.buying_points is not None and player.buying_points > self.min_buying_points_to_bid and player.price < self.max_player_price_to_bid_for

    def calculate_bid_price(self, player):
        player_millions_value = int(player.price/1000000)
        expensive_corrector_factor = 1-player_millions_value*0.015
        bid_percentage_to_multiply = float(interp(player.buying_points, [0, 10, 25, 75, 100], [0, 1.05, 1.10, 1.15, 1.20]))*expensive_corrector_factor
        return int(player.price*bid_percentage_to_multiply)

    def accept_offer(self, offer_id):
        return self.cli.do_get("acceptReceivedOffer?id=" + str(offer_id))["data"]

    def place_offer(self, player_id, bid_price):
        offer = PlaceOffer(bid_price, [player_id], None, "purchase")
        self.cli.do_post("placeOffer", offer)["data"]
        self.bided_today += bid_price

    def is_min_players_by_pos_guaranteed(self, player: Player):
        players_in_this_pos = len(self.my_players_by_pos[player.position])
        min_players_in_this_pos = self.min_players_by_pos[player.position - 1]
        if players_in_this_pos <= min_players_in_this_pos:
            print("don't sell " + str(player.name) +
                  "! We just have " + str(players_in_this_pos) + " players in this position. " +
                  "At least " + str(min_players_in_this_pos) + " are required. ")
            return False
        return True

    def calculate_buying_aggressivity(self):
        buy_aggr_by_money = self.available_money / MAX_MONEY_AT_BANK * 10
        buy_aggr_by_days = round(math.cos(4 * self.days_to_next_round / (2 * math.pi)), 2)
        if self.days_to_next_round > 10:
            buy_aggr_by_days = 1
        buy_aggr = round(buy_aggr_by_money + buy_aggr_by_days)
        return buy_aggr

    def get_buying_points(self, player: Player, predicted_price):
        diff_price_weight = 0.7
        diff_points_mean_weight = 0.2
        diff_points_per_million_weight = 0.1
        percentage_diff = (predicted_price - player.price) / player.price * 100
        normalized_diff = min(max(((percentage_diff) ** 3) / 20, -100), 100)

        normalized_points_per_million = float(interp(player.points_mean_per_million, [0, self.team_points_mean_per_million, 10], [-100, 0, 100]))

        normalized_points_mean = float(interp(player.points_mean, [0, self.team_points_mean, 10], [-100, 0, 100]))

        return round(diff_price_weight * normalized_diff + \
               diff_points_per_million_weight * normalized_points_per_million + \
               diff_points_mean_weight * normalized_points_mean, 4)

    def get_days_to_next_round(self):
        return self.cli.do_get("getDaysToNextRound")["data"]

    def get_received_offers(self):
        return self.cli.do_get("getReceivedOffers")["data"]

    def get_received_offers_from_computer(self):
        received_offers = self.get_received_offers()
        if received_offers is not None:
            return [x for x in received_offers if x["idUser"] == 0]

    def do_i_have_money_to_bid(self, bid_price):
        return self.available_money - self.bided_today - bid_price > 0

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
