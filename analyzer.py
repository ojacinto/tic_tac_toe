#  #!/usr/bin/env python3
#  -- coding: utf-8 --
#  -----------------------------------------------------------------------------------
#  Copyright (c) 2019. Oraldo Jacinto Simon
#  #----------------------------------------------------------------------------------
#  All rights reserved.
#  #
#  This is free software; you can do what the LICENCE file allows you to.

import _pickle as Pickle
import numpy
import random
from board import get_victory_positions
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier


def get_position_relatives():
    return dict(corner=[1, 3, 7, 9], middle=[2, 4, 6, 8], center=[5])


class RandomAnalyzer(object):

    def best_move(self, board):
        moves = board.empty_positions()
        return random.choice(moves)


class MyClassifier(object):

    def __init__(self):
        data = self.load_data()
        self.x_train = data.get('xtrain')
        self.x_test = data.get('xtest')
        self.y_train = data.get('ytrain')
        self.y_test = data.get('ytest')
        self.mlp = self.get_mlp_classifier(file='mlp_classifier.pkl')

    def load_data(self):
        data = numpy.loadtxt('tictac_dataset.txt')
        X = data[:, :9]
        y = data[:, 9:]
        # split the training and testing data
        x_train, x_test, y_train, y_test = train_test_split(
            X, y, test_size=0.25, random_state=42)
        return dict(xtrain=x_train, xtest=x_test, ytrain=y_train, ytest=y_test)

    def _fit(self, clf):
        return clf.fit(self.x_train, self.y_train)

    def get_mlp_classifier(self, file):
        return self._load_classifier(file)

    def _save_classifier(self, clf, name_file):
        # save the classifier
        with open(name_file, 'wb') as fid:
            Pickle.dump(clf, fid)

    def _load_classifier(self, name_file):
        # load it again
        try:
            with open(name_file, 'rb') as fid:
                clf = Pickle.load(fid)
        except FileNotFoundError:
            clf = self.built_mlp()
            self._fit(clf)
            self._save_classifier(clf, name_file)
        return clf

    def get_score(self, clf):
        return clf.score(self.X_test, self.y_test)

    def built_mlp(self):
        return MLPClassifier(hidden_layer_sizes=(400,), max_iter=307, alpha=1e-4,
                            solver='sgd', verbose=10, tol=1e-4, random_state=1,
                            learning_rate_init=.1)

    def predit_move(self, board_state):
        return self.mlp.predict(numpy.array(board_state).reshape(1, -1))[0]


class SmartAnalyzer(object):

    def __init__(self):
        self.X_test = None
        self.y_test = None
        self.classifier = MyClassifier()

    def transform_board_state(self, board):
        positions = []
        for pos in board.positions:
            value = str(pos.value)
            if value == 'X':
                positions.append(1.)
            elif value == 'O':
                positions.append(-1.)
            else:
                positions.append(0.)
        return positions

    def best_move(self, board):
        board_state = self.transform_board_state(board)
        move = self.classifier.predit_move(board_state)
        return int(move) + 1


class RuleAnalyse(object):

    def __init__(self, base_state=False, show_analysis=False):
        self.base_state = base_state
        self.victory_positions = get_victory_positions()
        positions = get_position_relatives()
        self.corner = positions.get('corner')
        self.middle = positions.get('middle')
        self.center = positions.get('center')

    def analyze_game(self, board, player, rival_player):
        is_last_move = self.get_last_move(board, player, rival_player)
        if is_last_move is not None:
            return is_last_move

        first_rules_apply = self.apply_rules_first_moves(player, rival_player)
        if first_rules_apply is not None:
            return first_rules_apply

        empty_positions = board.empty_positions()

        victory_after = self.victory_after(board, empty_positions,
                                               player, rival_player)
        if victory_after:
            return victory_after

        if empty_positions:
            return random.choice(empty_positions)

    def identify_first_moves(self, player, count_move=0):
        result = False
        if len(player.moves) == count_move:
            result = True
        return result

    def apply_rules_first_moves(self, player, rival_player):
        first_move_rival_player = rival_player.moves[0]
        if self.identify_first_moves(player) and self.identify_first_moves(rival_player):
            first_join = self.corner + self.center
            random_choice = random.choice(first_join + self.middle)
            return random_choice
        # If the opposing player started and the first player has not played
        elif self.identify_first_moves(player) and self.identify_first_moves(rival_player, 1):
            # If the rival player played in the corner play in the center
            if first_move_rival_player in self.corner:
                return self.center
            # If the rival player played in the center play in the corners
            if first_move_rival_player == self.center:
                return random.choice(self.corner)
        return None

    def get_last_move(self, board, player, rival_player):
        win = self.win_in_a_move(board, player)
        lose = self.loses_in_a_move(board, rival_player)
        if win:
            return win[0]
        elif lose:
            return lose[0]
        return None

    def victory_after(self, board, empty_positions, player,
                      rival_player):

        victory_win_after = self.victory_win_after(board, empty_positions,
                                                      player)
        if victory_win_after:
            return victory_win_after[0]

        rival_victory_win_after = self.victory_win_after(board, empty_positions,
                                                          rival_player)

        if rival_victory_win_after:
            return rival_victory_win_after[0]
        return []

    def win_in_a_move(self, board, player):
        player_mov = set(player.moves)
        win_moves = []
        for i in get_victory_positions():
            victory_pos = None
            v_position = set(i)
            union = player_mov.intersection(v_position)
            diff = v_position.difference(player_mov)
            if len(union) > 1 and len(diff) == 1:
                victory_pos = diff.pop()
                try:
                    is_position_occupied = board.is_position_occupied(victory_pos)

                    if not is_position_occupied:
                        win_moves.append(victory_pos)
                except:
                    pass
        return win_moves

    def loses_in_a_move(self, board, rival_player):
        return self.win_in_a_move(board, rival_player)

    def victory_win_after(self, board, empty_positions, player):
        copy_board = board.copy()
        victory_after = []
        for index in empty_positions:
            copy_board.fill_position(index, player.shape)
            player.moves.append(index)
            win_in_one = self.win_in_a_move(copy_board, player)
            if len(win_in_one) > 1:
                victory_after.append(index)
            player.moves.remove(index)
            copy_board.clear_position(index)
        return victory_after

    def best_move(self, board, player, rival_player,
                                 show_analysis=False):
        return self.analyze_game(board, player, rival_player)
