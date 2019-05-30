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
import os.path as path
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier


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
        data = numpy.loadtxt('tictac_single.txt')
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
            self._save_classifier(clf, file)
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