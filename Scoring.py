import Deal
import Deck
import itertools
from enum import Enum

"""
These all need to return a list of satisfying arrangements.

For example: 
is_pair: returns [2 of clubs, 2 of hearts], [3 of hearts, 3 of diamonds], [2 of clubs, 2 of diamonds]
"""


class Hand(Enum):
    HIGH_CARD = 1,
    PAIR = 2,
    TWO_PAIR = 3,
    THREE_OF_A_KIND = 4,
    STRAIGHT = 5,
    FLUSH = 6,
    FULL_HOUSE = 7,
    FOUR_OF_A_KIND = 8,
    STRAIGHT_FLUSH = 9,
    ROYAL_FLUSH = 10


def get_flushes(hand):
    distributions = {Deck.SPADES: 0, Deck.CLUBS: 0, Deck.HEARTS: 0, Deck.DIAMONDS: 0}
    for card in hand:
        distributions[card.suit] += 1

    flush_suit = None

    for suit in distributions:
        if distributions[suit] >= 5:
            flush_suit = suit

    if flush_suit is None:
        return []

    matching_cards = filter(lambda card: card.suit == flush_suit, hand)
    return list(itertools.combinations(matching_cards, 5))


def timeline_straights(straight):
    last_card = None
    straights = []
    for card in straight:
        if last_card and card.rank == last_card.rank:
            straights_copy = straights.copy()
            for s in straights_copy:
                straight_copy = s.copy()
                straight_copy[-1] = card
                straights.append(straight_copy)
        else:
            last_card = card
            for s in straights:
                s.append(card)
            if len(straights) == 0:
                straights.append([card])
    return straights


def decompose_straight(straight):
    if len(straight) == 5:
        return [straight]
    if len(straight) == 6:
        return [straight[0:-1], straight[1:]]
    return [straight[0:-2], straight[1:-1], straight[2:]]


def get_straights(hand):
    ordered_hand = sorted(hand, key=lambda card: card.rank)
    adjacent_cards = []
    run = []
    for card in ordered_hand:
        if run == [] or card.rank - run[-1].rank <= 1:
            run.append(card)
        elif len(run) > 0:
            adjacent_cards.append(run)
            run = [card]
    if run:
        adjacent_cards.append(run)
    straight_runs = list(filter(lambda r: r[-1].rank - r[0].rank >= 4, adjacent_cards))
    if len(straight_runs) == 0:
        return []
    straight = straight_runs[0]

    five_card_straights = []

    for s in timeline_straights(straight):
        for five_card in decompose_straight(s):
            five_card_straights.append(five_card)

    return five_card_straights


def get_straight_flushes(hand):
    return list(filter(is_flush, get_straights(hand)))


def get_royal_flushes(hand):
    return list(filter(lambda sf: sf[-1].rank == Deck.ACE, get_straight_flushes(hand)))


def is_flush(five_card):
    first_suit = five_card[0].suit
    for i in range(1, 5):
        if five_card[i].suit != first_suit:
            return False
    return True


def get_kinds(hand):
    rank_map = {}
    for card in hand:
        if card.rank in rank_map:
            rank_map[card.rank] += 1
        else:
            rank_map[card.rank] = 1

    results = {"pairs": [], "trips": [], "quads": []}

    for key in rank_map:
        count = rank_map[key]
        matches = list(filter(lambda card: card.rank == key, hand))
        if count == 2:
            results['pairs'].append(matches)
        elif count == 3:
            results['trips'].append(matches)
        elif count == 4:
            results['quads'].append(matches)
    return results


def get_four_of_a_kinds(hand):
    return get_kinds(hand)['quads']


def get_full_houses(hand):
    kinds = get_kinds(hand)
    if len(kinds['pairs']) == 1 and len(kinds['trips']) == 1:
        return [[kinds['pairs'][0], kinds['trips'][0]]]
    elif len(kinds['pairs']) == 2 and len(kinds['trips']) == 1:
        return [
            [kinds['pairs'][0], kinds['trips'][0]],
            [kinds['pairs'][1], kinds['trips'][0]]
        ]


def get_three_of_a_kinds(hand):
    return get_kinds(hand)['trips']


def get_two_pairs(hand):
    pairs = get_kinds(hand)['pairs']
    if len(pairs) == 2:
        return [[pairs[0], pairs[1]]]
    elif len(pairs) == 3:
        return [[pairs[0], pairs[1]], [pairs[1], pairs[2]]]

    return []


def get_pairs(hand):
    return get_kinds(hand)['pairs']


def get_high(hand):
    highest_card = Deck.Card(-1, Deck.SPADES)

    if isinstance(hand[0], list):
        for kind in hand:
            for card in kind:
                if card.rank > highest_card.rank:
                    highest_card = card
    else:
        for card in hand:
            if highest_card.rank < card.rank:
                highest_card = card
    return highest_card


def get_highest_full_house(hands):
    highest_hand = None
    highest_trip_rank = -1
    highest_pair_rank = -1

    for hand in hands:
        pair_rank = hand[0][0].rank
        trip_rank = hand[1][0].rank

        if trip_rank > highest_trip_rank:
            highest_hand = hand
            highest_trip_rank = trip_rank
            highest_pair_rank = pair_rank
            continue
        if trip_rank == highest_trip_rank and pair_rank > highest_pair_rank:
            highest_hand = hand
            highest_pair_rank = pair_rank

    return highest_hand


def get_highest(hands):
    highest_hand = None
    highest_rank = -1

    for hand in hands:
        high_card = get_high(hand)
        if high_card.rank > highest_rank:
            highest_hand = hand
            highest_rank = high_card.rank
    return highest_hand


def remove_from_pool(mutable_hand, cards):
    if isinstance(cards[0], list):
        for kind in cards:
            for card in kind:
                mutable_hand.remove(card)
    else:
        for card in cards:
            mutable_hand.remove(card)


def score_hand(hand):
    hands = []
    mutable_hand = hand.copy()
    cards_used = 0
    royal_flushes = get_royal_flushes(mutable_hand)
    if royal_flushes:
        return [(Hand.ROYAL_FLUSH, get_highest(royal_flushes))]
    straight_flushes = get_straight_flushes(mutable_hand)
    if straight_flushes:
        return [(Hand.STRAIGHT_FLUSH, get_highest(straight_flushes))]
    four_of_a_kinds = get_four_of_a_kinds(mutable_hand)
    if four_of_a_kinds:
        highest_four_of_kind = get_highest(four_of_a_kinds)
        hands.append((Hand.FOUR_OF_A_KIND, get_highest(four_of_a_kinds)))
        remove_from_pool(mutable_hand, highest_four_of_kind)
        cards_used += 4
    full_houses = get_full_houses(mutable_hand)
    if full_houses:
        return [(Hand.FULL_HOUSE, get_highest_full_house(full_houses))]
    flushes = get_flushes(mutable_hand)
    if flushes:
        return [(Hand.FLUSH, get_highest(flushes))]
    straights = get_straights(mutable_hand)
    if straights:
        return [(Hand.STRAIGHT, get_highest(straights))]
    three_of_a_kinds = get_three_of_a_kinds(mutable_hand)
    if three_of_a_kinds and (cards_used + 3 <= 5):
        highest_three_of_kind = get_highest(three_of_a_kinds)
        hands.append((Hand.THREE_OF_A_KIND, highest_three_of_kind))
        remove_from_pool(mutable_hand, highest_three_of_kind)
        cards_used += 3

    two_pairs = get_two_pairs(mutable_hand)
    if two_pairs and (cards_used + 4 <= 5):
        highest_two_pair = get_highest(two_pairs)
        hands.append((Hand.TWO_PAIR, highest_two_pair))
        remove_from_pool(mutable_hand, highest_two_pair)
        cards_used += 4
    pairs = get_pairs(mutable_hand)
    if pairs and (cards_used + 2 <= 5):
        highest_pair = get_highest(pairs)
        hands.append((Hand.PAIR, highest_pair))
        remove_from_pool(mutable_hand, highest_pair)
        cards_used += 2

    while cards_used < 5:
        high = get_high(mutable_hand)
        mutable_hand.remove(high)
        hands.append((Hand.HIGH_CARD, [high]))
        cards_used += 1
    return hands


def hands_all_equal(hands):
    print(hands)
    if not hands:
        return True
    first_hand = hands[0]
    for hand in hands[1:]:
        if first_hand != hand:
            return False
    return True


def get_highest_players(hands):
    highest_hands = []
    highest_rank = -1

    for i, hand in enumerate(hands):
        high = get_high(hand)
        if high.rank > highest_rank:
            highest_hands = [i]
            highest_rank = high.rank
        elif high.rank == highest_rank:
            highest_hands.append(i)
    return highest_hands


def get_highest_players_full_house(hands):
    highest_hand = None
    highest_trip_rank = -1
    highest_pair_rank = -1

    for i, hand in enumerate(hands):
        pair_rank = hand[0][0].rank
        trip_rank = hand[1][0].rank
        if trip_rank > highest_trip_rank:
            highest_hand = i
            highest_trip_rank = trip_rank
            highest_pair_rank = pair_rank
        elif trip_rank == highest_trip_rank and pair_rank > highest_pair_rank:
            highest_hand = i
            highest_pair_rank = pair_rank

    return highest_hand


def pick_winner(player_hands):
    winners = []
    excluded = []
    scores = list(map(score_hand, player_hands))
    highest_position = Hand.HIGH_CARD
    tiebreaks_round = 0

    # Manually broken in case of true tie
    while len(winners) != 1:
        for i, score in enumerate(scores):
            # Don't care about players who didn't match the initial high hand
            if i in excluded:
                continue

            if tiebreaks_round >= len(score):
                return winners

            # Find players in this round on the same level
            player_hand_score = score[tiebreaks_round][0]
            if player_hand_score.value > highest_position.value:
                winners = [i]
                highest_position = player_hand_score
            elif player_hand_score.value == highest_position.value:
                winners.append(i)

        # There was a tie here
        if len(winners) > 1:
            winners_sections = list(map(lambda x: scores[x][tiebreaks_round][1], winners))
            if highest_position == Hand.FULL_HOUSE:
                winner = get_highest_players_full_house(winners_sections)
                return [winners[winner]]
            else:
                winners = list(map(lambda x: winners[x], get_highest_players(winners_sections)))

            # Anyone below that level will not be relevant in the next tiebreak rounds
            for x in range(len(scores)):
                if x not in winners:
                    excluded.append(x)
            tiebreaks_round += 1

    return winners


for i in range(1000):
    deck = Deck.new_deck()
    [p1, p2, p3] = Deal.deal_holdem(deck, 3)
    print(p1)
    print(p2)
    print(p3)

    print(score_hand(p1))
    print(score_hand(p2))
    print(score_hand(p3))

    print(pick_winner([p1, p2, p3]))
