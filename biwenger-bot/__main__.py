from login import Login
from market import Market
from lineup import LineUp
from lineup import FORMATION_442
from config import Config
from biwengerApiClient import BiwengerApiClient
from prices_predictor import PricesPredictor
from player import Player

def main():
    config = Config()
    wave(config)
    cli = do_login(config)
    config.update_players_alias(cli)
    line_up = LineUp(cli)
    line_up.set_best_lineup()
    market = Market(cli)
    #market.study_offers_for_my_players()
    market.place_offers_for_players_in_market()
    wave_api(cli)

    print("======== ======== CONFIG BUSINESS STARTED ======== ========")
    print("======== Getting all alias information from players in league ========")

    print("======== All alias information from players got ========")
    print("======== ======== CONFIG BUSINESS ENDED ======== ========")

    print("======== ======== MARKET BUSINESS STARTED ======== ========")
    print("======== Sending all my players to market ========")
    market.place_all_my_players_to_market(125)
    print("======== All my players on sale on market ========")
    print("======== Placing offers at players in market ========")

    print("======== Offers placed to players in market ========")
    print("======== ======== MARKET BUSINESS ENDED ======== ========")

    print("======== ======== LINEUP BUSINESS STARTED ======== ========")
    print("======== Starting to set best possible line up ========")
    print("======== Best possible line up set ========")
    print("======== ======== LINEUP BUSINESS ENDED ======== ========")

    # LineUp.set_best_lineup_for_formation(cli, FORMATION_442)


def wave_api(cli):
    cli.do_get("")


def wave(config):
    print(config.get_param('Wave', 'init.message'))


def do_login(config):
    return BiwengerApiClient(
        config.get_param('Credentials', 'biwenger.mail'),
        config.get_param('Credentials', 'biwenger.pass'),
    )


if __name__ == '__main__':
    main()
