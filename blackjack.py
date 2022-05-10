#!/usr/bin/env python3
# Julian Ogata
# CPSC 386-01
# 2022-3-22
# jogata@csu.fullerton.edu
# @jogata5
#
# Lab 03-00
#
# Executable file for my pig game
#

"""Game Executable file"""

from blackjackgame.game import BlackJackGame as g


if __name__ == "__main__":
    BLACKJACK = g()
    BLACKJACK.run()
