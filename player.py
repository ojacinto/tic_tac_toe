#  #!/usr/bin/env python3
#  -- coding: utf-8 --
#  ---------------------------------------------------------------------------------
#  Copyright (c) 2019. Oraldo Jacinto Simon
#  #----------------------------------------------------------------------------------
#  All rights reserved.
#  #
#  This is free software; you can do what the LICENCE file allows you to.

from xutil import capture_prompt
from analyzer import RandomAnalyzer, SmartAnalyzer, RuleAnalyse
from figure import FigureX, FigureZero


class Player(object):

    def __init__(self):
        raise Exception("This an abstract class")

    def __new__(cls, *args, **kw):
        orig = super(Player, cls)
        new_instance = orig.__new__(cls)
        new_instance.game_wons = 0
        new_instance.moves = []
        return new_instance


class Human(Player):

    def __init__(self, name='Human', shape=FigureX()):
        self.name = name
        self.shape = shape

    def valid_position(position):
        try:
            number = int(position)
            return True if 1 <= number <= 9 else False
        except:
            return False

    def get_position(self):
        message = 'Please choose a position from 1 to 9'
        return int(capture_prompt(message, Human.valid_position))


class Computer(Player):

    def __init__(self, name='ComputerSmart', shape=FigureZero(), level='smart', game_state=None):
        self.name = name
        self.shape = shape
        self.game_won = 0
        self.level = level
        self.random_analyzer = RandomAnalyzer()
        self.smart_analyser = SmartAnalyzer()
        self.rule_analyzer = RuleAnalyse()

    def get_position(self, board, another_player):
        switch_level = {
            'random': self.random_analyzer.best_move,
            'rules': self.random_analyzer.best_move,
            'smart': self.rule_analyzer.best_move
        }
        method = switch_level.get(self.level)
        return method(board)
