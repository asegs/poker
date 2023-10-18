import Deal
import Deck
import Scoring
import random
import Betting


def print_odds(hand, community, names):
    odds = Betting.player_win_chance(hand, community, names[:players]) * 100
    print("Odds of winning: " + format(odds, ".2f") + "%")



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

greeting = "It's just you"
for i in range(1, players):
    greeting += ', ' + ('and ' if i == players - 1 else '') + names[i]
greeting += '.'

print(greeting)

print("Your hand:")
Deck.print_hand(hands[0])
print("You have: " + str(Scoring.score_hand(hands[0], 2)[0][0]))
print_odds(hands[0], [], names[:players])

input("Do the flop...")
community = Deal.deal_flop(deck)
Deck.print_hand(community)
print("You have: " + str(Scoring.score_hand(hands[0] + community)[0][0]))
print_odds(hands[0], community, names[:players])

input("Do the turn...")
community.append(Deal.deal_single(deck))
Deck.print_hand(community)
print("You have: " + str(Scoring.score_hand(hands[0] + community)[0][0]))
print_odds(hands[0], community, names[:players])


input("Do the river...")
community.append(Deal.deal_single(deck))
Deck.print_hand(community)
print("You have: " + str(Scoring.score_hand(hands[0] + community)[0][0]))
print_odds(hands[0], community, names[:players])



input("Do the showdown...")


for i, hand in enumerate(hands[1:]):
    print(names[i + 1] + ":")
    Deck.print_hand(hand)

print("You: ")
Deck.print_hand(hands[0])

print("Community cards: ")
Deck.print_hand(community)

winners = Scoring.pick_winner([hand + community for hand in hands])

for i, winner in enumerate(winners[0]):
    print(names[winner] + " wins with " + Scoring.describe_winning_hand(winners[1][i]))
