#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul  18 16:51:00 2019

@author: RaMy
"""

from dqn_agent import DQNAgent as dqn
from environment import ENV
import numpy as np


# Environment variables
nb_mec = 3
nb_vnfs = 2
# MECs
min_cpu = 50
max_cpu = 100
min_ram = 50
max_ram = 100
min_disk = 4096
max_disk = 12288
# Containers
min_c_cpu = 1
max_c_cpu = 4
min_c_ram = 1
max_c_ram = 4
min_c_disk = 512
max_c_disk = 4096

# DQN_agent
episodes = 1000                        # Total episodes for the training
batch_size = 32                         # Total used memory in memory replay mode
max_env_steps = 100                    # Max steps per episode

# Generate the MEC environment
env = ENV(nb_mec, nb_vnfs, min_cpu, max_cpu, min_ram, max_ram, min_disk, max_disk, min_c_cpu, max_c_cpu, min_c_ram,
          max_c_ram, min_c_disk, max_c_disk)
env.generate_mec()
env.generate_vnfs()
env.save_topology("environment")

# Computation of action/states size
action_size = len(env.vnfs) * (len(env.mec) + 2 * 3)
print('action_size: {}'.format(action_size))
# TODO: requires RNN for dynamic number of states
state_size = len(env.mec) * 3 + len(env.vnfs) * 2
print('state_size: {}'.format(state_size))

# Instantiating the DQN_Agent
agent = dqn(state_size, action_size)


done = False

for e in range(episodes):
    state = env.get_dqn_state(True)
    state = np.reshape(state, [1, state_size])
    for time in range(max_env_steps):
        print('@@@@@@@@@@@@-- The Current environment --@@@@@@@@@@@@')
        env.view_infrastructure()
        action = agent.act(state)
        print('The selected action is {}'.format(action))
        next_state, reward, done, _ = env.step(action)
        print('@@@@@@@@@@@@-- The Next environment --@@@@@@@@@@@@')
        env.view_infrastructure()
        reward = reward if not done else -10
        next_state = np.reshape(next_state, [1, state_size])
        agent.remember(state, action, reward, next_state, done)
        state = next_state
        if time >= 99:
            print("episode: {}/{}, score: {}, e: {:.2}"
                  .format(e, episodes, time, agent.epsilon))
            break
        if len(agent.memory) > batch_size:
            agent.replay(batch_size)





