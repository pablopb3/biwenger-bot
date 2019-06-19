import collections
from player import Player

FORMATION_343 = [1, 3, 4, 3]
FORMATION_352 = [1, 3, 5, 2]
FORMATION_433 = [1, 4, 3, 3]
FORMATION_442 = [1, 4, 4, 2]
FORMATION_451 = [1, 4, 5, 1]
FORMATION_532 = [1, 5, 3, 2]
FORMATION_541 = [1, 5, 4, 1]

ALL_POSSIBLE_FORMATIONS = [
    FORMATION_343,
    FORMATION_352,
    FORMATION_433,
    FORMATION_442,
    FORMATION_451,
    FORMATION_532,
    FORMATION_541
]


class LineUp:

    def __init__(self, formation, playerIds):
        self.formation = formation
        self.playersID = playerIds

    @staticmethod
    def set_best_lineup_for_formation(cli, formation):
        player_ids = LineUp.get_best_lineup_for_formation(cli, formation)
        return LineUp.set_lineup(cli, formation, player_ids)

    @staticmethod
    def set_best_lineup(cli):
        lineup = LineUp.get_best_lineup(cli)
        return LineUp.set_lineup(cli, lineup.formation, lineup.playersID)

    @staticmethod
    def get_best_lineup_for_formation(cli, formation):
        player_ids = LineUp.get_my_player_ids(cli)
        players = LineUp.get_players_from_player_ids(cli, player_ids)
        players_by_pos = LineUp.get_players_by_pos(players)
        return LineUp.get_best_lineup_player_ids_by_formation(players_by_pos, formation)

    @staticmethod
    def get_best_lineup(cli):
        player_ids = LineUp.get_my_player_ids(cli)
        players = LineUp.get_players_from_player_ids(cli, player_ids)
        players = LineUp.filter_players_ok(players)
        LineUp.order_players_by_points(players)
        return LineUp.get_best_lineup_from_ordered_players(players)

    @staticmethod
    def get_best_lineup_from_ordered_players(ordered_players):
        players_by_pos = {}
        possible_formations = ALL_POSSIBLE_FORMATIONS
        for player in ordered_players:
            if LineUp.is_player_fitable_in_lineup(player.position, players_by_pos, possible_formations):
                players_by_pos.setdefault(player.position, []).append(player)
                possible_formations = LineUp.erase_impossible_formations(players_by_pos, possible_formations)
        return LineUp(
            globals()
            ['FORMATION_'
             + str(players_by_pos[2].__len__())
             + str(players_by_pos[3].__len__())
             + str(players_by_pos[4].__len__())],
            LineUp.get_player_ids_from_selected_players_dict(players_by_pos)
        )

    @staticmethod
    def get_player_ids_from_selected_players_dict(selected_players_dict):
        dictlist = []
        for pos, players in selected_players_dict.items():
            for player in players:
                dictlist.append(player.id)
        return dictlist

    @staticmethod
    def is_player_fitable_in_lineup(player_position, players_by_pos, possible_formations):
        for formation in possible_formations:
            if player_position not in players_by_pos:
                return True
            if players_by_pos[player_position].__len__() < formation[player_position - 1]:
                return True
        return False

    @staticmethod
    def erase_impossible_formations(players_by_pos, possible_formations):
        return [x for x in possible_formations if not LineUp.should_erase_formation(x, players_by_pos)]

    @staticmethod
    def should_erase_formation(formation, players_by_pos):
        for i in range(1, 5):
            if i not in players_by_pos:
                continue
            if players_by_pos[i].__len__() > formation[i - 1]:
                return True
        return False

    @staticmethod
    def filter_players_ok(players):
        return [p for p in players if p.status == "ok"]

    @staticmethod
    def order_players_by_points(players):
        return players.sort(key=lambda x: x.points, reverse=True)

    @staticmethod
    def set_lineup(cli, formation, lineup_player_ids):
        biwenger_line_up = BiwengerLineUp(formation, lineup_player_ids)
        cli.do_post("setLineUp", biwenger_line_up)

    @staticmethod
    def get_my_player_ids(cli):
        resp = cli.do_get("getMyPlayers")
        return resp["data"]

    @staticmethod
    def get_players_from_player_ids(cli, player_ids):
        players = []
        for player_id in player_ids:
            player = Player(cli.do_get("getPlayerById", {"id": player_id}))
            players.append(player)
        return players

    @staticmethod
    def get_players_by_pos(players):
        players_by_pos = {}
        for player in players:
            players_by_pos.setdefault(player.position, []).append(player)
        return collections.OrderedDict(sorted(players_by_pos.items()))

    @staticmethod
    def get_best_lineup_player_ids_by_formation(players_by_pos, formation):
        lineup_players = []
        for key, players in players_by_pos.items():
            players = LineUp.filter_players_ok(players)
            LineUp.order_players_by_points(players)
            lineup_players.extend(players[:formation[key - 1]])
        lineup_player_ids = [p.id for p in lineup_players]
        return lineup_player_ids

class BiwengerLineUp:

    def __init__(self, formation, playerIds):
        del formation[0]
        self.type = '-'.join([str(i) for i in formation])
        self.playersID = playerIds