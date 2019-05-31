#  #!/usr/bin/env python3
#  -- coding: utf-8 --
#  ---------------------------------------------------------------------------------
#  Copyright (c) 2019. Oraldo Jacinto Simon
#  #----------------------------------------------------------------------------------
#  All rights reserved.
#  #
#  This is free software; you can do what the LICENCE file allows you to.

from player import Human, Computer
from figure import FigureX, FigureZero


class GameMode(object):

    def restart(self):
        self.player1.moves = []
        self.player2.moves = []

    def __new__(cls, *args, **kw):
        mode = super(GameMode, cls)
        new_instance = mode.__new__(cls)
        _level = kw.get('level', None)
        if _level:
            new_instance._level=_level
        else:
            new_instance._level = None
        new_instance.draws = 0
        return new_instance


class HumanVSComputer(GameMode):

    def __init__(self, game_state=None):
        self.player1 = Human()
        self.player2 = Computer()


class ComputerVSComputer(GameMode):
    def __init__(self, player1='PC1', player2='PC2', game_state=None, level='smart'):
        self.player1 = Computer(name='ComputerRandom', shape=FigureX(), game_state=game_state,
                                level='random')
        if self._level:
            self.player2 = Computer(name='RulesPlayer', level=self._level)
        else:
            self.player2 = Computer(level=level)
