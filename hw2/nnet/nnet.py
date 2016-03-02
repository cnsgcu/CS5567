import random
import numpy as np

from scipy.special import expit

class MLPNNet:
    def predict(self, observation):
        return self._compute_(observation)[-1]


    def train(self, tolerance=5.e-3, learning_rate=0.1, max_iteration=1000, snapshot=100):
        self._term_iteration = self._iteration + max_iteration
        self._snapshot, self._tolerance, self._learning_rate  = snapshot, tolerance, learning_rate

        for observation, target in self._random_training_set_():
            self._sigmas = self._compute_(observation)

            if self._should_stop_(): return
            else:
                self._evolve_(target)
                self._iteration += 1


    def describe(self):
        return { 'weights': self._weights, 'errors': self._MSE, 'iteration': self._iteration }


    def __init__(self, training_set, hidden_layers=[]):
        self._MSE = []
        self._iteration, self._term_iteration = 0, 0
        self._activation_ = (lambda x: 1 if x > 0 else 0) if not hidden_layers else lambda x: expit(x)
        self._activation_prime_ = (lambda z: 1) if not hidden_layers else lambda z: z * (1 - z)

        observations, targets = [np.array([np.reshape(row[i], (-1, 1)) for row in training_set]) for i in range(2)]
        self._training_set = [training_data for training_data in zip(observations, targets)]

        hidden_layers = [observations.shape[1]] + hidden_layers + [targets.shape[1]]
        self._weights = [np.random.uniform(-1, 1, (D[0] + 1, D[1])) for D in zip(hidden_layers[:-1], hidden_layers[1:])]


    def _random_training_set_(self):
        while True: yield random.choice(self._training_set)


    def _compute_(self, observation):
        sigmas = [np.reshape(observation, (-1, 1))]

        for i in range(len(self._weights)):
            bias_sigma = np.vstack(([1], sigmas[i]))
            sigmas.append(self._activation_(self._weights[i].T.dot(bias_sigma)))

        return sigmas


    def _evolve_(self, target):
        self._deltas = [np.atleast_2d(target - self._sigmas[-1]) * self._activation_prime_(self._sigmas[-1])]

        for idx in range(len(self._sigmas) - 2, 0, -1):
            bias_activation_prime = np.vstack(([1], self._activation_prime_(self._sigmas[idx])))
            self._deltas[:0] = [((self._weights[idx].dot(self._deltas[0])) * bias_activation_prime)[1:,:]]

        for idx in range(len(self._weights)):
            self._weights[idx] += self._learning_rate * np.vstack(([1], self._sigmas[idx])).dot(self._deltas[idx].T)


    def _should_stop_(self):
        mse = np.sum([0.5 * np.sum((self.predict(observation) - target) ** 2) for observation, target in self._training_set])

        if (self._iteration + 1) == self._snapshot * (len(self._MSE) + 1):
            self._MSE.append(mse)

        return np.less_equal(mse, self._tolerance) or self._iteration == self._term_iteration