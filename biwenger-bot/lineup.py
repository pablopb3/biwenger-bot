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

MIN_PLAYERS_BY_POS = [1, 5, 4, 2]


class LineUp:

    def __init__(self, cli, formation=None, player_ids=None):
        self.cli = cli
        self.formation = formation
        self.player_ids = player_ids

    def set_best_lineup(self):
        lineup = self.get_best_lineup()
        return self.set_lineup(lineup.formation, lineup.player_ids)

    def get_my_players(self):
        player_ids = self.get_my_player_ids()
        return Player.get_players_from_player_ids(self.cli, player_ids)

    def get_best_lineup(self):
        players = self.get_my_players()
        self.order_players_by_lineup_points(players)
        return self.get_best_lineup_from_ordered_players(players)

    def get_my_player_ids(self):
        resp = self.cli.do_get("getMyPlayers")
        return resp["data"]

    def filter_players_ok(self, players):
        return [p for p in players if p.status == "ok"]

    def order_players_by_lineup_points(self, players):
        return players.sort(key=lambda x: x.lineup_points, reverse=True)

    def order_players_by_assure_points(self, players):
        return players.sort(key=lambda x: x.assure_points, reverse=True)

    def order_players_by_position(self, players):
        return players.sort(key=lambda x: x.position)

    def get_best_lineup_from_ordered_players(self, ordered_players):
        players_by_pos = {}
        possible_formations = ALL_POSSIBLE_FORMATIONS
        for player in ordered_players:
            if self.is_player_fitable_in_lineup(player.position, players_by_pos, possible_formations):
                players_by_pos.setdefault(player.position, []).append(player)
                possible_formations = self.erase_impossible_formations(players_by_pos, possible_formations)
        formation = "{0}{1}{2}".\
            format(str(players_by_pos[2].__len__()),
                   str(players_by_pos[3].__len__()),
                   str(players_by_pos[4].__len__()))
        formation_const = 'FORMATION_' + formation
        #print("Line up decided : " + formation + ". ")
        #print(', '.join(players_by_pos.name))
        return LineUp(
            self.cli,
            globals()[formation_const],
            self.get_player_ids_from_selected_players_dict(players_by_pos)
        )

    def get_best_lineup_for_formation(self, formation):
        player_ids = self.get_my_player_ids()
        players = self.get_players_from_player_ids(player_ids)
        players_by_pos = self.get_players_by_pos(players)
        return self.get_best_lineup_player_ids_by_formation(players_by_pos, formation)

    def set_best_lineup_for_formation(self, formation):
        player_ids = self.get_best_lineup_for_formation(formation)
        return self.set_lineup(formation, player_ids)

    def get_player_ids_from_selected_players_dict(self, selected_players_dict):
        dictlist = []
        selected_players_dict
        for pos, players in sorted(selected_players_dict.items()):
            for player in players:
                dictlist.append(player.id)
        return dictlist

    def is_player_fitable_in_lineup(self, player_position, players_by_pos, possible_formations):
        for formation in possible_formations:
            if player_position not in players_by_pos:
                return True
            if players_by_pos[player_position].__len__() < formation[player_position - 1]:
                return True
        return False

    def erase_impossible_formations(self, players_by_pos, possible_formations):
        return [x for x in possible_formations if not self.should_erase_formation(x, players_by_pos)]

    def should_erase_formation(self, formation, players_by_pos):
        for i in range(1, 5):
            if i not in players_by_pos:
                continue
            if players_by_pos[i].__len__() > formation[i - 1]:
                return True
        return False

    def set_lineup(self, formation, lineup_player_ids):
        biwenger_line_up = BiwengerLineUp(formation, lineup_player_ids)
        self.cli.do_post("setLineUp", biwenger_line_up)

    def get_players_by_pos(self, players):
        players_by_pos = {}
        for player in players:
            players_by_pos.setdefault(player.position, []).append(player)
        return collections.OrderedDict(sorted(players_by_pos.items()))

    def get_best_lineup_player_ids_by_formation(self, players_by_pos, formation):
        lineup_players = []
        for key, players in players_by_pos.items():
            players = self.filter_players_ok(players)
            self.order_players_by_lineup_points(players)
            lineup_players.extend(players[:formation[key - 1]])
        lineup_player_ids = [p.id for p in lineup_players]
        return lineup_player_ids


class BiwengerLineUp:

    def __init__(self, formation, player_ids):
        del formation[0]
        self.type = '-'.join([str(i) for i in formation])
        self.playersID = player_ids
