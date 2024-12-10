"""
Buckshot Roulette
By Ariel Zepezauer (arielzepezauer@gmail.com)
Created: 12/6/24
Repository at:
Description:
An AI for playing Buckshot Roulette
TODO list:
    - Finish Basic Terminal Version
    - Add item support
    - Refactor all print statements to use other methods
      for adaptability in moving beyond a basic terminal implementation
    - Eventually turn this into a discord bot
"""
import random
from random import *
import sys
import time
import os
import copy


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
        # Set Placeholder/Default Values for everything else
        self.inventory = []
        self.max_hp = None
        self.hp = self.max_hp
        self.number = None
        self.wins = 0
        self.aliases = self.generate_aliases()
        self.jammed = False

    def set_new_max_hp(self, value: int):
        self.max_hp = value
        self.hp = value

    def generate_items(self):
        pass

    def generate_aliases(self):
        aliases = [ # TODO: make this cleaner, account for bugs with custom names
            f"{self.name}" if self.name else None,
            f"{self.number}" if self.number else None,
            f"p{self.number}" if self.number else None,
            f"player{self.number}" if self.number else None,
        ]
        self.aliases = [alias.casefold() for alias in aliases if alias]
        return self.aliases

    def __str__(self):
        return (f"Player {self.number}{f" ({self.name})" if self.name else ""} "
                f"[{"".join(["↯" if not self.jammed else " " for _ in range(self.hp)]) +
                    "".join([" " for _ in range(self.max_hp - self.hp)])}]")



class BSRoulette:
    def __init__(self, players: list[BSRPlayer]=(BSRPlayer(),BSRPlayer(human=False))):
        # Setup Players
        self.players = list(players)
        self.living_players = self.players
        # Assign player numbers and aliases
        for i, player in enumerate(self.players):
            player.number = i + 1
        [player.generate_aliases() for player in self.players]
        self.player_dict = {alias: player for player in self.players for alias in player.aliases}
        # Set placeholders
        self.magazine = []
        # Set starting values
        self.active_player = 0
        self.round = 0
        self.sawed_off = False
        self.shotgun_damage = 1
        self.sawed_off_bonus = 1
        self.skip_embellishments = False

    def add_player(self):
        raise NotImplemented

    def begin(self):
        # Reset starting values
        self.active_player = 0
        self.round = 0
        # Play for 3 rounds
        while self.round < 3:
            # First Pick the first player (-1 to account for off by one errors with 0 index)
            self.active_player = self.random_player_least_wins().number - 1
            # Then begin the round
            self.begin_round()

    def random_player_least_wins(self) -> BSRPlayer:
        # (The first player of the next round is the one with the least wins, with ties broken by chance)
        players = copy.deepcopy(self.players)
        shuffle(players)
        return min(players, key=lambda x:x.wins)

    def begin_round(self):
        # Reset player hp
        new_max_hp = randint(3,5)
        [player.set_new_max_hp(new_max_hp) for player in self.players]
        self.living_players = self.players
        # Advance the round counter (this might be better to have one level up)
        self.round += 1
        print(f"------------------------\n"
              f"Begin round {"".join([f"I" for _ in range(self.round)])}\n"
              f"------------------------\n")
        # And begin cycling through magazines
        while self.begin_magazine():
            pass

    def begin_magazine(self) -> bool:
        # Refresh Players' items
        [player.generate_items() for player in self.players]
        # Reload the Magazine
        self.magazine = self.generate_magazine()
        # Show it to the players unshuffled
        print(", ".join([f"Live" if shell else f"Blank" for shell in self.magazine]))
        # Shuffle it
        shuffle(self.magazine)
        print(self.active_player)
        # Then, begin the game
        while self.magazine:
            player = self.living_players[self.active_player]
            if self.get_move(player): # Moves return True if they advance the turn counter
                self.active_player += 1
                # NOTE: This line may create a bug where a player hitting themselves with a blank
                # at the end of the magazine does not correctly carry over to the next one
                self.active_player %= len(self.living_players)
            if len(self.living_players) == 1:
                self.living_players[0].wins += 1
                return False # Return False to end the round
        return True # Return True to start another magazine

    @staticmethod
    def generate_magazine():
        shell_count = randint(2,6)
        live_shells = randint(1, shell_count - 1)
        blank_shells = [False for _ in range(shell_count - live_shells)]
        live_shells  = [True  for _ in range(live_shells)]
        return blank_shells + live_shells

    def get_move(self, player: BSRPlayer):
        if player.human:
            return self.move_ui(player)
        return self.get_ai_move(player.ai_complexity)

    def get_ai_move(self, complexity):
        pass

    def move_ui(self, player):
        """
        UI loop for selecting a move for a human player
        moves return True or False in order to determine when there turn is over
        """
        print(f"Player {self.active_player + 1}{f" ({player.name})" if player.name else ""}, "
              f"Pick Your Move (type 'help' for movelist):")
        while True:
            move = input()
            move = move.strip().casefold().split(" ")
            arguments = move[1::] if len(move) > 1 else None
            move = move[0]
            if move in self.HELP_ALIASES:
                print(self.help(arguments))
            elif move in self.SHOOT_ALIASES:
                return self.shoot(player)
            elif move in self.LISTPLAYERS_ALIASES:
                print(self.list_players())
            else:
                print("Invalid Move (type 'help' for movelist:")

    def update_player_aliases(self):
        for player in self.players:
            player.generate_aliases()
        self.player_dict = {alias: player for player in self.players for alias in player.aliases}

    # --------------------------------------------------------------
    # <editor-fold: commands>
    # ALL NEW COMMANDS MUST HAVE:
    # - AN ALIASES CONSTANT WHICH HAS BEEN ADDED TO THE MOVE LIST ABOVE 'help()'
    # - AN ELIF STATEMENT IN 'move_ui()'
    # <editor-fold: shoot() and shoot() helper functions>
    SHOOT_ALIASES = ('shoot', 's', 'kill')
    SELF_ALIASES = ('me', 'self', 'myself', 's')
    def shoot(self, shooter) -> bool:
        # <editor-fold: Flair>
        time.sleep(0.25) if not self.skip_embellishments else None
        for char in "P I C K. Y O U R. T A R G E T.":
            print(char,end='')
            if char not in (' ', '.'):
                time.sleep(randint(1, 3) * 0.1) if not self.skip_embellishments else None
        print()
        time.sleep(0.6) if not self.skip_embellishments else None
        # </editor-fold>
        # Update player aliases to be safe
        self.update_player_aliases()
        # Enter a UI loop to pick a target
        while True:
            target = input("W H O ?\n").strip().casefold()
            if target in BSRoulette.SELF_ALIASES + tuple(shooter.aliases):
                return self.fire_shotgun(shooter)
            if target not in self.player_dict.keys():
                continue
            target = self.player_dict[target]
            if target in self.living_players:
                return self.fire_shotgun(target)
            else:
                print(f"{target} is already dead.")

    def fire_shotgun(self, target: BSRPlayer) -> bool:
        # <editor-fold: Flair>
        for _ in range(randint(3,5)):
            print(".",end="")
            time.sleep(randint(3,6) * 0.1) if not self.skip_embellishments else None
        print()
        time.sleep(randint(4, 8) * 0.1) if not self.skip_embellishments else None
        # </editor-fold>
        if self.magazine.pop():
            print("BANG.") # TODO: Make this more dramatic
            time.sleep(0.1) if not self.skip_embellishments else None
            self.hit(target)
            # <editor-fold: Flair>
            time.sleep(1) if not self.skip_embellishments else None
            print()
            # Source: https://stackoverflow.com/a/2084628
            # os.system('cls' if os.name == 'nt' else 'clear')
            # </editor-fold>
            return True
        else:
            print("click.")
            time.sleep(1) if not self.skip_embellishments else None
            print()
        return False

    def hit(self, target):
        damage = self.shotgun_damage
        if self.sawed_off:
            self.sawed_off = False
            damage += self.sawed_off_bonus
        target.hp -= damage
        if target.hp <= 0:
            self.kill_player(target)

    def kill_player(self, player):
        # if player in self.living_players[self.active_player: self.active_player + 1]:
        # TODO: Add logic to fix bugs related to the turn order when a player dies
        self.living_players.remove(player)
    # </editor-fold>

    LISTPLAYERS_ALIASES = ('listplayers', 'ls','lp', 'l','players','list')
    def list_players(self) -> str:
        # Update player aliases to be safe
        self.update_player_aliases()
        return "\n".join([f"{player}"
                          f" - Aliases: {", ".join([f"'{alias}'" for alias in player.aliases])}"
                          for player in self.living_players])

    # <editor-fold: help() and help constants>
    HELP_ALIASES = ('help', 'h', '?')
    UNABRIDGED_MOVE_LIST = (HELP_ALIASES, SHOOT_ALIASES, LISTPLAYERS_ALIASES)
    MOVE_LIST = (move[0] for move in UNABRIDGED_MOVE_LIST)
    @staticmethod
    def help(arguments:list[str]|str=None):
        """Help Command: lists information about other commands"""
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
    # </editor-fold: help>
    # </editor-fold: commands>
    # ------------------------------------------------

def main():
    game = BSRoulette([BSRPlayer(),BSRPlayer()])
    game.skip_embellishments = True
    game.begin()

if __name__ == "__main__":
    main()