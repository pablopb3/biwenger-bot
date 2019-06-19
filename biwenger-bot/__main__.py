from login import Login
from lineup import LineUp
from lineup import FORMATION_442
from config import Config
from biwengerApiClient import BiwengerApiClient


def main():
    config = Config()
    print(config.get_param('Wave', 'init.message'))
    cli = do_login(config)
    wave_api(cli)
    LineUp.set_best_lineup(cli)
    #LineUp.set_best_lineup_for_formation(cli, FORMATION_442)


def wave_api(cli):
    cli.do_get("")


def do_login(config):
    return BiwengerApiClient(
        config.get_param('Credentials', 'biwenger.mail'),
        config.get_param('Credentials', 'biwenger.pass'),
    )


if __name__ == '__main__':
    main()
