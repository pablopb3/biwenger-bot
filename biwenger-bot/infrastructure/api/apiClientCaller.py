from apiClient import ApiClient


class ApiClientCaller:

    def __init__(self):
        self.__cli = ApiClient()

    # wave
    def wave(self):
        return self.__cli.do_get()

    # login
    def login(self, login):
        return self.__cli.do_post('login', login)

    # config
    def update_players_alias(self):
        return self.__cli.do_get("updatePlayersAlias")

    # squad
    def get_my_player_ids(self):
        return self.__cli.do_get("getMyPlayers")["data"]

    def set_line_up(self, biwenger_line_up):
        return self.__cli.do_post("setLineUp", biwenger_line_up)

    # players
    def get_player(self, player_id):
        return self.__cli.do_get("getPlayerById", {"id": player_id})

    # league
    def get_days_to_next_round(self):
        return self.__cli.do_get("getDaysToNextRound")["data"]

    # market
    def send_players_to_market(self, place_players_to_market):
        return self.__cli.do_post("sendPlayersToMarket", place_players_to_market)

    def get_players_in_market(self):
        return self.__cli.do_get("getPlayersInMarket")["data"]

    def get_received_offers(self):
        return self.__cli.do_get("getReceivedOffers")["data"]

    def place_offer(self, offer):
        return self.__cli.do_post("placeOffer", offer)["data"]

    def accept_offer(self, offer_id):
        return self.__cli.do_get("acceptReceivedOffer?id=" + str(offer_id))["data"]

    def get_my_money(self):
        return self.__cli.do_get("getMyMoney")["data"]

    def get_max_bid(self):
        return self.__cli.do_get("getMaxBid")["data"]

    def get_market_evolution(self):
        return self.__cli.do_get("getMarketEvolution")["data"]


