import pied_poker as pp
from dataclasses import dataclass

import Deck

WINDOW = 20
BOLDNESS = 2

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


def player_win_chance(hand, community, names):
    players = [pp.Player(names[i], (hand_to_pp_card(hand) if i == 0 else [])) for i in
               range(len(names))]
    player = players[0]

    community_cards = hand_to_pp_card(community)
    simulator = pp.PokerRoundSimulator(community_cards=community_cards,
                                       players=players,
                                       total_players=len(players))
    num_simulations = 500

    simulation_result = simulator.simulate(n=num_simulations, n_jobs=8, status_bar=False)

    probability = simulation_result.probability_of(pp.PlayerWins(player))
    return probability.probability


@dataclass
class PlayerState:
    cards: list
    folded: bool
    raised: bool
    contribution: int
    make_decision: callable
    money: int
    name: str

    def __init__(self, cards, money, human, name):
        self.cards = cards
        self.money = money
        if human:
            self.make_decision = human_bet
        else:
            self.make_decision = cpu_bet
        self.folded = False
        self.raised = False
        self.contribution = 0
        self.name = name


@dataclass
class Round:
    players: list
    community: list

    def __init__(self, players):
        self.players = players
        self.community = []

    def remaining(self):
        count = 0
        for state in self.players:
            if not state.folded:
                count += 1

        return count

    def pot_size(self):
        pot = 0
        for state in self.players:
            pot += state.contribution

        return pot

    def reset_between_bets(self):
        for state in self.players:
            state.raised = False

    def reset_between_hands(self):
        for state in self.players:
            state.folded = False
            state.raised = False
            state.cards = []
            state.contribution = 0


def missing_contribution(round, idx):
    player = round.players[idx]
    player_contribution = player.contribution
    for i in range(idx, idx - len(round.players), -1):
        if not round.players[i].folded and round.players[i].contribution > player_contribution:
            return round.players[i].contribution - player_contribution

    return 0


def cpu_bet(round, idx):
    names = [player.name for player in round.players]
    name = names[idx]
    still_in_names = [names[i] for i in range(len(round.players)) if not round.players[i].folded]
    odds = player_win_chance(round.players[idx].cards, round.community, still_in_names)
    happy_odds = (1 + WINDOW / 100) * odds
    expected_odds = 1 / len(still_in_names)

    missing = missing_contribution(round, idx)

    if missing == 0 and round.players[idx].raised:
        return

    budget = round.players[idx].money
    if missing > budget:
        round.players[idx].folded = True
        print(name + " folded.")
        return

    if missing == 0 and happy_odds < expected_odds:
        print(name + " checked.")
        return

    if missing > 0 and happy_odds < expected_odds:
        round.players[idx].folded = True
        print(name + " folded.")
        return
    if happy_odds >= expected_odds:
        want_to_bet = int((odds - expected_odds) * budget)
        if odds >= expected_odds:
            bet = 0 if round.players[idx].raised else want_to_bet
            bet += missing
            if bet == missing:
                if missing > want_to_bet * BOLDNESS:
                    round.players[idx].folded = True
                    print(name + " folded.")
                    return
                print(name + " called.")
            else:
                print(name + " raised " + str(bet - missing))
                round.players[idx].raised = True

            round.players[idx].contribution += bet
            round.players[idx].money -= bet
            return

        elif missing > 0:
            if missing > want_to_bet * BOLDNESS:
                round.players[idx].folded = True
                print(name + " folded.")
                return
            round.players[idx].contribution += missing
            round.players[idx].money -= missing
            print(name + " called.")
            return
        else:
            print(name + " checked.")


def human_bet(round, idx):
    if round.players[idx].folded:
        return
    missing = missing_contribution(round, idx)
    can_raise = not round.players[idx].raised

    if missing == 0 and not can_raise:
        return

    pot = round.pot_size()
    print("Pot: $" + str(pot))
    print("You have $" + str(round.players[idx].money) + " left")
    print("$" + str(missing) + " to play...")
    if missing == 0:
        choice = input("(C)heck or (r)aise? ")
    else:
        prompt = "(C)all, (f)old, or (r)aise? " if can_raise else "(C)all or (f)old? "
        choice = input(prompt)

    if choice.lower() == 'c':
        round.players[idx].contribution += missing
        round.players[idx].money -= missing

        print("You " + ("check" if missing == 0 else "call"))
        return
    elif choice.lower() == 'f':
        print("You fold.")
        round.players[idx].folded = True
        return

    raise_amount = int(input("How much? "))
    total_amount = missing + raise_amount

    round.players[idx].contribution += total_amount
    round.players[idx].money -= total_amount
    round.players[idx].raised = True
