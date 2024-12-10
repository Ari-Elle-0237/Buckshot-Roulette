"""

Cross Scrabble
By Ariel Zepezauer (arielzepezauer@gmail.com)
Created: 12/6/24
Repository at:
Description:
An AI for playing Buckshot Roulette
"""
from random import *

from pycparser.c_ast import While


class BSRPlayer:
    def __init__(self, name=None, human=True):
        self.human = human
        self.name = name
        if not self.human and self.name is None:
            self.name = "Dealer"
        self.inventory = []
        self.max_hp = -1
        self.hp = self.max_hp

    def set_new_max_hp(self, value: int):
        self.max_hp = value
        self.hp = value

    def generate_items(self):
        pass

class BSRoulette:
    def __init__(self, players: list[BSRPlayer]):
        self.players = players
        self.magazine = []
        self.active_player = 0
        self.round = 0
        self.begin_round()

    def begin_round(self):
        new_max_hp = randint(3,5)
        [player.set_new_max_hp(new_max_hp) for player in self.players]
        self.round += 1
        self.begin_magazine()

    def begin_magazine(self):
        # Refresh Players' items
        [player.generate_items() for player in self.players]
        # Reload the Magazine
        shell_count = randint(2,6)
        live_shells = randint(1, shell_count - 1)
        blank_shells = [False for _ in range(shell_count - live_shells)]
        live_shells  = [True  for _ in range(live_shells)]
        self.magazine = blank_shells + live_shells
        # Show it to the players unshuffled
        print(", ".join([f"Live" if shell else f"Blank" for shell in self.magazine]))
        # Then shuffle it
        shuffle(self.magazine)

        # Then, begin the game
        while True:
            player = self.players[self.active_player]
            move = self.get_move(player)

    def get_move(self, player: BSRPlayer):
        if player.human:
            return self.move_ui(player)
        # AI Move Logic Goes Here

    def move_ui(self, player):
        while True:
            move = input(f"Player {self.active_player + 1}{f" ({player.name})" if player.name else ""}, "
                         f"Pick Your Move (type 'help' for movelist):\n")
            move = move.strip().casefold().split(" ")
            if move[0] in self.HELP_ALIASES:
                self.help(move)
            elif move[0] in self.SHOOT_ALIASES:
                self.shoot(player, move)



    SHOOT_ALIASES = ('shoot', 's', 'kill')
    def shoot(self, player, move):
        print(f"{self.SHOOT_ALIASES}:{player=},{move=}")

    HELP_ALIASES = ('help', 'h', '?')
    MOVE_LIST = (move[0] for move in (HELP_ALIASES,
                                      SHOOT_ALIASES,))
    def help(self, move):
        if len(move) == 1:
            print(f"Valid Moves: {", ".join(self.MOVE_LIST)}\n"
                  "type 'help <move>' to show usage, description and aliases")
        elif move[1] in self.HELP_ALIASES:
            print(f"Usage: 'help <optional:move>'\n"
                  f"Aliases: {self.HELP_ALIASES}"
                  f"Shows list of moves if no argument is given, "
                  f"otherwise shows description and arguments for a move.")
        elif move[1] in self.SHOOT_ALIASES:
            print("Usage: 'shoot'\n"
                  f"Aliases: {self.SHOOT_ALIASES}"
                  "Picks up the shotgun, once it has been picked up you must pick a target.\n"
                  "Targets can be 'self' or one of the players shown in 'listplayers'")
