#  #!/usr/bin/env python3
#  -- coding: utf-8 --
#  ---------------------------------------------------------------------------------
#  Copyright (c) 2019. Oraldo Jacinto Simon
#  #----------------------------------------------------------------------------------
#  All rights reserved.
#  #
#  This is free software; you can do what the LICENCE file allows you to.


def _fill_positions(board_state, positions, value):
    for pos in range(len(positions)):
        board_state[positions[pos] - 1] = value
    return board_state


def generate_data_set(_copy, file_name):
    """Transform the moves of a game to:
    Example:
      legend: (1=>X), (-1=>0) y (0=>empty)
      _copy = [1, 3, 5, 2, 9]
      output = [-1, 1, 1, 0, -1, 0, 0, 0, 0, 8]

    :param _copy:
    :return: Returns the moves of the game in the nine positions and
    in the position 10 the correct move
    """
    target = _copy[-1] - 1
    _copy.reverse()
    _min1 = _copy[2::2]
    _ones = _copy[1::2]
    board_state = [0, 0, 0, 0, 0, 0, 0, 0, 0]
    board_state = _fill_positions(board_state, _min1, -1)
    board_state = _fill_positions(board_state, _ones, 1)
    line = ' '.join([str(el) for el in board_state])
    line += ' ' + str(target) + ' \n'
    f = open(file_name, 'a')
    f.write(line)
    f.close()
