#  #!/usr/bin/env python3
#  -- coding: utf-8 --
#  ---------------------------------------------------------------------------------
#  Copyright (c) 2019. Oraldo Jacinto Simon
#  #----------------------------------------------------------------------------------
#  All rights reserved.
#  #
#  This is free software; you can do what the LICENCE file allows you to.


class Figure(object):

    def __init__(self):
        raise NotImplementedError("This an abstract class")

    def __repr__(self):
        return self.shape


class FigureZero(Figure):

    def __init__(self):
        self.shape = 'O'

    def __eq__(self, figure):
        """ Compute if `figure` is an instance of class `FigureZero`
        :param figure: Figure that represents the `zeros` and `x` of the players

        """
        if isinstance(figure, FigureZero):
            return self.shape == figure.shape
        return False


class FigureX(Figure):

    def __init__(self):
        self.shape = 'X'

    def __eq__(self, figure):
        """ Compute if `figure` is an instance of class `FigureX`
        :param figure: Figure that represents the `zeros` and `x` of the players

        """
        if isinstance(figure, FigureX):
            return self.shape == figure.shape
        return False



