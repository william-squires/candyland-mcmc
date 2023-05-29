from collections import Counter
from random import shuffle, choice
import matplotlib.pyplot as plt
import pandas
import seaborn as sns

from candyland_resources import board, deck, characters, colors, bridges

class CandyLand():
    """class for modeling how candyland is played"""
    def __init__(
            self,
            board: list,
            deck: Counter,
            characters: list,
            bridges: list
        ):
        """Initialize Candyland with a board and shuffled deck

        board: a list of objects that each represent types of spaces.
            Color spaces look like {"color": "<color>"}
            Character spaces look like {"char": "<char_name>"}
            Special spaces contain the key "special"
                {"special": "start"}:
                    Marks starting space of board.
                {"special": "end"}:
                    Marks ending space of board. counts as every color.
                {"color": "<color>", "special": "miss"}:
                    Indicates player landing here misses their next turn.
                {"special": "skip"}:
                    Players that miss their turn move here
                        to track skipping a turn.
            There are also bridges:
                {"color": "<color>", "bridge": "<bridge_name>"}:
                    Indicates that a bridge starts here. Players that land on a
                        bridge start move to the other end immediately.
                {"color": "<color>", "end": "<bridge_name>"}:
                    Indicates the end of a bridge.

        deck: A Counter that tracks how many of each card are in a deck. See
            traverse for more info on specific cards.

        shuffled_deck: A list form of deck that has been shuffled.

        characters: A list of names that appear on character cards and spaces.

        character_mappings: A dictionary mapping each character to its space.

        bridges: A list of bridge names:

        bridge_mappings:  A dictionary mapping each bridge to its end space.

        pos: Player's current position
        """
        self.board = board

        self.deck = deck
        self.shuffled_deck = self.make_shuffled_deck()

        self.characters = characters
        self.character_mappings = self._make_character_mappings()

        self.bridges = bridges
        self.bridge_mappings = self._make_bridge_mappings()

        self.pos = 0

    def traverse(self, card, start=0):
        """Move from start to another space on a board based on card.
        Returns the new square's index.
        Cards:
            Single color: Move forward to the next sqaure of that color.
            Double color: move forward to the next square of that color twice.
            Character:
                Move forwards or backwards to that character's square.
            Bridges:
                If a move ends on the start of the bridge,
                    move to the end of it.
            Miss:
                If a move starts on a miss tile,
                    move forward to the next skip tile.
            End:
                Counts as any color.
        """

        start_space: dict = self.board[start]

        #handle miss a turn spaces
        if start_space.get("special") == "miss":
            return start + 1

        #handle character spaces
        if card in self.characters:
            return self.character_mappings[card]

        #handle normal spaces
        for idx, space in enumerate(self.board):
            if idx > start:
                if space.get("color") == card[0]:
                    if len(card) == 1:
                        if space.get("bridge"):
                            return self.bridge_mappings[space.get("bridge")]
                        else:
                            return idx
                    else:
                        return self.traverse(card[0], idx)

        #return end of board if we get through all normal spaces
        return len(self.board) - 1

    def play(self):
        """Play a game of candyland. Return number of turns taken to win"""
        self.pos = 0
        turns = 0

        while self.pos < len(self.board) - 1:
            if len(self.shuffled_deck) == 0:
                self.shuffled_deck = self.make_shuffled_deck()

            card = self.shuffled_deck.pop()
            self.pos = self.traverse(card, self.pos)

            turns += 1

        return turns

    def make_shuffled_deck(self):
        """Returns a shuffled deck derived from instance's deck"""
        shuffled = sorted(self.deck.elements())
        shuffle(shuffled)
        return shuffled

    def _make_character_mappings(self):
        """Return dict of char and space mappings"""
        spaces = [
            self._get_character_pos(character)
            for character
            in self.characters
        ]

        return dict(zip(self.characters, spaces))

    def _get_character_pos(self, character: str):
        """Returns the space number of a character's space.
        If not found, return None.
        """

        for idx, space in enumerate(self.board):
            if space.get("char") == character:
                return idx
        return None

    def _make_bridge_mappings(self):
        """Return dict of bridge name and end space mappings"""
        spaces = [
            self._get_bridge_end_pos(bridge)
            for bridge
            in self.bridges
        ]

        return dict(zip(self.bridges, spaces))

    def _get_bridge_end_pos(self, bridge):
        """Returns the space number of a bridge's end space.
        If not found, return None.
        """

        for idx, space in enumerate(self.board):
            if space.get("end") == bridge:
                return idx
        return None

candyland = CandyLand(board, deck, characters, bridges)
games_to_play = 100000
turns = []
for i in range(games_to_play):
    turns.append(candyland.play())

turn_counts_df = pandas.DataFrame(
    turns,
    columns=["Turns"]
)

freqs = sns.displot(turn_counts_df, x="Turns", kind="kde")
plt.show()