from dataclasses import dataclass
import pied_poker as pp

import Deck

ENGLISH_SUITS = {
    Deck.SPADES: 's',
    Deck.CLUBS: 'c',
    Deck.HEARTS: 'h',
    Deck.DIAMONDS: 'd'
}


def card_to_pp_card(card):
    rank_str = str(card.rank) if card.rank <= 10 else Deck.format_rank(card.rank).lower()
    return pp.Card(rank_str, ENGLISH_SUITS[card.suit])


def hand_to_pp_card(hand):
    return [card_to_pp_card(card) for card in hand]


def player_win_chance(hands, community, names, player_idx):
    players = [pp.Player(names[i], (hand_to_pp_card(hands[player_idx]) if i == player_idx else [])) for i in
               range(len(names) - 1)]
    player = players[player_idx]

    community_cards = hand_to_pp_card(community)
    simulator = pp.PokerRoundSimulator(community_cards=community_cards,
                                       players=players,
                                       total_players=len(players))
    num_simulations = 10000

    simulation_result = simulator.simulate(n=num_simulations, n_jobs=8, status_bar=False)

    probability = simulation_result.probability_of(pp.PlayerWins(player))
    return probability.probability
