from dataclasses import dataclass

SPADES = '♠'
HEARTS = '♥'
DIAMONDS = '♦'
CLUBS = '♣'

JACK = 11
QUEEN = 12
KING = 13
ACE = 14

FACE_CARDS = {11: 'J', 12: 'Q', 13: 'K', 14: 'A'}


def format_rank(rank):
    return FACE_CARDS.get(rank, str(rank))


SUITS = [SPADES, CLUBS, HEARTS, DIAMONDS]


@dataclass
class Card:
    rank: int
    suit: str

    def __repr__(self):
        return '[' + format_rank(self.rank) + " of " + self.suit + ']'


def new_deck():
    deck = []
    for suit in SUITS:
        for rank in range(2, ACE + 1):
            deck.append(Card(rank, suit))
    return deck
