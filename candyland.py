from collections import Counter
from random import shuffle, choice

from candyland_resources import board, deck, characters, colors

class CandyLand():
    """class for modeling how candyland is played"""
    def __init__(self, board: list, deck: Counter, characters: list):
        """Initialize Candyland with a board and shuffled deck"""
        self.board = board
        self.deck = deck
        self.shuffled_deck = self.make_shuffled_deck()
        self.characters = characters
        self.character_mappings = self._make_character_mappings()

    def traverse(self, card, start=0):
        """Move from start to another space on a board based on card.
        Returns the new square's index.
        Cards:
            Single color: Move forward to the next sqaure of that color.
            Double color: move forward to the next square of that color twice.
            Character:
                Move forwards or backwards to that character's square.
            Bridges:
                If a move ends on the start of the bridge, move to the end of it.
            Miss:
                If a move starts on a miss tile, move forward to the next skip tile.
            End:
                Counts as any color.
        """

        start_space: dict = self.board[start]

        #handle miss a turn spaces
        if start_space.get("special") == "miss":
            return start + 1

        #handle character spaces
        if card in characters:
            for character in self.mappings

        #handle normal spaces

    def make_shuffled_deck(self):
        """Returns a shuffled deck derived from instance's deck"""
        shuffled = sorted(self.deck.elements())
        shuffle(shuffled)
        return shuffled

    def _make_character_mappings(self):
        """Return dict of char and space number mappings"""
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

        for space, idx in self.board:
            if space.get("char") == character:
                return idx
        return None


candyland = CandyLand(board, deck, characters)
print(candyland.character_mappings)