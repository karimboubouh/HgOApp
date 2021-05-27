import time

import numpy as np
from sklearn.utils import shuffle

from backend.optimizers import LROptimizer
from backend.utils import get_batch, sigmoid, accuracy


class LogisticRegression(object):
    """
    Logistic Regression
    """

    def __init__(self, n_features, lr=0.001, epochs=200, batch_size=128, threshold=0.5, debug=True):
        self.lr = lr
        self.epochs = epochs
        self.batch_size = batch_size
        self.optimizer = None
        self.threshold = threshold
        self.debug = debug
        self.costs = []
        self._accuracies = []
        self.W = np.random.randn(n_features, 1) * 0.01

    def one_epoch(self, X, y, block, optimizer=LROptimizer):
        self.optimizer = optimizer(self.W, self.lr, block)
        if self.batch_size > 0:
            features, labels = self.get_random_batch(X, y)
        elif self.batch_size == 0:
            features, labels = shuffle(X, y)
        else:
            raise
        # Foreword step
        predictions = self.forward(features)
        # Optimization step
        grads, gtime = self.optimizer.optimize(labels, predictions, features)

        return grads, gtime

    def get_random_batch(self, X, y):
        sX, sy = shuffle(X, y)
        m = X.shape[0]

        if m < self.batch_size:
            self.batch_size = m
        nb_batches = (m // self.batch_size)
        j = np.random.choice(nb_batches, replace=False)
        return get_batch(sX, sy, self.batch_size, j)

    def forward(self, X):
        # a = np.dot(self.W.T, X.T)
        a = X @ self.W
        return sigmoid(a)

    def predict(self, X):
        y_pred = sigmoid(np.dot(self.W.T, X.T))
        return np.array(list(map(lambda x: 1 if x >= 0.5 else 0, y_pred.flatten())))

    def evaluate(self, X, y, optimizer=LROptimizer):
        self.optimizer = optimizer(self.W, self.lr, None)
        predictions = self.forward(X)
        cost = self.optimizer.loss(y, predictions)
        acc = accuracy(y, predictions)
        return cost, acc


if __name__ == '__main__':
    pass
