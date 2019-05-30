#  #!/usr/bin/env python3
#  -- coding: utf-8 --
#  ---------------------------------------------------------------------------------
#  Copyright (c) 2019. Oraldo Jacinto Simon
#  #----------------------------------------------------------------------------------
#  All rights reserved.
#  #
#  This is free software; you can do what the LICENCE file allows you to.

import pickle
FILE = 'game_state'


class ResultGame(object):

    def __init__(self, from_pos, game_moves, winning_player, score):
        self.from_pos = from_pos
        self.game_moves = game_moves
        self.winning_player = winning_player
        self.score = score


class GameState(object):

    def __init__(self):
        try:
            self.load_game_state()
        except:
            self.list_game_results = []

    def save(self):
        if self.list_game_results:
            serialized_results = pickle.dumps(self.list_game_results)
            try:
                with open(FILE, 'w') as game_state_file:
                    game_state_file.write(serialized_results)
            except:
                print('No possible to store the results game!')

    def load_game_state(self):
        with open(FILE, 'r') as game_state_file:
            serialized_results = game_state_file.read()
        self.list_game_results = pickle.loads(serialized_results)

    def exist_game_state(self, game_moves):
        filtered = list(filter(lambda x: x.game_moves == game_moves,
                               self.list_game_results))
        return True if len(filtered) > 0 else False

    def add_game_result(self, game_moves, player_won, from_pos, score):
        if not self.exist_game_state(game_moves):
            game_result = ResultGame(game_moves, player_won, from_pos, score)
            self.list_game_results.append(game_result)
