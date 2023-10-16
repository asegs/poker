import Deal
import Deck
import Scoring

players = int(input("How many players?: "))
deck = Deck.new_deck()

hands = Deal.deal_hands(deck, players)

print("Your hand:")
Deck.print_hand(hands[0])

input("Do the flop...")
community = Deal.deal_flop(deck)
Deck.print_hand(community)
print("You have: " + str(Scoring.score_hand(hands[0] + community)[0][0]))

input("Do the turn...")
community.append(Deal.deal_single(deck))
Deck.print_hand(community)
print("You have: " + str(Scoring.score_hand(hands[0] + community)[0][0]))

input("Do the river...")
community.append(Deal.deal_single(deck))
Deck.print_hand(community)
print("You have: " + str(Scoring.score_hand(hands[0] + community)[0][0]))


input("Do the showdown...")


for i, hand in enumerate(hands[1:]):
    print("Player " + str(i + 1) + ":")
    Deck.print_hand(hand)

print("You: ")
Deck.print_hand(hands[0])

print("Community cards: ")
Deck.print_hand(community)

winners = Scoring.pick_winner([hand + community for hand in hands])
if 0 in winners[0]:
    print("You win!")
else:
    for i, winner in enumerate(winners[0]):
        print("Player " + str(winner) + " wins with " + Scoring.describe_winning_hand(winners[1][i]))