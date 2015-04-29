#!/usr/bin/env python2.7
"""
A gambling, dice rolling game. Score 100 points to win.
A player scores the sum total of the roll of three six-sided dice.
Continue rolling until the player rolls a 1, or chooses to bank their points.
Rolling a 1 ends the players turn, and they forfeit all points accumulated that turn.
Rolling two 1s ends the players turn, and resets their score to 0.
Rolling three 1s ends the players turn, and puts them out of the game.
After a player scores 100 (or more) points, all other players take one more turn.
"""

import argparse
from random import randint
from time import sleep

class Dice:
    """All three dice are always rolled together"""
    def __init__(self):
        self.min_value = 1
        self.max_value = 6
        self.values = [self.min_value, self.min_value, self.min_value]


    def __str__(self):
        """Return a string representation of all three dice."""
        return "%d + %d + %d = %d" % \
                (self.values[0], self.values[1], self.values[2], self.total())


    def __repr__(self):
        """Return a string representation of all three dice."""
        return "Die 1: %d\nDie 2: %d\nDie 3: %d" % \
                (self.values[0], self.values[1], self.values[2])


    def roll(self):
        """Roll all three dice, return the total and the number of 1s rolled."""
        for i in range(0, 3):
            self.values[i] = randint(self.min_value, self.max_value)

        ones = self.values.count(1)

        return (self.values, ones)

    def total(self):
        """Return the integer value of the sum of the last roll of the dice."""
        return sum(self.values)


class Player:
    def __init__(self, name):
        self.name = name
        self.score = 0
        self.out_of_turns = False


    def __str__(self):
        """Return a string representation of a player's name and score"""
        return "%s: %d points" % (self.name, self.score)


    def __repr__(self):
        """Return a string representation of a player's name and score"""
        return "%s: %d points" % (self.name, self.score)


    def add_points(self, points):
        """Add points to the player's score"""
        self.score = self.score + points


    def take_turn(self, dice):
        """Roll all three dice, decide whether to roll again or keep points."""
        still_rolling = True
        running_total = 0
        print "------------"

        while still_rolling:
            print self.name + " rolled"
            roll, ones = dice.roll()
            print dice

            if ones == 0:
                # Prompt to keep rolling
                running_total = running_total + dice.total()
                inp = raw_input("%d points on the line. Roll again? (Y/n) " % running_total)
                if inp.strip().lower() == 'n':
                    self.add_points(running_total)
                    return
            elif ones == 1:
                still_rolling = False
                print("Rolled a 1, lost turn.")
                sleep(1)
                return
            elif ones == 2:
                still_rolling = False
                print("Rolled two 1s, lost all points.")
                self.score = 0
                sleep(1)
                return
            elif ones == 3:
                still_rolling = False
                print("Rolled three 1s, lost the game.")
                self.score = 0
                self.out_of_turns = True
                sleep(1)
                return


def print_scores(players):
    """Take a list of players and print all their scores"""
    print "Scores"
    print "------------"
    for player in players:
        print player


def main():
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('number_of_players', metavar='PLAYERS', type=int,
            help='Number of players')
    args = parser.parse_args()

    dice = Dice()

    # Collect player names
    players = []

    for i in range(0, args.number_of_players):
        name = raw_input("Player " + str(i + 1) + " name: ")
        new_player = Player(name)
        players.append(new_player)

    # Take turns
    game_over = False
    last_turn = False

    while not game_over:
        players_out_of_turns = 0
        for player in players:
            if not player.out_of_turns:
                player.take_turn(dice)
                if player.score >= 100:
                    print "%s has %d points! Last turn!" % (player.name, player.score)
                    player.out_of_turns = True
                    last_turn = True
                if last_turn:
                    player.out_of_turns = True
            else:
                players_out_of_turns = players_out_of_turns + 1
                if players_out_of_turns == len(players):
                    game_over = True

        print_scores(players)


if __name__ == "__main__":
    main()
