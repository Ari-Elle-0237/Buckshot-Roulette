"""

Cross Scrabble
By Ariel Zepezauer (arielzepezauer@gmail.com)
Created: 12/6/24
Repository at:
Description:
An AI for playing Buckshot Roulette
TODO list:
    - Eventually turn this into a discord bot
    - Finish Basic Terminal Version
    - Add item support
"""
from random import *

class BSRPlayer:
    """
    Class for storing data about Buckshot Roulette Players.
    Should not contain any logic.
    (Consider nesting in BSRoulette class)
    """
    def __init__(self, name:str=None, human:bool=True, ai_complexity=None):
        # Set Human/AI variables
        self.human = human
        self.name = name
        if not self.human and self.name is None:
            self.name = "Dealer"
        if not self.human:
            self.ai_complexity = ai_complexity
        self.ai_complexity = None
        # Set Placeholder Values for everything else
        self.inventory = []
        self.max_hp = None
        self.hp = self.max_hp
        self.number = None

    def set_new_max_hp(self, value: int):
        self.max_hp = value
        self.hp = value

    def generate_items(self):
        pass

class BSRoulette:
    def __init__(self, players: list[BSRPlayer]=(BSRPlayer(),BSRPlayer(human=False))):
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

    @staticmethod
    def generate_magazine():
        shell_count = randint(2,6)
        live_shells = randint(1, shell_count - 1)
        blank_shells = [False for _ in range(shell_count - live_shells)]
        live_shells  = [True  for _ in range(live_shells)]
        return blank_shells + live_shells

    def begin_magazine(self):
        # Refresh Players' items
        [player.generate_items() for player in self.players]
        # Reload the Magazine
        self.magazine = self.generate_magazine()
        # Show it to the players unshuffled
        print(", ".join([f"Live" if shell else f"Blank" for shell in self.magazine]))
        # Then shuffle it
        shuffle(self.magazine)

        # Then, begin the game
        while True:
            player = self.players[self.active_player]
            self.get_move(player)

    def get_move(self, player: BSRPlayer):
        if player.human:
            return self.move_ui(player)
        return self.get_ai_move(player.ai_complexity)

    def get_ai_move(self, complexity):
        pass

    def move_ui(self, player):
        while True:
            move = input(f"Player {self.active_player + 1}{f" ({player.name})" if player.name else ""}, "
                         f"Pick Your Move (type 'help' for movelist):\n")
            move = move.strip().casefold().split(" ")
            arguments = move[1::] if len(move) > 1 else None
            move = move[0]
            if move in self.HELP_ALIASES:
                print(self.help(arguments))
            elif move in self.SHOOT_ALIASES:
                self.shoot(player)



    SHOOT_ALIASES = ('shoot', 's', 'kill')
    def shoot(self, player):
        print(f"{self}")

    HELP_ALIASES = ('help', 'h', '?')
    MOVE_LIST = (move[0] for move in (HELP_ALIASES,
                                      SHOOT_ALIASES,))
    @staticmethod
    def help(arguments:list[str]|str=None):
        if type(arguments) == str:
            arguments = [arguments]
        if arguments is None:
            return (f"Valid Moves: {", ".join(BSRoulette.MOVE_LIST)}\n"
                    "type 'help <move>' to show usage, description and aliases")
        elif len(arguments) > 1:
            return f"Too many arguments, expected 1, got {len(arguments)}"
        elif arguments[0] in BSRoulette.HELP_ALIASES:
            return (f"Usage: 'help <optional:move>'\n"
                    f"Aliases: {BSRoulette.HELP_ALIASES}"
                    f"Shows list of moves if no argument is given, "
                    f"otherwise shows description and arguments for a move.")
        elif arguments[0] in BSRoulette.SHOOT_ALIASES:
            return ("Usage: 'shoot'\n"
                    f"Aliases: {BSRoulette.SHOOT_ALIASES}"
                    "Picks up the shotgun, once it has been picked up you must pick a target.\n"
                    "Targets can be 'self' or one of the players shown in 'listplayers'")

def main():
    game = BSRoulette()

if __name__ == "__main__":
    main()