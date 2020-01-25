class LineUp:

    def __init__(self, formation, player_ids):
        del formation[0]
        self.type = '-'.join([str(i) for i in formation])
        self.playersID = player_ids