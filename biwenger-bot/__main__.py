from login import Login
from lineup import LineUp
from config import Config
from biwengerApiClient import BiwengerApiClient

FORMATION = [1, 4, 4, 2]


def main():
    config = Config()
    print(config.get_param('Wave', 'init.message'))
    cli = do_login(config)
    wave_api(cli)
    lineup_player_ids = LineUp.get_player_ids_to_lineup(cli, FORMATION)
    LineUp.set_lineup(cli, FORMATION, lineup_player_ids)


def wave_api(cli):
    cli.do_get("")


def do_login(config):
    return BiwengerApiClient(
        config.get_param('Credentials', 'biwenger.mail'),
        config.get_param('Credentials', 'biwenger.pass'),
    )


if __name__ == '__main__':
    main()
