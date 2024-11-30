"""
Represents a player object on the server side
"""

class Player(object):
    def __init__(self, ip, name):
        """
        Initialize the player object
        :param ip: str
        :param name: str
        """
        self.game = None
        self.ip = ip
        self.name = name
        self.score = 0

    def set_game(self, game):
        """
        Sets the player's game association
        :param game: Game
        :return: None
        """
        self.game = game

    def update_score(self, x):
        """
        Updates a player's score
        :param x: int
        :return: None
        """
        self.score += x

    def guess(self, wrd):
        """
        Makes a player guess
        :param wrd: str
        :return: bool
        """
        if self.game:
            return self.game.player_guess(self, wrd)
        return False

    def disconnect(self):
        """
        Call to disconnect player
        :return: None
        """
        if self.game:
            self.game.player_disconnected(self)

    def get_ip(self):
        """
        Gets player IP address
        :return: str
        """
        return self.ip

    def get_name(self):
        """
        Gets player name
        :return: str
        """
        return self.name

    def get_score(self):
        """
        Gets player score
        :return: int
        """
        return self.score