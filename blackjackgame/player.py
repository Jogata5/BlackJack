#!/usr/bin/env python3
# Julian Ogata
# CPSC 386-01
# 2022-3-22
# jogata@csu.fullerton.edu
# @jogata5
#
# Lab 03-00
#
# Header file that holds the players' infomation and player methods
#

"""Player Class File"""

from random import randrange


class Player:
    '''Card File'''

    def __init__(self, name, balance=10000.00):
        self._name = name
        self._bet = [0, 0]
        self._insurance = [0, 0]
        self._balance = int(balance)
        self._hand = [[], []]
        self._bust = [False, False]
        self._user_id = randrange(99999999)

    @property
    def name(self):
        '''Gets player name'''
        return self._name

    @name.setter
    def name(self, name):
        '''Sets player name'''
        self._name = name

    @property
    def user_id(self):
        '''Gets player's user ID'''
        return self._user_id

    @user_id.setter
    def user_id(self, user_id):
        '''Sets player's user ID'''
        self._user_id = user_id

    @property
    def insurance(self):
        '''Gets player insurance'''
        return self._insurance

    @insurance.setter
    def insurance(self, insure):
        '''Sets player insurance'''
        self._insurance = insure

    @property
    def balance(self):
        '''Gets player balance'''
        return self._balance

    @balance.setter
    def balance(self, new_balance):
        '''Sets player balance'''
        self._balance = new_balance

    def add_balance(self, add):
        '''Adds to player balance'''
        self._balance += add

    @property
    def hand(self):
        '''Gets the player's hand'''
        return self._hand

    @hand.setter
    def hand(self, new_hand):
        '''Sets the player's hand'''
        self._hand = new_hand

    @property
    def bust(self):
        '''Gets bust bool check'''
        return self._bust

    @property
    def bet(self):
        '''Gets the player's bet'''
        return self._bet

    @name.setter
    def name(self, name):
        '''Sets player name'''
        self._name = name

    @bust.setter
    def bust(self, bool_bust):
        '''Sets player bool bust'''
        self._bust = bool_bust

    @bet.setter
    def bet(self, new_bet):
        '''Sets player bet'''
        self._bet = new_bet

    def show_hand(self, num=0):
        '''Shows the player's hand in a readable string'''
        return '\n'.join(map(str, self._hand[num]))

    def value_hand(self, num=0):
        '''Returns the mod value of the hand'''
        return self.hand[num][0].value() % self.hand[num][1].value()

    def add_hand(self, cards, num=0):
        '''Adds a card to the player's hand'''
        for card in cards:
            self.hand[num].append(card)

    def add_hand_split(self, card):
        '''Adds a card to the player's split hand'''
        self.hand[1].append(card)

    def double_bet(self, which_hand):
        '''Doubles the player's bet'''
        self.balance -= self._bet[which_hand]
        self._bet[which_hand] *= 2

    def payout(self, which_hand):
        '''Returns the player's payout'''
        payout = self.bet[which_hand] * 2
        return payout

    def minus_balance(self, change):
        '''Subtracts player's balance'''
        self._balance -= change

    def hand_sum(self, num=0):
        '''Calculates the sum of the player's hand'''
        total = sum(map(int, self.hand[num]))
        if (
            sum(map(lambda c: c.rank == 'Ace', self.hand[num]))
            and total + 11 <= 21
        ):
            total += 11
        return total


class Dealer(Player):
    '''Dealer class'''

    def __init__(self):
        super().__init__(self)
        self._name = 'Tom the Dealer'

    @property
    def show_first(self):
        '''Shows the first card in the Dealer's hand'''
        return self.hand[0][0]


def check_shoe(deck):
    '''Checks for cut card in deck'''
    if deck.cut_card:
        print('Cut card reached...')
        return True
    return False


def deal_to(player, deck, num, hand=0):
    '''Deals to a player'''
    for _ in range(num):
        player.add_hand(deck.deal(), hand)
