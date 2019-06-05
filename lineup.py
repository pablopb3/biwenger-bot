import collections
from player import Player


class LineUp:

    def __init__(self, formation, playerIds):
        del formation[0]
        self.type = '-'.join([str(i) for i in formation])
        self.playersID = playerIds

    @staticmethod
    def set_lineup(cli, formation, lineup_player_ids):
        lineup = LineUp(formation, lineup_player_ids)
        cli.do_post("setLineUp", lineup)

    @staticmethod
    def get_player_ids_to_lineup(cli, formation):
        player_ids = LineUp.get_my_player_ids(cli)
        players_by_pos = {}
        players = []
        lineup_players = []
        for player_id in player_ids:
            player = Player(cli.do_get("getPlayerById", {"id": player_id}))
            players.append(player)
            players_by_pos.setdefault(player.position, []).append(player)
        players_by_pos = collections.OrderedDict(sorted(players_by_pos.items()))
        for key, players in players_by_pos.items():
            players = [p for p in players if p.status == "ok"]
            players.sort(key=lambda x: x.points, reverse=True)
            lineup_players.extend(players[:formation[key - 1]])
        lineup_player_ids = [p.id for p in lineup_players]
        return lineup_player_ids

    @staticmethod
    def get_my_player_ids(cli):
        resp = cli.do_get("getMyPlayers")
        return resp["data"]



