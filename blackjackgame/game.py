#!/usr/bin/env python3
# Julian Ogata
# CPSC 386-01
# 2022-3-22
# jogata@csu.fullerton.edu
# @jogata5
#
# Lab 03-00
#
# Game file that holds core elements: game rules, turns, scores, etc.
#

"""Game Class file"""

from random import randrange
from time import sleep
from .cards import Deck
from .player import Player as p, Dealer as deal, deal_to, check_shoe
from .save_data_file import to_file, from_file


def reset_variables(players, file_name):
    '''Resets player values for continuation/end of game'''
    for player in players:
        player.bet = [0, 0]
        player.insurance = [0, 0]
        player.hand = [[], []]
        player.bust = [False, False]
    to_file(file_name, players[:-1])


def check_name(player_names, counter):
    """Function: Checks player names for duplicates"""
    while True:
        name = input("What is Player {}'s name?\n".format(str(counter + 1)))
        if name == "":
            name = "Player {}".format(str(counter + 1))
        elif name not in player_names:
            player_names.append(name)
            return player_names
        else:
            print(
                'Duplicate name detected...\n'
                + 'Please input a different name.'
            )


def check_ace(player):
    '''Checks if player has an Ace'''
    counter = 0
    for card in player.hand[0]:
        if card.rank == 'Ace':
            counter += 1
    if counter == 1:
        return False
    return True


def check_split(player):
    '''Checks if player can split'''
    if (
        player.hand[0][0].value() == player.hand[0][1].value()
        and player.balance - player.bet[0] >= player.bet[0]
        and check_ace(player) is True
    ):
        return True
    return False


def split_player(player, deck):
    '''Splits player hand'''
    player.add_hand_split(player.hand[0][1])
    player.hand[0].pop()
    deal_to(player, deck, 1, 0)
    deal_to(player, deck, 1, 1)
    sleep(1)
    player.balance -= player.bet[0]
    player.bet[1] = player.bet[0]


def check_sum(player, which_hand):
    '''Checks the sum of the player's hand'''
    sum_result = player.hand_sum(which_hand)
    if sum_result >= 21:
        if sum_result == 21:
            print('BLACKJACK!')
        else:
            print('BUST!\nYou lost ${}\n'.format(player.bet[which_hand]))
            player.bust[which_hand] = True
        return False
    return True


def prompt_names(players, counter, file_name):
    '''Prompts the user for a name and creates a user id'''
    name_loop = True
    player_names = []
    while name_loop:
        player_names = check_name(player_names, counter)
        players.append(p(player_names[-1]))
        if players[-1].user_id in from_file(file_name):
            random_id = randrange(99999999)
            while random_id not in from_file(file_name):
                players[-1].user_id = randrange(99999999)
        to_file(file_name, players)
        name_loop = False
        print('You will start will a balance of $10,000.\n')
        print('Your User Id is: {}\n'.format(players[-1].user_id))
        input('Please remember your ID.\nPress any key to continue...')
    return players


def add_funds(player):
    '''Asks player if they would like to add funds to their balance'''
    choice_loop = True
    while choice_loop:
        prompt = input('Would you like to add funds? (y/n): ')
        if prompt.lower() == 'y':
            choice_loop = False
            fund_loop = True
            while fund_loop:
                try:
                    amount = int(input('How much: $: '))
                    if amount > 0:
                        player.balance += amount
                        print('You have added: ${}'.format(amount))
                        print('Your balance is: ${}'.format(player.balance))
                        fund_loop = False
                    else:
                        print('Please enter a positive integer.')
                except ValueError:
                    print('Please enter a positive integer.')
        else:
            choice_loop = False


def check_winnings(players, dealer):
    '''Checks if a player has won or not'''
    for player in players:
        if isinstance(player, deal):
            break
        for which_hand, hand in enumerate(player.hand):
            if player.bust[which_hand] is False and hand:
                print('\n--------------------------')
                if (
                    player.hand_sum(which_hand) > dealer.hand_sum()
                    and dealer.hand_sum(which_hand) <= 21
                ) or (dealer.hand_sum() > 21):
                    payout = player.payout(which_hand)
                    player.add_balance(payout)
                    print(
                        '{} won with a bet of ${}!\n'.format(
                            player.name, player.bet[which_hand]
                        )
                    )
                    print(
                        '${} has been added to your balance\nBalance: ${}'.format(
                            payout, player.balance
                        )
                    )
                elif player.hand_sum(which_hand) == dealer.hand_sum():
                    if (
                        player.hand_sum(which_hand) == 21
                        and dealer.hand_sum() == 21
                        and len(player.hand) == 2
                        and len(dealer.hand) > 2
                    ):
                        payout = player.payout(which_hand)
                        print(
                            '{} won with a bet of ${}!\n'.format(
                                player.name, player.bet[which_hand]
                            )
                        )
                        print(
                            '${} has been added to your balance'.format(payout)
                        )
                        player.add_balance(payout)
                        print('Balance: ${}'.format(player.balance))
                    else:
                        player.add_balance(
                            player.bet[which_hand]
                            + player.insurance[which_hand]
                        )
                        print(
                            'Push...\n{} will receive their bet of ${} back.'.format(
                                player.name, player.bet[which_hand]
                            )
                        )
                        print('\nBalance: ${}'.format(player.balance))
                        player.bet[which_hand] = 0
                else:
                    print(
                        '{} lost with a bet of ${}\nBalance: ${}'.format(
                            player.name, player.bet[which_hand], player.balance
                        )
                    )
            elif not hand:
                break
        sleep(0.5)


def player_turn(player, idx):
    '''Prompts players for wagers'''
    print('** Player {} **'.format(idx))
    print("\n{}'s wager".format(player.name))
    input_loop = True
    while input_loop:
        try:
            print('Your balance is: ${}'.format(player.balance))
            bet = int(input('How much would you like to bet: $'))
            if bet > player.balance:
                print('You do not have the funds for that bet')
            elif bet < 1:
                print('Please bet a positive number of money')
            else:
                player.bet[0] = bet
                input_loop = False
        except ValueError:
            print('Please input a positive integer')
    print('Previous Balance: ${}'.format(player.balance))
    player.minus_balance(bet)
    print('New Balance: ${}'.format(player.balance))


def insurance_bet(player, dealer, which_hand):
    '''Prompts player for insurance'''
    choice_loop = True
    while choice_loop:
        insure = input(
            'The dealer has a {}, '.format(dealer.show_first)
            + 'would you like to buy insurance? (y/n)'
        )
        if insure.lower() == 'y':
            prompt_loop = True
            while prompt_loop:
                try:
                    print(
                        "{}'s balance: ${}".format(player.name, player.balance)
                    )
                    amount = int(input('How much insurance: $'))
                    if 0 < amount <= player.balance:
                        player.balance -= amount
                        player.insurance[which_hand] = amount
                        print('New Balance: {}'.format(player.balance))
                        prompt_loop = False
                except ValueError:
                    print('Please input an integer')
        elif insure.lower() == 'n':
            prompt_loop = False
        choice_loop = False


def check_insurance(dealer, players):
    '''Checks if players won insurance or not'''
    for player in players:
        for insure in player.insurance:
            if insure != 0 and not isinstance(player, deal):
                if dealer.hand_sum == 21:
                    print(
                        '{} has won their insurance of ${}'.format(
                            player.name, insure
                        )
                    )
                    player.balance += insure
                else:
                    print(
                        '{} has lost their insurance of ${}'.format(
                            player.name, insure
                        )
                    )
                    insure = 0


def check_file(file_name):
    if from_file(file_name):
        return file_name
    else:
        choice = input('Would you like to enter a different file name? (y,n): ')
        if choice.lower() == 'y':
            file = input('Input full file name: ')
            if from_file(file):
                print('Data File Found!')
                return file
        return False


def next_player(players):
    '''Goes to the next player in the list'''
    temp = players[0]
    players.pop(0)
    players.append(temp)
    return players


def end_prompt():
    '''Asks player to play again'''
    print('\n--------------------------')
    prompt = input('Continue playing? (y/n):')
    return prompt.lower()


class BlackJackGame:
    '''Class for Blackjack game'''

    def __init__(self):
        self._deck = Deck(60, 80)
        self._turn = 0
        self._num_players = 0
        self._order = [self._num_players]
        self._game_is_not_over = True
        self._ids_used = []

    @property
    def deck(self):
        '''Gets the game deck'''
        return self._deck

    @deck.setter
    def deck(self, deck):
        '''Sets the game deck'''
        self._deck = deck

    @property
    def ids_used(self):
        '''Gets user ids that have been loaded'''
        return self._ids_used

    def add_ids_used(self, user_id):
        '''Adds user ids to the in-play id list'''
        self._ids_used.append(user_id)

    def set_num_players(self, players):
        '''Sets the number of players'''
        self._num_players = players

    def get_num_players(self):
        '''Gets the number of players'''
        return self._num_players

    def prompt_num_players(self):
        '''Prompts user for number of players'''
        while True:
            try:
                self.set_num_players(int(input("How many players: ")))
                if self.get_num_players() < 1 or self.get_num_players() > 4:
                    print("Please input a number from 1 - 4")
                else:
                    break
            except ValueError:
                print("Please input a number from 1 - 4")

    def get_save_data(self, players, counter, file_name):
        '''Asks the player if they would like to load a save, loads saves'''
        choice_loop = True
        chosen = False
        saved_ids = from_file(file_name)
        while choice_loop:
            try:
                user_id = int(input('Please input your User ID: '))
                if user_id in saved_ids.keys() and user_id not in self.ids_used:
                    print(
                        'Save found!\n\tName: {}\n\tBalance: ${}'.format(
                            saved_ids.get(user_id).name,
                            saved_ids.get(user_id).balance,
                        )
                    )
                    prompt = input('Would you like to load? (y/n): ')
                    if prompt.lower() == 'y':
                        print('Save Loaded\n')
                        self.add_ids_used(user_id)
                        players.append(saved_ids.get(user_id))
                        chosen = True
                        choice_loop = False
                elif user_id in self.ids_used:
                    print('User id in play...')
                else:
                    print('Save not found...')
                if chosen is False:
                    prompt2 = input('Do you still want to load a save? (y/n): ')
                    if prompt2.lower() == 'n':
                        prompt_names(players, counter, file_name)
                        choice_loop = False
                    else:
                        continue
                else:
                    choice_loop = False
            except ValueError:
                print('Please enter a valid id of positive integers')
        return players

    def prompt_data(self, players, file_name):
        '''Prompts users for their name/save file id'''
        counter = 0
        players = []
        while counter < self.get_num_players():
            print('\n--------------------------')
            print('Player {}'.format(counter + 1))
            prompt = input('Would you like to load a save? (y/n): ')
            if prompt.lower() == 'y':
                players = self.get_save_data(players, counter, file_name)
            else:
                players = prompt_names(players, counter, file_name)
            counter += 1
        return players

    def setup(self, file_name):
        '''Sets the game up'''
        players = []
        self.prompt_num_players()
        players = self.prompt_data(players, file_name)
        for player in players:
            print('\n--------------------------')
            print('{}'.format(player.name))
            add_funds(player)
        players.append(deal())
        for _ in range(7):
            self.deck.merge(Deck(20, 30))
        self.deck.shuffle(5)
        self.deck.cut()
        return players

    def dealer_turn(self, dealer, players):
        '''Deals cards to players'''
        print('{} will start dealing cards...'.format(dealer.name))
        print_str = 'Dealing...\n'
        for char in print_str:
            print(char, end='', flush=True)
            sleep(0.2)
        for player in players[1:]:
            if check_shoe(self.deck):
                self.deck = Deck(60, 80)
            deal_to(player, self.deck, 2)
        deal_to(dealer, self.deck, 2)
        sleep(0.2)
        return True

    def dealer_show(self, dealer, players, split_counter):
        '''Has Dealer show/deal their own hand/checks player insurance'''
        print('\n--------------------------')
        print(
            "\n{}'s turn...\n{} hand:\n{}\n".format(
                dealer.name, dealer.name, dealer.show_hand()
            )
        )
        sleep(0.7)

        bust_counter = 0
        for player in players:
            for bust in player.bust:
                if bust is True:
                    bust_counter += 1

        check_insurance(dealer, players)

        if bust_counter < len(players) - 1 + split_counter:
            loop = True
            while loop:
                sum_result = dealer.hand_sum()
                print("{}'s Total: {}\n".format(dealer.name, sum_result))
                if dealer.hand_sum() > 21:
                    print('{} has busted'.format(dealer.name))
                    loop = False
                elif sum_result == 21:
                    print('{} GOT BLACKJACK!'.format(dealer.name))
                    loop = False
                elif sum_result >= 17:
                    print('{} stays'.format(dealer.name))
                    loop = False
                else:
                    deal_to(dealer, self.deck, 1)
                    print('{} Hit!'.format(dealer.name))
                    sleep(0.3)
                    print('Dealt: {}'.format(dealer.hand[0][-1]))
                    print('Total Sum: {}'.format(dealer.hand_sum()))
                sleep(1)

    def inital_choice(self, players, dealer):
        '''Checks for the appropriate prompts for players'''
        split_counter = 0
        for counter, player in enumerate(players):
            if player.hand_sum() < 21:
                if not isinstance(player, deal) and check_split(player):
                    self.split_choice(player, dealer, counter + 1)
                    split_counter += 1
                    sleep(0.7)
                elif isinstance(player, deal):
                    self.dealer_show(dealer, players, split_counter)
                    break
            for idx, hand in enumerate(player.hand):
                if hand:
                    self.reg_choices(player, dealer, counter + 1, idx)

    def reg_choices(self, player, dealer, counter, which_hand):
        '''Prompts players to hit, stay, or double down'''
        choice_loop = True
        print('\n--------------------------')
        print('** Player {} **\n'.format(counter))
        print(
            "{}'s turn...\nYour cards are:\n{}\n".format(
                player.name, player.show_hand(which_hand)
            )
        )
        print('Total Sum: {}\n'.format(player.hand_sum(which_hand)))
        print("{}'s face-up card: \n{}".format(dealer.name, dealer.show_first))
        if (
            dealer.show_first.rank in '10 Ace King Queen Jack'.split()
            and player.balance > 0
        ):
            insurance_bet(player, dealer, counter)
            sleep(0.7)

        while choice_loop:
            choice = input(
                '\nWhat would you like to do?\n'
                + '\tHit\n'
                + '\tDouble Down\n'
                + '\tStay\nInput: '
            )
            try:
                if choice.lower() == 'stay':
                    if check_sum(player, which_hand):
                        choice_loop = False
                elif choice.lower() == 'hit':
                    deal_to(player, self.deck, 1, which_hand)
                    print('Dealt: {}'.format(player.hand[which_hand][-1]))
                    sleep(0.5)
                    if check_sum(player, which_hand):
                        self.remaining_choice(
                            player, dealer, counter, which_hand
                        )
                        choice_loop = False
                    else:
                        choice_loop = False
                elif choice.lower() == 'double down':
                    player.double_bet(which_hand)
                    print(
                        'You have doubled down...\nYour wager is now: ${}'.format(
                            player.bet[which_hand]
                        )
                    )
                    print('Remaining Balance: ${}'.format(player.balance))
                    sleep(0.7)
                    self.remaining_choice(player, dealer, counter, which_hand)
                    choice_loop = False
                sleep(0.3)
            except ValueError:
                print('Please input desired action listed')

    def split_choice(self, player, dealer, counter):
        '''Asks player if they would like to split their hand'''
        print('\n--------------------------')
        print('** Player {} **\n'.format(counter))
        print(
            "{}'s turn...\nYour cards are:\n{}\n".format(
                player.name, player.show_hand()
            )
        )
        print('Total Sum: {}\n'.format(player.hand_sum()))
        print("{}'s face-up card: \n{}".format(dealer.name, dealer.show_first))
        choice_loop = True
        while choice_loop:
            try:
                prompt = input('Would you like to split?(y/n)')
                if prompt.lower() == 'y':
                    split_player(player, self.deck)
                    print(
                        'Your hand has been split with the same bet\n\n'
                        + 'New Hand:\n{}\n\nBet: {}\n'.format(
                            player.show_hand(0), player.bet[0]
                        )
                    )
                    print(
                        'Split Hand:\n{}\nBet: {}\n'.format(
                            player.show_hand(1), player.bet[1]
                        )
                    )
                    print(
                        'You will continue with your current hand '
                        + 'until the next turn'
                    )
                    choice_loop = False
                sleep(0.5)
                choice_loop = False
            except ValueError:
                print('Please input desired action listed')

    def remaining_choice(self, player, dealer, counter, which_hand):
        '''Continues to prompt players to hit or stay'''
        choice_loop = True
        while choice_loop:
            print('\n--------------------------')
            print('** Player {} **\n'.format(counter))
            print(
                "{}'s turn...\nYour cards are:\n{}\n".format(
                    player.name, player.show_hand(which_hand)
                )
            )
            print('Total Sum: {}\n'.format(player.hand_sum(which_hand)))
            print(
                "{}'s face-up card: \n{}".format(dealer.name, dealer.show_first)
            )
            choice = input('\nHit or Stay?\n\tHit\n\tStay\n')
            try:
                if choice.lower() == 'stay':
                    if check_sum(player, which_hand):
                        break
                elif choice.lower() == 'hit':
                    deal_to(player, self.deck, 1, which_hand)
                    print('Dealt: {}'.format(player.hand[which_hand][-1]))
                    if not check_sum(player, which_hand):
                        choice_loop = False
            except ValueError:
                print('Please input desired action listed')

    def run(self):
        '''Runs game'''
        has_dealed = False
        file_name = 'saves.pckl'
        file = check_file(file_name)
        if file is False:
            print('Exitting Program...')
            exit()
        file_name = file
        players = self.setup(file_name)
        dealer = players[-1]
        while self._game_is_not_over:
            counter = 1
            while has_dealed is False:
                print('\n--------------------------')
                if isinstance(players[0], deal):
                    has_dealed = self.dealer_turn(players[0], players)
                else:
                    player_turn(players[0], counter)
                players = next_player(players)
                counter += 1
                sleep(1)
            counter = 1
            self.inital_choice(players, dealer)
            check_winnings(players, dealer)
            reset_variables(players, file_name)
            if end_prompt() == 'y':
                has_dealed = False
            else:
                print('\n* Thank you for playing! *\n')
                self._game_is_not_over = False
