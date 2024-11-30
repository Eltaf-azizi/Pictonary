"""
Represents a round of the game, storing things like word,
time, skips, drawing player and more.
"""

import time as t
from _thread import *
from game import Game
from chat import Chat

class Round(object):
    def __init__(self, word, player_drawing, game):

        """
        init object
        :param word: str
        :param playerdrawing: Player
        :param players: Player[]
        """
        self.word = word
        self.player_drawing = player_drawing
        self.player_guessed = []
        self.players_skipped = []
        self.skips = 0
        self.time = 74
        self.game = game
        self.player_scores = {player:0 for player in self.game.players}
        self.chat = Chat(self)
        start_new_thread( self.time_thread, ())

    def skip(self, player):
        """
        Return true if round skipped threshold met
        :return: bool
        """

        if player not in self.players_skipped:
            self.players_skipped.append(player)
            self.skips += 1
            self.chat.update_chat(f"Player has votes to skip ({self.skips}/{len(self.game.players) -2})")
            

        if self.skip >= len(self.game.player) - 2:
            return True
        
        return False
    

    def getscores(self):
        """
        :returns all the player scores
        """
        return self.player_scores
    
    def score(self, player):
        """
        gets aspecific players scores
        :param player: Player
        :return: int
        """
        if player in self.player_scores:
            return self.player_scores[player]
        
        else:
            raise Exception("Player not in score list")

    def time_thread(self):
        """
        removes player that left from scores and list
        :param player: Player
        :return: None
        """

        while self.time > 0:
            t.sleep(1)
            self.time -= 1
            self.end_round("Time is up")


    def guess(self, player , wrd):
        
        """
        :returns bool if player got guess correct
        :param player: Player
        :param wed: str
        :return: bool
        """
        correct = wrd == self.wrd
        if correct:
            self.player_guessed.append(player)
            # TODO implement scoring system here
            self.chat.update_chat(f"{player.name} guessed the word.")
            return True
        
        self.chat.update_chat(f"{player.name} guessed {wrd}")
        return False
    
    def player_left(self, player):
        """
        removes player that left from scores and list
        :param player: Player
        :return: None
        """
        if player in self.player_scores:
            del self.player_scores[player]

        if player in self.player_guessed:
            self.player_guessed.remove(player)
            self.end_round("Drawing player leaves")

        if player == self.player_drawing:
            self.chat.update_chat("Round has been skipped because the drawer left.")
            self.end_round("Drawing player leaves")

    def end_round(self, msg):
        for player in self.game.player:
            if self in self.player_scores:
                player.update_score(self.player_scores[player])
        self.game.round_ended()