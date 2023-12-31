import random


def deal_cards(deck, count):
    returned = []
    for i in range(count):
        card = random.choice(deck)
        deck.remove(card)
        returned.append(card)
    return returned


def deal_hand(deck):
    return deal_cards(deck, 2)


def deal_flop(deck):
    return deal_cards(deck, 3)


def deal_single(deck):
    return deal_cards(deck, 1)[0]

def deal_full(deck):
    return deal_cards(deck, 7)


def deal_hands(deck, players):
    return [deal_hand(deck) for i in range(players)]


def deal_holdem(deck, players):
    holes = deal_hands(deck, players)
    community = deal_cards(deck, 5)

    return list(map(lambda hole: hole + community, holes))
