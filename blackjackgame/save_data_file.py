#!/usr/bin/env python3
# Julian Ogata
# CPSC 386-01
# 2022-3-22
# jogata@csu.fullerton.edu
# @jogata5
#
# Lab 03-00
#
# File that holds functions to retrive and save player data into a file
#    using pickle
#

'''Save to Data File Functions'''

import pickle


def to_file(pickle_file, players):
    '''Saves player data into a data file as a dict'''
    saves = from_file(pickle_file)
    try:
        with open(pickle_file, 'wb') as file_handle:
            for player in players:
                if saves.get(player.user_id):
                    saves.update({player.user_id: player})
                else:
                    saves[player.user_id] = player
            pickle.dump(saves, file_handle, pickle.HIGHEST_PROTOCOL)
    except FileNotFoundError:
        print('Data file not found')
        return False


def from_file(pickle_file):
    '''Loads player data'''
    try:
        with open(pickle_file, 'rb') as file_handle:
            try:
                players = pickle.load(file_handle)
            except EOFError:
                players = {}
        return players
    except FileNotFoundError:
        print('Data file not found')
        return False
