#!/usr/bin/env python3
# Julian Ogata
# CPSC 386-01
# 2022-3-22
# jogata@csu.fullerton.edu
# @jogata5
#
# Lab 03-00
#
# Holds Card Class for Deck creation
#

'''Card File'''

from collections import namedtuple
from random import shuffle, randrange
from math import ceil

# Makes a class named 'Card' with values of ['rank' and 'suit']
Card = namedtuple('Card', ['rank', 'suit'])


def stringify_card(card):
    '''Transforms card into a readable string'''
    return '{} of {}'.format(card.rank, card.suit)


# Makes the card a string
Card.__str__ = stringify_card


class Deck:
    '''Class that holds Deck infomation and Variables'''

    ranks = ['Ace'] + [str(x) for x in range(2, 11)] + 'Jack Queen King'.split()
    suits = 'Clubs Hearts Spades Diamonds'.split()
    values = list(range(1, 11)) + [10, 10, 10]
    values_dict = dict(zip(ranks, values))

    def __init__(self, cut_card_position_min, cut_card_position_max):
        self.card = Card('King', 'Hearts')
        self._cards = [
            Card(rank, suit) for suit in self.suits for rank in self.ranks
        ]
        self._cut_cards_position = randrange(
            cut_card_position_min, cut_card_position_max
        )
        self._cut_card_reached = False

    @property
    def cards(self):
        '''Gets Cards'''
        return self._cards

    @cards.setter
    def cards(self, cards):
        '''Sets Cards'''
        self._cards = cards

    @property
    def cut_card(self):
        '''Gets cut card'''
        return self._cut_card_reached

    @cut_card.setter
    def cut_card(self, bool_cut):
        '''Sets cut card'''
        self._cut_card_reached = bool_cut

    def get_card(self):
        '''Gets Card in string form'''
        return '\n'.join(map(str, self.cards))

    def __getitem__(self, position):
        '''Gets Card from position'''
        return self.cards[position]

    def __len__(self):
        '''Gets the length of the card deck'''
        return len(self.cards)

    def __int__(self):
        '''Returns the card's value'''
        return card_value

    def __str__(self):
        '''Transforms card into a readable string'''
        return '\n'.join(map(str, self.cards))

    def shuffle(self, num=1):
        '''Shuffles deck'''
        for _ in range(num):
            shuffle(self.cards)

    def cut(self):
        '''Puts the cut card in the deck'''
        extra = ceil(len(self.cards) * 0.2)
        half = (len(self.cards) // 2) + randrange(-extra, extra)
        tophalf = self.cards[:half]
        bottomhalf = self.cards[half:]
        bottomhalf.insert(self._cut_cards_position, 'cut')
        self.cards = bottomhalf + tophalf

    def deal(self, num=1):
        '''Deals cards from the deck'''
        cards = []
        for _ in range(num):
            if self.cards[0] == 'cut':
                self.cut_card = True
                self.cards.pop(0)
            cards.append(self.cards.pop(0))
        return cards

    def merge(self, other_deck):
        '''Merges decks into one'''
        self.cards = self.cards + other_deck.deal(len(other_deck))


def card_value(card):
    '''Gets the card value from a dictionary'''
    return Deck.values_dict[card.rank]


Card.value = card_value
Card.__int__ = card_value
