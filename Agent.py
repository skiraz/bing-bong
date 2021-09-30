import pygame.time
import torch
import random
import numpy as np
from collections import deque
from main import bb_game
from model import Linear_QNet, QTrainer#, mymodel

global reset
reset=True

MAX_MEMORY = 100_000
BATCH_SIZE = 1000
LR = 0.001


class Agent:

    def __init__(self):
        self.n_games = 0
        self.epsilon = 0  # randomness
        self.gamma = 0.9  # discount rate
        self.randomove=random.randint(1,2)
        self.memory = deque(maxlen=MAX_MEMORY)  # popleft()
        self.model = Linear_QNet(8,256,3)
        self.trainer = QTrainer(self.model, lr=LR, gamma=self.gamma)

    def get_state(self, game):
        hit_left=game.hit_left()
        state = [
            game.bar.centerx,
            game.pong.centerx,
            game.pong.centery,
            game.direction == "Left",
            game.direction == "Right",
            game.direction == " ",
            hit_left,
            not hit_left



        ]

        return np.array(state, dtype=int)

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))  # popleft if MAX_MEMORY is reached
    def train_long_memory(self):
        if len(self.memory) > BATCH_SIZE:
            mini_sample = random.sample(self.memory, BATCH_SIZE)
            # list of tuples
        else:
            mini_sample = self.memory

        states, actions, rewards, next_states, dones = zip(*mini_sample)
        self.trainer.train_step(states, actions, rewards, next_states, dones)
        # for state, action, reward, next_state, done in mini_sample:
        #    self.trainer.train_step(state, action, reward, next_state, done)

    def train_short_memory(self, state, action, reward, next_state, done):
        self.trainer.train_step(state, action, reward, next_state, done)
    def resetrandom(self):
        self.randomove=random.randint(0,2)
    def get_action(self, state,seconds):
        global reset
        #print(seconds)
        # random moves: tradeoff exploration / exploitation
        self.epsilon = 100 - self.n_games
        final_move=[0,0,0]
        if random.randint(0,200) <self.epsilon:
            if seconds%3==0:
                print(seconds%3)
                    #print(seconds)
                if reset:
                 self.resetrandom()
            else:
                final_move[self.randomove]=1


        # if random.randint(0, 200) < self.epsilon:
        #     move = random.randint(0, 2)
        #     final_move[move] = 1
        else:
            state0 = torch.tensor(state, dtype=torch.float)
            prediction = self.model(state0)
            move = torch.argmax(prediction).item()
            print(prediction)

            final_move[move] = 1



        return final_move,0


def train():
    agent = Agent()
    game = bb_game()
    while True:


        # get old state
        state_old = agent.get_state(game)

        # get move
        final_move,epsilon = agent.get_action(state_old,game.seconds)

        # perform move and get new state
        reward, done = game.play_step(final_move,epsilon)

        state_new = agent.get_state(game)
            # train short memory
        agent.train_short_memory(state_old, final_move, reward, state_new, done)

        # remember
        agent.remember(state_old, final_move, reward, state_new, done)




        if done:
            # train long memory, plot result
            game.reset()
            agent.n_games += 1
            agent.train_long_memory()
            print('Game', agent.n_games,  reward , done)



        else:
            agent.model.save()




if __name__ == '__main__':
    train()
