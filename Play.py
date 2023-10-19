import Deal
import Deck
import Scoring
import random
import Betting


def print_odds(hands, community, names, idx):
    odds = Betting.player_win_chance(hands[idx], community, names[:players]) * 100
    print("Odds of winning: " + format(odds, ".2f") + "%")


def print_remaining(round):
    for player in round.players:
        if not player.folded:
            print(player.name + " in with " + str(player.money))


def play_turn(round):
    Deck.print_hand(betting_round.community)
    print("You have: " + str(Scoring.score_hand(hands[0] + betting_round.community)[0][0]))
    print_odds(hands, betting_round.community, names[:players], 0)
    play_round(betting_round, names[:players])
    print_remaining(round)


def play_round(round, names):
    for i, player in enumerate(round.players):
        if not player.folded:
            player.make_decision(round, i, names)

    # Matching possible raises
    for i, player in enumerate(round.players):
        if not player.folded:
            player.make_decision(round, i, names)

    round.reset_between_bets()


names = [
    "Earl",
    "Stanley",
    "Wilbur",
    "Lars",
    "Tommy",
    "Al",
    "Ivan",
    "Erlang",
    "The Kid",
    "Jarvis",
    "Fats",
    "Billy",
    "Randall",
    "Bad Randall",
    "Slick",
    "Frank",
    "Slim"
]

random.shuffle(names)
names = ["The Player"] + names

players = int(input("How many players?: "))
deck = Deck.new_deck()

hands = Deal.deal_hands(deck, players)

betting_players = [Betting.PlayerState(hands[i], 5000, i == 0, names[i]) for i in range(players)]
betting_round = Betting.Round(betting_players)

greeting = "It's just you"
for i in range(1, players):
    greeting += ', ' + ('and ' if i == players - 1 else '') + names[i]
greeting += '.'

print(greeting)

print("Your hand:")
Deck.print_hand(hands[0])
print("You have: " + str(Scoring.score_hand(hands[0], 2)[0][0]))
print_odds(hands, betting_round.community, names[:players], 0)
play_round(betting_round, names[:players])
print_remaining(betting_round)

input("Do the flop...")
betting_round.community = Deal.deal_flop(deck)
play_turn(betting_round)

input("Do the turn...")
betting_round.community.append(Deal.deal_single(deck))
play_turn(betting_round)

input("Do the river...")
betting_round.community.append(Deal.deal_single(deck))
play_turn(betting_round)

input("Do the showdown...")

for i, hand in enumerate(hands[1:]):
    print(names[i + 1] + ":")
    Deck.print_hand(hand)

print("You: ")
Deck.print_hand(hands[0])

print("Community cards: ")
Deck.print_hand(betting_round.community)

winners = Scoring.pick_winner([hand + betting_round.community for hand in hands])

for i, winner in enumerate(winners[0]):
    print(names[winner] + " wins with " + Scoring.describe_winning_hand(winners[1][i]))
