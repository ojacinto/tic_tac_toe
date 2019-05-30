#  #!/usr/bin/env python3
#  -- coding: utf-8 --
#  ---------------------------------------------------------------------------------
#  Copyright (c) 2019. Oraldo Jacinto Simon
#  #----------------------------------------------------------------------------------
#  All rights reserved.
#  #
#  This is free software; you can do what the LICENCE file allows you to.

from figure import Figure


class Position(object):

    def __init__(self):
        self.reset_position()

    def reset_position(self):
        """Change the value of the position to an empty string

        """
        self.occupied = False
        self.value = ' '

    def set_value(self, figure):
        """Change the value of the position given the `figure` passed
         by parameter

        :param figure: Figure that represents the `zeros` and `x` of the players

        """
        if isinstance(figure, Figure):
            self.value = figure
            self.occupied = True
        else:
            print("In one position there can only be figures of the game")

    def __eq__(self, position):
        return self.value == position.value
