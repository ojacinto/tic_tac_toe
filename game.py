#  #!/usr/bin/env python3
#  -- coding: utf-8 --
#  ---------------------------------------------------------------------------------
#  Copyright (c) 2019. Oraldo Jacinto Simon
#  #----------------------------------------------------------------------------------
#  All rights reserved.
#  #
#  This is free software; you can do what the LICENCE file allows you to.

from xutil import capture_prompt, validate_value
from draw_board import DrawBoard
from board import Board
from player import Human
from game_state import GameState, ResultGame
from mode import (HumanVSComputer, ComputerVSComputer)


class TicTacToe(object):
    """Represents the game board

    """

    def __init__(self, mode=None, game_state=None, select_player=0):
        self.game_state = GameState()
        self.board_painter = DrawBoard()
        if mode:
            self.mode = mode
        else:
            self.show_menu()
            self.mode = None
        self.is_over = False
        self.won_position = None
        self.winner = None
        self.current_player = None
        self.moves_game = []
        self.init_game()
        self.start_game()

    def show_menu(self):
        welcome = """!!!!!!!Welcome to Tic-Tac-Toe Game.!!!!!!!"""
        summary = """Tic-tac-toe (American English), noughts and crosses (British English), or Xs and Os
is a paper-and-pencil game for two players, X and O, who take turns marking the spaces 
in a 3×3 grid. Each of the positions are represented with numbers from one to nine.
If the spaces are free you can select the number that corresponds in the range of one
to nine. Win the first to achieve three consecutive figures in a straight line."""
        self.board_painter.draw(show_positions=True)
        print(welcome)
        print(summary)
        input('Press enter to begin:')

    def get_game_mode(self):
        modes = {
            1: HumanVSComputer,
            2: ComputerVSComputer
        }
        if self.mode is not None:
            self.mode.restart()
            return self.mode
        else:
            print(''' Game Modes:
             1. HumanVSComputer
             2. ComputerVSComputer''')
            game_mode = capture_prompt(message='Please select a game mode:',
                                       value=validate_value)
            class_mode = modes.get(int(game_mode))
            return class_mode()

    def ask_player_starts(self):
        print('Select the first player to play:')
        message = 'Enter `1` for player1: {0}  or `2` for player2: {1}.'.format
        message = message(self.mode.player1.name,
                          self.mode.player2.name)
        validator = validate_value
        select = capture_prompt(message, validator)
        if select == '1':
            self.current_player = self.mode.player1
        else:
            self.current_player = self.mode.player2

    def init_game(self):
        self.board = Board()
        self.board_painter.set(self.board)
        self.mode = self.get_game_mode()
        if isinstance(self.mode, ComputerVSComputer):
            players = [self.mode.player1, self.mode.player2]
            import random
            self.current_player = random.choice(players)
        else:
            self.ask_player_starts()
        self.is_over = False
        self.won_position = None
        self.winner = None
        self.moves_game = []

    def is_player_won(self, player, test_mode=False):
        if len(player.moves) < 3:
            return False
        player_moves = set(player.moves)
        for position in self.board.victory_positions:
            win_position = set(position)
            if win_position.issubset(player_moves):
                if not test_mode:
                    self.won_position = position
                    self.winner = player
                    self.update_player_games_won()
                return True
        return False

    def first_or_second_in_to_play(self, player):
        return 1 if player.moves[0] == self.moves_game[0] else 2

    def store_game_result(self, player):
        from_pos, score = 0, 8
        self.game_state.add_game_result(self.moves_game,
                                        self.first_or_second_in_to_play(player),
                                        from_pos, score)

    def show_game_history(self):
        match = "Results: Player{0}: {1} vs Player{2}: {3} 'Draws': {4}. "
        print(match.format(
            self.mode.player1.name, self.mode.player1.game_wons,
            self.mode.player2.name, self.mode.player2.game_wons,
            self.mode.draws))

    def exit(self, base_state=False):
        self.is_over = True
        if base_state:
            #self.base_state.save()
            pass
        print('Game over!!!!')

    def is_game_finish(self):
        self.exit(True)

    def show_game_result(self):
        self.board_painter.draw()
        if self.winner:
            result = '{0}Player: {1} WON.WONDERFUL!!{2}'
            result = result.format('*'*10, self.winner.name, '*'*10)
        else:
            result = '{0}The game is draw{1}'
            result = result.format('*'*15, '*'*15)
        print(result)
        print('Player: {0}: moves: {1}'.format(
            self.mode.player1.name, self.mode.player1.moves))
        print('Player: {0}: moves: {1}'.format(
            self.mode.player2.name, self.mode.player2.moves))
        self.show_game_history()
        self.is_game_finish()

    def check_winner(self):
        players = [self.mode.player1, self.mode.player2]
        for p in players:
            player_won = self.is_player_won(p)
            if player_won:
                if isinstance(self.mode, ComputerVSComputer):
                    self.store_game_result(p)
                self.show_game_result()

    def check_draw(self):
        if not self.board.empty_positions():
            self.mode.draws += 1
            self.show_game_result()

    def verify_status_game(self):
        self.check_winner()
        self.check_draw()

    def start_game(self):
        while not self.is_over:
            self.board_painter.update_board(self.board)
            self.show_player_info()
            position = self.next_move()
            self.moves_game.append(position)
            self.verify_status_game()
            self.update_current_player()

    def get_vs_current_player(self):
        if self.mode.player1 == self.current_player:
            return self.mode.player2
        else:
            return self.mode.player1

    def update_player_moves(self, move):
        if self.mode.player1 == self.current_player:
            self.mode.player1.moves.append(move)
        else:
            self.mode.player2.moves.append(move)

    def update_player_games_won(self):
        if self.mode.player1 == self.current_player:
            self.mode.player1.game_wons += 1
        else:
            self.mode.player2.game_wons += 1

    def update_current_player(self):
        if self.current_player == self.mode.player1:
            self.current_player = self.mode.player2
        else:
            self.current_player = self.mode.player1

    def next_move(self):
        position_found = False
        while not position_found:
            if isinstance(self.current_player, Human):
                position = self.current_player.get_position()
            else:
                # Is the computer
                position = self.current_player.get_position(
                    self.board, self.get_vs_current_player())
            try:
                shape = self.current_player.shape
                self.board.fill_position(position, shape)
                position_found = True
            except Exception as e:
                raise e
        self.update_player_moves(position)
        return position

    def show_player_info(self):
        inf = 'Player {0}: figure => "{1}" (Vs) Player {2}: figure => "{3}"'
        player_name_1 = self.mode.player1.name
        player_shape_1 = self.mode.player1.shape
        player_name_2 = self.mode.player2.name
        player_shape_2 = self.mode.player2.shape
        players_inf = inf.format(player_name_1, player_shape_1, player_name_2, player_shape_2)
        print(players_inf)
        print('Current player: {0}'.format(self.current_player.name))


if __name__ == '__main__':
    val = 1
    game = TicTacToe()
    while val < 10:
        game = TicTacToe(mode=game.mode)
        val += 1