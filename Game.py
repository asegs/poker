from Deck import new_deck
import Deal
deck = new_deck()

p1 = Deal.deal_hand(deck)
p2 = Deal.deal_hand(deck)

player = Deal.deal_hand(deck)

print(p1)
print(p2)
print(player)