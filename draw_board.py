#  #!/usr/bin/env python3
#  -- coding: utf-8 --
#  ---------------------------------------------------------------------------------
#  Copyright (c) 2019. Oraldo Jacinto Simon
#  #----------------------------------------------------------------------------------
#  All rights reserved.
#  #
#  This is free software; you can do what the LICENCE file allows you to.

import os


class DrawBoard(object):
    """ Draw the game board.
     Print the board in the form of lines of characters

    """

    def __init__(self):
        self._row1 = '   {0}  |  {1}  |  {2}  \n _____|_____|_____\n'
        self._row2 = '   {0}  |  {1}  |  {2}  \n _____|_____|_____\n'
        self._row3 = '   {0}  |  {1}  |  {2}  \n      |     |     '

    def set(self, board):
        self.board = board

    def update_board(self, board):
        self.board = board
        self.draw()

    @staticmethod
    def clear_board():
        os.system('cls' if os.name == 'nt' else 'clear')

    def draw(self, show_positions=False):
        if show_positions:
            row_position1 = [1, 2, 3]
            row_position2 = [4, 5, 6]
            row_position3 = [7, 8, 9]
        else:
            row_position1 = [pos.value for pos in self.board.positions[:3]]
            row_position2 = [pos.value for pos in self.board.positions[3:6]]
            row_position3 = [pos.value for pos in self.board.positions[6:9]]

        DrawBoard.clear_board()
        row1 = self._row1.format(*row_position1)
        row2 = self._row2.format(*row_position2)
        row3 = self._row3.format(*row_position3)
        print("Board: ")
        print(row1 + row2 + row3)




