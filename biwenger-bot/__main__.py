from ApiClientCaller import ApiClientCaller
from login import Login
from market import Market
from lineup import LineUp
from lineup import FORMATION_442
from config import Config
from prices_predictor import PricesPredictor
from player import Player
import datetime


def main():
    print("~~~~~~~~~~~ STARTING EXECUTION FOR DAY " + get_formated_time() + "~~~~~~~~~~~")

    cli = ApiClientCaller()

    wave()
    wave_api(cli)

    Config.update_db(cli)

    print("======== ======== MARKET BUSINESS STARTED ======== ========")
    line_up = LineUp(cli)
    market = Market(cli, line_up)

    print("======== Sending all my players to market ========")
    market.place_all_my_players_to_market(500)
    print("======== All my players on sale on market ========")

    print("======== Studying received offers for my players ========")
    market.study_offers_for_my_players()
    print("======== All the received offers were studied ========")

    print("======== Placing offers at players in market ========")
    market.place_offers_for_players_in_market()
    print("======== Offers placed to players in market ========")

    print("======== Assure positive balance before start of next round")
    market.assure_positive_balance_before_next_round()
    print("======== Assured positive balance before start of next round")

    print("======== ======== MARKET BUSINESS ENDED ======== ========")

    print("======== ======== LINEUP BUSINESS STARTED ======== ========")
    line_up = LineUp(cli)
    print("======== Starting to set best possible line up ========")
    try:
        line_up.set_best_lineup()
    except Exception as e:
        print("An error ocurred while setting the best lineup: " + str(e))
    print("======== Best possible line up set ========")
    print("======== ======== LINEUP BUSINESS ENDED ======== ========")
    print("~~~~~~~~~~~ ENDED EXECUTION FOR DAY " + get_formated_time() + "~~~~~~~~~~~")


def wave():
    config = Config()
    print(config.wave())


def wave_api(cli: ApiClientCaller):
    print(cli.wave())


def get_formated_time():
    return datetime.datetime.now().strftime('%d-%b-%G at %H:%M:%S')


if __name__ == '__main__':
    main()
