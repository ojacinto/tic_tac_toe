#  #!/usr/bin/env python3
#  -- coding: utf-8 --
#  ---------------------------------------------------------------------------------
#  Copyright (c) 2019. Oraldo Jacinto Simon
#  #----------------------------------------------------------------------------------
#  All rights reserved.
#  #
#  This is free software; you can do what the LICENCE file allows you to.

from position import Position
from draw_board import DrawBoard


def get_victory_positions():
    v1 = [1, 2, 3]
    v2 = [4, 5, 6]
    v3 = [7, 8, 9]
    diagonals = [[1, 5, 9], [3, 5, 7]]
    victory_positions = [v1, v2, v3]
    victory_positions.extend([[v1[pos], v2[pos], v3[pos]] for pos in range(3)])
    victory_positions.extend(diagonals)
    return victory_positions


class Board(object):
    """Represents the game board

    """

    def __init__(self):
        self.positions = [Position() for i in range(9)]
        self.victory_positions = get_victory_positions()

    def empty_positions(self):
        list_positions_index = [index + 1 for index, position in
                                enumerate(self.positions) if not position.occupied]
        return list_positions_index if len(list_positions_index) > 0 else []

    def get_index(self, index):
        try:
            num_index = int(index)
        except:
            return -1
        is_valid = True if 1 <= num_index <= 9 else False
        if is_valid:
            return num_index - 1
        else:
            return -1

    def get_position(self, index):
        message = 'Invalid index of position!: {0}'.format(index)

        index_valid = self.get_index(index)
        if index_valid > -1:
            return self.positions[index_valid]
        else:
            raise IndexError(message)

    def _is_position_occupied(self, index):
        figure = self.get_position(index)
        return figure.occupied

    def fill_positions(self, positions, player):
        for index in positions:
            self.fill_position(index, player.shape)

    def fill_position(self, index, shape):
        if self.empty_positions():
            if self._is_position_occupied(index):
                raise InvalidMove("Invalid position's move!")
            else:
                valid_index = self.get_index(index)
                if valid_index > -1:
                    self.positions[valid_index].set_value(shape)
                else:
                    raise IndexError('Invalid index!: {0}'.format(index))
