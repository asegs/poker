from dataclasses import dataclass
import colorama

SPADES = '♠'
HEARTS = '♥'
DIAMONDS = '♦'
CLUBS = '♣'

JACK = 11
QUEEN = 12
KING = 13
ACE = 14

FACE_CARDS = {10: 'T', 11: 'J', 12: 'Q', 13: 'K', 14: 'A'}


def format_rank(rank):
    return FACE_CARDS.get(rank, str(rank))


SUITS = [SPADES, CLUBS, HEARTS, DIAMONDS]

good_red = '\033[38;2;160;0;0m'


def color_rank(rank, suit):
    fmt_rank = format_rank(rank)
    if suit == SPADES or suit == CLUBS:
        return colorama.Fore.BLACK + fmt_rank + colorama.Fore.RESET
    return good_red + fmt_rank + colorama.Fore.RESET


def color_suit(suit):
    if suit == SPADES or suit == CLUBS:
        return colorama.Fore.BLACK + suit + colorama.Fore.RESET
    return good_red + suit + colorama.Fore.RESET


def rows_of_card(card):
    return [
        ' ' + colorama.Back.WHITE + ' ' + color_suit(card.suit) + '   ' + colorama.Back.RESET,
        ' ' + colorama.Back.WHITE + '  ' + color_rank(card.rank, card.suit) + '  ' + colorama.Back.RESET,
        ' ' + colorama.Back.WHITE + '   ' + color_suit(card.suit) + ' ' + colorama.Back.RESET
    ]


def print_hand(cards):
    card_rows = [rows_of_card(card) for card in cards]
    for row in range(3):
        for card_row_set in card_rows:
            print(card_row_set[row], end='  ')
        print()


@dataclass
class Card:
    rank: int
    suit: str

    def __repr__(self):
        return format_rank(self.rank) + ' of ' + self.suit


def new_deck():
    deck = []
    for suit in SUITS:
        for rank in range(2, ACE + 1):
            deck.append(Card(rank, suit))
    return deck
