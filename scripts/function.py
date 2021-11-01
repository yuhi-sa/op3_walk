#!/usr/bin/env python
# coding: utf-8
import numpy as np
import random
import torch
from torch import nn
from torch import optim
import torch.nn.functional as F
from collections import namedtuple

BATCH_SIZE = 32
CAPACITY = 10000000
GAMMA = 0.05

Transition = namedtuple(
    'Transition', ('state', 'action', 'next_state', 'reward')
)

class ReplayMemory:
    def __init__(self,CAPACITY):
        self.capacity = CAPACITY
        self.memory = [] 
        self.index = 0
    
    def push(self, state, action, next_state, reward):
        if len(self.memory) < self.capacity:
            self.memory.append(None)
        self.memory[self.index] = Transition(state, action, next_state, reward)
        self.index = (self.index + 1)%self.capacity 
    
    def sample(self, batch_size):
        return random.sample(self.memory, batch_size)

    def __len__(self):
        return len(self.memory)


class Brain:
    def __init__(self, num_states, num_actions):
        self.actions = num_actions
        self.states = num_states
        self.memory = ReplayMemory(CAPACITY)      
        self.model = nn.Sequential()
        self.model.add_module('fc1', nn.Linear(self.states, 32))
        self.model.add_module('relu1', nn.ReLU())
        self.model.add_module('fc2', nn.Linear(32,32))
        self.model.add_module('relu2', nn.ReLU())
        self.model.add_module('fc3', nn.Linear(32, self.actions))
        self.optimizer = optim.Adam(self.model.parameters(),lr=0.0001)

    def replay(self):
        if len(self.memory) < BATCH_SIZE:
            return
        
        # Batch
        transitions = self.memory.sample(BATCH_SIZE)
        batch = Transition(*zip(*transitions))
        state_batch = torch.cat(batch.state)
        action_batch = torch.cat(batch.action)
        reward_batch = torch.cat(batch.reward)
        non_final_next_states = torch.cat([s for s in batch.next_state if s is not None])

        # calculate next_state
        self.model.eval()
        state_action_values = self.model(state_batch).gather(1 ,action_batch)
        non_final_mask = torch.ByteTensor(tuple(map(lambda s:s is not None, batch.next_state)))
        next_state_values = torch.zeros(BATCH_SIZE)
        next_state_values[non_final_mask] = self.model(non_final_next_states).max(1)[0].detach()

        # calculate Q(s_t,a_t)
        expected_state_action_values = reward_batch + GAMMA*next_state_values

        # calculate loss
        self.model.train()
        loss = F.smooth_l1_loss(state_action_values, expected_state_action_values.unsqueeze(1))

        # update params
        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()

    def decide_action(self, state, episode):
        # epsilon-greedy
        epsilon = 1/(episode+1)
        if epsilon <= np.random.uniform(0,1):
            self.model.eval()
            with torch.no_grad():
                action = self.model(state).max(1)[1].view(1,1)
        else:
            action = torch.LongTensor([[random.randrange(self.actions)]])
        return action

class Agent:
    def __init__(self, num_states, num_actions):
        self.brain = Brain(num_states, num_actions)
        self.state = None
        self.next_state = []
        self.action = 0
        self.start_time = 0
        self.trial = 0
        self.episode = 0
        self.last_index = 0
        self.history = []
        self.distance_old = 0

    def update_q_function(self):
        self.brain.replay()
    
    def get_action(self, episode):
        action = self.brain.decide_action(self.state, episode)
        return action
    
    def memorize(self, state_next, reward):
        self.brain.memory.push(self.state, self.action, state_next, reward)