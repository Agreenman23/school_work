#Alex Greenman
#873392313
#This program contains two classes: "Card" and "Deck". A "Card" object represents a
#single card and has two attributes, suit and rank. A "Deck"  object represents an
#entire deck of cards and features methods that perform actions on the Deck. The
#'deal' function simulates the setup of a card game using methods from the Deck class.

import random

class Card:

     '''This class contains information about a particular card.

     Attributes:
         suit: str
         rank: str

     '''

     def __init__(self, rank, suit):
         self.rank = rank
         self.suit = suit

     def __str__(self):
         #to return a printable representation of a Card object
         return f'{self.rank} of {self.suit}'

     def __repr__(self):
         #returns valid expression that could help recreate Card object with same value
         return f'Card({self.rank!r},{self.suit!r})'

class Deck:

     '''This class represents an entire deck of cards. This class also contains
     methods which can be used to manipulate the Deck.

     Attributes:
         cards: list of strs

     '''

     def __init__(self, cards):
         ## check whether items are coming from a Card or list
         if type(cards) == Card:
             cards == cards.contents
         #copy those items, to avoid an aliasing problem
         self.contents = list(cards)

     def __str__(self):
         #to return a printable representation of a Deck object
         if len(self.contents) == 0:
             return 'empty deck'
         else:
             return f'Deck of {len(self.contents)} cards'

     def __repr__(self):
         #returns valid expression that could help recreate Deck object with same value
         return f'Deck({self.contents!r})'

     def shuffle(self):
         '''This method shuffles the Cards in the deck'''
         random.shuffle(self.contents)


     def draw(self, i=-1):
         '''This method removes a single Card from the Deck & returns it to the user'''
         if len(self.contents) == 0:
             raise ValueError("there are not enough cards in the deck")
         return self.contents.pop(i)


     def size(self):
          '''This method returns the number of cards left in the deck'''
          return len(self.contents)

def deal(deck, players, hand_size):
    """This function simulates the setup of a card game; it shuffles the
    given deck and then distributes a certain number of cards to a
    certain number of players"""
    #make deck iterable
    deck = [deck]
    #create the required # of hands based on what is passed into players parameter
    hands = [[] for _ in range(0, players)]
    i = -1
    #the for loop below shuffles cards in deck
    for cards in deck:
        cards.shuffle()
        #the for loop below ensure each player is dealt proper number of cards
        for _ in range(hand_size):
            #the for loop below draws cards and appends them to players' hands
            for h in hands:
                i += 1
                draw_card = cards.draw()
                draw_card_to_string = str(draw_card)
                h.append(draw_card_to_string)
    #while loop prints each players' hand until each player has received the
    #appropriate number of cards
    j = 0
    #added hands_idx counter so that it would move the index of the hands list
    #each iteration of the while loop
    hands_idx = 0
    player_number = 0
    while j < len(hands) and player_number <= players:
        player_number += 1
        print(f'Player {player_number} got: {", ".join(hands[hands_idx])}')
        j+=1
        hands_idx+=1
