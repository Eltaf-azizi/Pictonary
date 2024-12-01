"""
Handles operations related to game and connections
between player, board, chat, and round
"""
import random
from board import Board
from round import Round

class Game(object):

    def __init__(self, id, players):
        """
        Init the game once the player threshold is met.
        :param id: int
        :param players: Player[]
        """
        self.id = id
        self.players = players
        self.words_used = set()
        self.round = None
        self.board = Board()
        self.player_draw_ind = 0
        self.round_count = 1
        self.start_new_round()

    def start_new_round(self):
        """
        Starts a new round with a new word.
        :return: None
        """
        try:
            self.round = Round(self.get_word(), self.players[self.player_draw_ind], self)
            self.round_count += 1

            # Check if the player_draw_ind exceeds the number of players
            if self.player_draw_ind >= len(self.players):
                self.round_ended()
                self.end_game()

            self.player_draw_ind += 1
        except Exception as e:
            print(f"Error starting new round: {e}")
            self.end_game()

    def player_guess(self, player: Player, guess: str) -> bool:
        """
        Makes the player guess the word.
        :param player: Player
        :param guess: str
        :return: bool
        """
        return self.round.guess(player, guess)

    def player_disconnected(self, player: Player):
        """
        Cleans up objects when a player disconnects.
        :param player: Player
        :raises: Exception
        """
        if player in self.players:
            self.players.remove(player)
            self.round.player_left(player)
            self.round.chat.update_chat(f"Player {player.get_name()} disconnected.")
        else:
            raise Exception("Player not in game")

        if len(self.players) <= 2:
            self.end_game()

    def get_player_scores(self):
        """
        Returns a dict of player scores.
        :return: dict
        """
        scores = {player.get_name(): player.get_score() for player in self.players}
        return scores

    def skip(self, player: Player):
        """
        Increments the round skips; if skips are greater than the threshold, starts a new round.
        :return: None
        """
        if self.round:
            new_round = self.round.skip(player)
            if new_round:
                self.round.chat.update_chat(f"Round has been skipped.")
                self.round_ended()
                return True
            return False
        else:
            raise Exception("No round started yet!")

    def round_ended(self):
        """
        Called when the round ends.
        :return: None
        """
        self.round.chat.update_chat(f"Round {self.round_count} has ended.")
        self.start_new_round()
        self.board.clear()

    def update_board(self, x: int, y: int, color: int):
        """
        Calls update method on the board.
        :param x: int
        :param y: int
        :param color: 0-8
        :return: None
        """
        if not self.board:
            raise Exception("No board created")
        self.board.update(x, y, color)

    def end_game(self):
        """
        Ends the game.
        :return: None
        """
        print(f"[GAME] Game {self.id} ended")
        for player in self.players:
            player.game = None

    def get_word(self) -> str:
        """
        Returns a word that has not yet been used.
        :return: str
        """
        with open("words.txt", "r") as f:
            words = []

            for line in f:
                wrd = line.strip()
                if wrd not in self.words_used:
                    words.append(wrd)

        if not words:
            raise Exception("No more words available.")

        wrd = random.choice(words)
        self.words_used.add(wrd)

        return wrd