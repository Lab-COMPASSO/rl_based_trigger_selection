import random
import gym
import numpy as np
from collections import deque
from keras.models import Sequential
from keras.layers import Dense
from keras.optimizers import Adam


class DQNAgent:
    def __init__(self, state_size=None, action_size=None, epsilon_decay=0.995, epsilon=1.0, epsilon_min=0.01,
                 gamma=0.95, alpha=.001, alpha_decay=0.995):

        self.memory = deque(maxlen=100000)
        self.state_size = state_size
        self.action_size = action_size
        self.epsilon = epsilon                          # Exploration rate
        self.epsilon_decay = epsilon_decay              # Exponential decay rate for exploration prob
        self.epsilon_min = epsilon_min                  # Minimum exploration probability
        self.gamma = gamma                              # Discounting rate
        self.alpha = alpha                              # Learning rate
        self.alpha_decay = alpha_decay
        self.model = self._build_model()

    def _build_model(self):
        # Neural Net for Deep-Q learning Model
        model = Sequential()
        model.add(Dense(24, input_dim=self.state_size, activation='relu'))
        model.add(Dense(24, activation='relu'))
        model.add(Dense(self.action_size, activation='linear'))
        model.compile(loss='mse', optimizer=Adam(lr=self.alpha, decay=self.alpha_decay))
        return model

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    def act(self, state):
        if np.random.rand() <= self.epsilon:
            return random.randrange(self.action_size - 1)
        act_values = self.model.predict(state)
        return np.argmax(act_values[0])  # returns action

    def replay(self, batch_size):
        mini_batch = random.sample(self.memory, batch_size)
        for state, action, reward, next_state, done in mini_batch:
            target = reward
            if not done:
                target = (reward + self.gamma *
                          np.amax(self.model.predict(next_state)[0]))
            target_f = self.model.predict(state)
            target_f[0][action] = target
            self.model.fit(state, target_f, epochs=1, verbose=0)
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay

    def load(self, name):
        self.model.load_weights(name)

    def save(self, name):
        self.model.save_weights(name)

